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
""" PyBuilder plugin which provides work with PyTest tool"""
import os.path
from sys import path as sys_path

import pytest
from pybuilder.core import task, init, use_plugin
from pybuilder.errors import BuildFailedException
from pybuilder.plugins.python.test_plugin_helper import ReportsProcessor
from pybuilder.plugins.python.unittest_plugin \
        import _register_test_and_source_path_and_return_test_dir \
        as push_test_path_to_syspath
from pybuilder.utils import Timer

from pybuilder_pytest import version

__author__ = 'Alexey Sanko'
__version__ = version.__version__

use_plugin("python.core")


@init
def initialize_pytest_plugin(project):
    """ Init default plugin project properties. """
    project.plugin_depends_on('pytest')
    project.set_property_if_unset("dir_source_pytest_python",
                                  "src/unittest/python")
    project.set_property_if_unset("pytest_extra_args", [])

    project.set_property_if_unset("dir_source_pytest_integration_python",
                                  "src/integrationtest/python")
    project.set_property_if_unset("pytest_integration_extra_args", [])


@task
def run_unit_tests(project, logger):
    """ Call pytest for the sources of the given project. """
    logger.info('pytest: Run unittests.')
    test_dir = push_test_path_to_syspath(project, sys_path, 'pytest')
    extra_args = [project.expand(prop)
                  for prop in project.get_property("pytest_extra_args")]
    try:
        pytest_args = [test_dir] + (extra_args if extra_args else [])
        if project.get_property('verbose'):
            pytest_args.append('-s')
            pytest_args.append('-v')
        ret = pytest.main(pytest_args)
        if ret:
            raise BuildFailedException('pytest: unittests failed')
        else:
            logger.info('pytest: All unittests passed.')
    except Exception:
        raise


@task
def run_integration_tests(project, logger, reactor):
    """ Call pytest for the sources of the given project. """
    logger.info('pytest: Run integrationtests.')
    test_dir = push_test_path_to_syspath(
        project, sys_path, 'pytest_integration'
    )
    if not os.path.exists(test_dir):
        logger.warn(f"pytest: No integration tests found in {test_dir}, skipping")
        return
    # reports_dir = prepare_reports_directory(project)
    extra_args = [
        project.expand(prop)
        for prop in project.get_property("pytest_integration_extra_args")
    ]

    reports = []
    total_time = Timer.start()
    try:
        if project.get_property("integrationtest_parallel"):
            logger.warn("Parallel integration test execution is disabled")
            # reports, total_time = run_integration_tests_in_parallel(
            #     project, logger, reactor, test_dir, extra_args
            # )
        # else:
        reports, total_time = run_integration_tests_sequentially(
            project, logger, reactor, test_dir, extra_args
        )
    except Exception:
        total_time.stop()
        raise
    finally:
        reports_processor = ReportsProcessor(project, logger)
        reports_processor.process_reports(reports, total_time)
        reports_processor.report_to_ci_server(project)
        reports_processor.write_report_and_ensure_all_tests_passed()


def run_integration_tests_sequentially(
    project, logger, reactor, test_dir, extra_args
):
    logger.debug("Running integration tests sequentially")

    report_items = []
    total_time = Timer.start()

    pytest_args = [test_dir] + (extra_args if extra_args else [])
    if project.get_property('verbose'):
        pytest_args.append('-s')
        pytest_args.append('-v')
    try:
        ret = pytest.main(pytest_args)
        if ret:
            raise BuildFailedException('pytest: integrationtests failed')
        else:
            logger.info('pytest: All integrationtests passed.')
    except Exception:
        raise
    finally:
        total_time.stop()

    report_items.append({
        "test": "All integration tests",
        "test_file": test_dir,
        "time": total_time.get_millis(),
        "success": True
    })

    return report_items, total_time


def run_integration_tests_in_parallel(
    project, logger, reactor, test_dir, extra_args
):
    pass
