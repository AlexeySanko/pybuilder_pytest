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

from os.path import join as path_join, isfile

from pytest import main as pytest_main
from sys import path as sys_path

from pybuilder.core import task, init, use_plugin
from pybuilder.errors import BuildFailedException

__author__ = 'Alexey Sanko'

use_plugin("python.core")


DEFAULT_PYTEST_PYTHON_MODULE_GLOBS = ["test_*", "*_test.py"]
DEFAULT_PYTEST_FUNCTIONS_N_METHOD_GLOBS = ["test_*"]
DEFAULT_PYTEST_CLASS_GLOBS = ["Test*"]

pytest_ini_template = """
[pytest]
python_files={python_files}
python_classes={python_classes}
python_functions={python_functions}
"""


@init
def initialize_pytest_plugin(project):
    """ Init default plugin project properties. """
    project.plugin_depends_on('pytest')
    project.set_property_if_unset('dir_source_pytest_python', "src/unittest/python")
    project.set_property_if_unset('pytest_extra_args', [])
    project.set_property_if_unset('pytest_python_module_globs', list(DEFAULT_PYTEST_PYTHON_MODULE_GLOBS))
    project.set_property_if_unset('pytest_function_n_method_globs', list(DEFAULT_PYTEST_FUNCTIONS_N_METHOD_GLOBS))
    project.set_property_if_unset('pytest_class_globs', list(DEFAULT_PYTEST_CLASS_GLOBS))


@task
def run_unit_tests(project, logger):
    """ Call pytest for the sources of the given project. """
    logger.info("pytest: Run unittests.")
    # Add test and source folders to syspath
    from pybuilder.plugins.python.unittest_plugin \
        import _register_test_and_source_path_and_return_test_dir \
        as push_test_path_to_syspath
    test_dir = push_test_path_to_syspath(project, sys_path, 'pytest')
    # Pass module/class/function/method globs to pytest.ini if any glob was changed
    if any([
        sorted(project.get_property('pytest_python_module_globs')) != sorted(DEFAULT_PYTEST_PYTHON_MODULE_GLOBS),
        sorted(project.get_property('pytest_function_n_method_globs')) != sorted(
                    DEFAULT_PYTEST_FUNCTIONS_N_METHOD_GLOBS),
        sorted(project.get_property('pytest_class_globs')) != sorted(DEFAULT_PYTEST_CLASS_GLOBS)
        ]
    ):
        pytest_ini = path_join(test_dir, 'pytest.ini')
        if isfile(pytest_ini):
            raise BuildFailedException(
                "File pytest.ini was found into test folder: {dir}. "
                "Please provide manually parameter(s) python_files/python_classes/python_functions "
                "into section [pytest] there and remove corresponding project properties.".format(dir=test_dir))
        f = open(pytest_ini, 'w')
        content = pytest_ini_template.format(
            python_files=' '.join(project.get_property('pytest_python_module_globs')),
            python_classes=' '.join(project.get_property('pytest_class_globs')),
            python_functions=' '.join(project.get_property('pytest_function_n_method_globs'))
        )
        f.write(content)
        f.flush()
        f.close()
    print "$$$$$$$$$$$$$$$$$$: " + test_dir
    from os import walk
    f = []
    for (dirpath, dirnames, filenames) in walk(test_dir):
        f.extend(filenames)
        break
    print f
    f = open(path_join(test_dir, 'pytest.ini'), 'r')
    for line in f:
        print line,
    print "$$$$$$$$$$$$$$$$$$"
    try:
        pytest_args = [test_dir] + project.get_property('pytest_extra_args')
        if project.get_property('verbose'):
            pytest_args.append('-s')
            pytest_args.append('-v')
        ret = pytest_main(pytest_args)
        if ret:
            raise BuildFailedException("pytest: unittests failed")
        else:
            logger.info("pytest: All unittests passed.")
    except:
        raise
