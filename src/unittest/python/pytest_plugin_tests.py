#   -*- coding: utf-8 -*-
#
#   Copyright 2016 Alexey Sanko
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

from os import mkdir
from os.path import join as path_join
from mock import Mock
from shutil import rmtree
from sys import path as sys_path
from tempfile import mkdtemp
from unittest import TestCase

from pybuilder.core import Project
from pybuilder.errors import BuildFailedException
from pybuilder_pytest import initialize_pytest_plugin, run_unit_tests


class PytestPluginInitializationTests(TestCase):
    def setUp(self):
        self.project = Project("basedir")

    def test_should_set_dependency(self):
        mock_project = Mock(Project)
        initialize_pytest_plugin(mock_project)
        mock_project.plugin_depends_on.assert_called_with('pytest')

    def test_should_set_default_properties(self):
        initialize_pytest_plugin(self.project)
        expected_default_properties = {
                "dir_source_pytest_python": "src/unittest/python"
                }
        for property_name, property_value in expected_default_properties.items():
            self.assertEquals(self.project.get_property(property_name), property_value)

    def test_should_leave_user_specified_properties_when_initializing_plugin(self):
        expected_properties = {
            "dir_source_pytest_python": "some/path"
            }
        for property_name, property_value in expected_properties.items():
            self.project.set_property(property_name, property_value)

        initialize_pytest_plugin(self.project)

        for property_name, property_value in expected_properties.items():
            self.assertEquals(self.project.get_property(property_name), property_value)


pytest_file_success = """
def test_pytest_base_success():
    assert True
"""

pytest_file_failure = """
def test_pytest_base_failure():
    assert False
"""

pytest_conftest_result_to_file = """
from os.path import abspath, dirname, join as path_join
curr_dir = dirname(abspath(__file__))

def pytest_collection_modifyitems(config, items):
    verbose_flag = config.getoption('verbose')
    capture = config.getoption('capture')
    tests_list = []
    for item in items:
        tests_list.append(item.name)
    f = open(path_join(curr_dir, 'pytest_collected_config.out'), 'w')
    f.write(str(verbose_flag) + '\\n')
    f.write(str(capture) + '\\n')
    f.write(','.join(tests_list))
    f.flush()
    f.close()
"""

pytest_file_success_with_extra_args = """
def test_success_with_extra_args(test_arg):
    assert test_arg == "test_value"
"""

pytest_conftest_test_arg = """
import pytest

def pytest_addoption(parser):
    parser.addoption("--test-arg", action="store")

@pytest.fixture
def test_arg(request):
    return request.config.getoption("--test-arg")
"""

pytest_file_class_globs = """
class TestSuccess():
    def test_pytest_base_success(self):
        assert True

class CheckSuccess():
    def test_pytest_base_success(self):
        assert True

class SuccessTest():
    def test_pytest_base_success(self):
        assert True
"""

pytest_file_func_globs = """
def test_pytest_base_success():
    assert True

def pytest_base_success_test():
    assert True

def check_pytest_base_success():
    assert True
"""


