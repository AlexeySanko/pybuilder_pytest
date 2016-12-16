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

from sys import path as sys_path

from pybuilder.core import Author, init, use_plugin, task

use_plugin("python.core")
use_plugin("python.install_dependencies")
use_plugin("python.flake8")
use_plugin("python.coverage")
use_plugin("python.distutils")


name = "pybuilder-pytest"
version = '0.1.0'
authors = [Author('Alexey Sanko', 'alexeycount@gmail.com')]
url = 'https://github.com/AlexeySanko/pybuilder_pytest'
description = 'Please visit {0} for more information!'.format(url)
license = 'Apache License, Version 2.0'
summary = 'PyBuilder Pytest Plugin'

default_task = ['clean', 'analyze', 'publish']


@init
def set_properties(project):
    # dependencies
    project.depends_on('pytest')

    # coverage
    project.set_property('coverage_break_build', False)

    # flake8
    project.set_property('flake8_verbose_output', True)
    project.set_property('flake8_break_build', True)

    # distutils
    project.set_property('distutils_classifiers', [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'])


# "Eating your own dog food"
@task
def run_unit_tests(project, logger):
    import imp
    module_found = imp.find_module('pybuilder_pytest', [project.expand_path('$dir_source_main_python')])
    pybuilder_pytest = imp.load_module('pybuilder_pytest', *module_found)

    from pybuilder_pytest import call_pytest, initialize_pytest_plugin
    initialize_pytest_plugin(project)
    call_pytest(project, logger, ['--build-project-path', project.get_property('basedir')])
