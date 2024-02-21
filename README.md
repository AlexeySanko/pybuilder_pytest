PyBuilder Pytest Plugin [![Build Status](https://travis-ci.org/AlexeySanko/pybuilder_pytest.svg?branch=master)](https://travis-ci.org/AlexeySanko/pybuilder_pytest)
=======================

Use `pytest` Python module for running unittests and/or integration tests. This module follows the naming convention of `pytest`: file names start with `test_` instead of ending with `_tests.py` as stated in the PyBuilder

How to use pybuilder_pytest
----------------------------------

Add plugin dependency to your `build.py`
```python
use_plugin('pypi:pybuilder_pytest')

@init
def init(project):
    project.get_property("pytest_extra_args").append("-x")
    project.get_property("pytest_integration_extra_args").append("-x")
```

This will break the build if any unittest/integrationtest failed.

Coverage measure
----------------------------------

For coverage measure is recommended to use [pybuilder_pytest_coverage](https://github.com/AlexeySanko/pybuilder_pytest_coverage)

Properties
----------

Plugin has next properties with provided defaults

| Name                                 | Type | Default Value              | Description |
|--------------------------------------| --- |----------------------------| --- |
| dir_source_pytest_python             | string | src/unittest/python        | Relative path to directory with unittest modules
| pytest_extra_args                    | list | `[]`                       | Extra arguments which will be passed to pytest |
| dir_source_pytest_integration_python | string | src/integrationtest/python | Relative path to directory with integrationtest modules
| pytest_integration_extra_args        | list | `[]`                       | Extra arguments which will be passed to pytest |
