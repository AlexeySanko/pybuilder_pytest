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

from os.path import join as join_path
from pytest import fixture, raises as pytest_raises
from sys import path as sys_path

from pybuilder.core import Project
from pybuilder.errors import BuildFailedException
from pybuilder.reactor import Reactor
from test_utils import Mock
from pybuilder_pytest import initialize_pytest_plugin, run_unit_tests


@fixture
def test_project(build_project_path):
    project = Project(build_project_path)
    project.set_property('dir_source_main_python', 'src/main/python')
    initialize_pytest_plugin(project)
    return project


def test_should_set_dependency():
    mock_project = Mock(Project)
    initialize_pytest_plugin(mock_project)
    mock_project.plugin_depends_on.assert_called_with('pytest')


def test_should_set_default_properties(test_project):
    initialize_pytest_plugin(test_project)
    expected_default_properties = {
            "dir_source_pytest_python": "src/unittest/python"
            }
    for property_name, property_value in expected_default_properties.items():
        assert test_project.get_property(property_name) == property_value


def test_should_leave_user_specified_properties_when_initializing_plugin(test_project):
    expected_properties = {
        "dir_source_pytest_python": "some/path"
        }
    for property_name, property_value in expected_properties.items():
        test_project.set_property(property_name, property_value)

    initialize_pytest_plugin(test_project)

    for property_name, property_value in expected_properties.items():
        assert test_project.get_property(property_name) == property_value


def test_should_run_pytest_tests(test_project, capsys):
    test_project.set_property('dir_source_pytest_python',
                              'src/unittest/resources/pytest_base_success')
    test_project.set_property('verbose', True)
    run_unit_tests(test_project, Mock())
    out, err = capsys.readouterr()
    assert test_project.expand_path('$dir_source_main_python') in sys_path
    assert test_project.expand_path('$dir_source_pytest_python') in sys_path


def test_should_run_pytest_tests_with_verbose(test_project, capsys):
    test_project.set_property('dir_source_pytest_python',
                              'src/unittest/resources/pytest_base_success')
    test_project.set_property('verbose', True)
    run_unit_tests(test_project, Mock())
    out, err = capsys.readouterr()
    assert 'test_success.py::test_pytest_base_success' in out
    assert test_project.expand_path('$dir_source_main_python') in sys_path
    assert test_project.expand_path('$dir_source_pytest_python') in sys_path


def test_should_correct_get_pytest_failure(test_project, capsys):
    test_project.set_property('dir_source_pytest_python',
                              'src/unittest/resources/pytest_base_failure')

    with pytest_raises(BuildFailedException):
        run_unit_tests(test_project, Mock())
    out, err = capsys.readouterr()
