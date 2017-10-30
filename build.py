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
use_plugin("python.frosted")
use_plugin("python.coverage")
use_plugin("python.distutils")
use_plugin("python.unittest")
use_plugin('pypi:pybuilder_semver_git_tag')


name = "pybuilder-pytest"
authors = [Author('Alexey Sanko', 'alexeycount@gmail.com')]
url = 'https://github.com/AlexeySanko/pybuilder_pytest'
description = 'Please visit {0} for more information!'.format(url)
license = 'Apache License, Version 2.0'
summary = 'PyBuilder Pytest Plugin'

default_task = ['clean', 'analyze', 'publish']


@init
def set_properties(project):
    # dependencies
    project.build_depends_on('mock')
    project.depends_on('pytest')

    # coverage
    project.set_property('coverage_break_build', False)

    # flake8
    project.set_property('flake8_verbose_output', True)
    project.set_property('flake8_break_build', True)

    # frosted
    project.set_property("frosted_break_build", True)
    project.set_property("frosted_include_test_sources", True)

    # distutils
    project.set_property('distutils_commands', ['bdist', 'bdist_wheel'])
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