class PytestPluginRunningTests(TestCase):
    def setUp(self):
        self.tmp_test_folder = mkdtemp()

    def create_test_project(self, name, content_dict):
        project_dir = path_join(self.tmp_test_folder, name)
        mkdir(project_dir)
        test_project = Project(project_dir)
        initialize_pytest_plugin(test_project)
        tests_dir = path_join(project_dir, 'tests')
        mkdir(tests_dir)
        test_project.set_property('dir_source_pytest_python',
                                  'tests')
        src_dir = path_join(project_dir, 'src')
        mkdir(src_dir)
        test_project.set_property('dir_source_main_python',
                                  'src')
        for file_name, content in content_dict.items():
            f = open(path_join(tests_dir, file_name), 'w')
            f.write(content)
            f.flush()
            f.close()
        test_project.set_property('verbose', True)
        return test_project

    def read_pytest_conftest_result_file(self, dir):
        out_file = path_join(dir, 'pytest_collected_config.out')
        f = open(out_file, 'r')
        out = dict()
        out.update({'verbose': f.readline().strip()})
        out.update({'capture': f.readline().strip()})
        out.update({'tests_list': f.readline().strip().split(',')})
        f.close()
        return out

    def test_should_run_pytest_tests(self):
        test_project = self.create_test_project('pytest_success', {'test_success.py': pytest_file_success})
        run_unit_tests(test_project, Mock())
        self.assertTrue(test_project.expand_path('$dir_source_main_python') in sys_path)
        self.assertTrue(test_project.expand_path('$dir_source_pytest_python') in sys_path)

    def test_should_run_pytest_tests_without_verbose(self):
        test_project = self.create_test_project('pytest_success_without_verbose',
                                                {'test_success_without_verbose.py': pytest_file_success,
                                                 'conftest.py': pytest_conftest_result_to_file})
        run_unit_tests(test_project, Mock())
        cfg = self.read_pytest_conftest_result_file(test_project.expand_path('$dir_source_pytest_python'))
        self.assertEqual(cfg['verbose'], '0')
        self.assertEqual(cfg['capture'], 'fd')

    def test_should_run_pytest_tests_with_verbose(self):
        test_project = self.create_test_project('pytest_success_with_verbose',
                                                {'test_success_with_verbose.py': pytest_file_success,
                                                 'conftest.py': pytest_conftest_result_to_file})
        test_project.set_property('verbose', True)
        run_unit_tests(test_project, Mock())
        cfg = self.read_pytest_conftest_result_file(test_project.expand_path('$dir_source_pytest_python'))
        self.assertEqual(cfg['verbose'], '1')
        self.assertEqual(cfg['capture'], 'no')

    def test_should_correct_get_pytest_failure(self):
        test_project = self.create_test_project('pytest_failure', {'test_failure.py': pytest_file_failure})
        self.assertRaises(BuildFailedException, run_unit_tests, test_project, Mock())
        # has to be compatible with Python 2.6
        # with self.assertRaises(BuildFailedException) as context:
        #     run_unit_tests(test_project, Mock())

    def test_should_run_pytest_tests_with_extra_args(self):
        test_project = self.create_test_project('pytest_success_with_extra_args',
                                                {'test_success_with_extra_args.py': pytest_file_success_with_extra_args,
                                                 'conftest.py': pytest_conftest_test_arg})
        test_project.set_property("pytest_extra_args",
                                  test_project.get_property("pytest_extra_args")
                                  + ["--test-arg", "test_value"])
        run_unit_tests(test_project, Mock())

    def test_should_run_pytest_tests_with_module_glob(self):
        test_project = self.create_test_project('pytest_success_with_module_glob',
                                                {'test_success_with_module_glob.py': pytest_file_success,
                                                 'success_with_module_glob_test.py': pytest_file_success,
                                                 'check_success_with_module_glob.py': pytest_file_success,
                                                 'success_with_module_glob_check.py': pytest_file_success,
                                                 'conftest.py': pytest_conftest_result_to_file})
        test_project.get_property("pytest_python_module_globs").append("check_*")
        run_unit_tests(test_project, Mock())
        cfg = self.read_pytest_conftest_result_file(test_project.expand_path('$dir_source_pytest_python'))
        self.assertEqual(len(cfg['tests_list']), 3)

    def test_should_run_pytest_tests_with_class_glob(self):
        test_project = self.create_test_project('pytest_success_with_class_glob',
                                                {'test_success_with_class_glob.py': pytest_file_class_globs,
                                                 'conftest.py': pytest_conftest_result_to_file})
        test_project.get_property("pytest_class_globs").append("Check*")
        run_unit_tests(test_project, Mock())
        cfg = self.read_pytest_conftest_result_file(test_project.expand_path('$dir_source_pytest_python'))
        self.assertEqual(len(cfg['tests_list']), 2)

    def test_should_run_pytest_tests_with_function_glob(self):
        test_project = self.create_test_project('pytest_success_with_func_glob',
                                                {'test_success_with_func_glob.py': pytest_file_func_globs,
                                                 'conftest.py': pytest_conftest_result_to_file})
        test_project.get_property("pytest_function_n_method_globs").append("check_*")
        run_unit_tests(test_project, Mock())
        cfg = self.read_pytest_conftest_result_file(test_project.expand_path('$dir_source_pytest_python'))
        self.assertEqual(len(cfg['tests_list']), 2)

    def test_should_fail_pytest_tests_with_module_glob_and_inifile(self):
        test_project = self.create_test_project('pytest_inifile_exists',
                                                {'test_fail_inifile_exists.py': pytest_file_success,
                                                 'pytest.ini': pytest_file_success})
        test_project.get_property("pytest_python_module_globs").append("check_*")
        self.assertRaises(BuildFailedException, run_unit_tests, test_project, Mock())


    def tearDown(self):
        rmtree(self.tmp_test_folder)
