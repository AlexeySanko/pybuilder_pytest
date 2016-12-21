PyBuilder Pytest Plugin [![Build Status](https://travis-ci.org/AlexeySanko/pybuilder_pytest.svg?branch=master)](https://travis-ci.org/AlexeySanko/pybuilder_pytest)
=======================

Use pytest Python module for running unittests

How to use pybuilder_pytest
----------------------------------

Add plugin dependency to your `build.py`
```python
use_plugin('pypi:pybuilder_pytest')
```

Configure the plugin within your `init` function:
```python
@init
def init(project):
    # directory with unittest modules
    project.set_property("dir_source_pytest_python", "src/unittest/python")
    # extra arguments which will be passed to pytest
    project.get_property("pytest_extra_args").append("-x")
    # globs which define files with unittests
    project.get_property("pytest_python_module_globs").append("*_check.py")
    # globs which define classes with unittests
    project.get_property("pytest_class_globs").append("Check*")
    # globs which define unittests functions and methods
    project.get_property("pytest_function_n_method_globs").append("check_*")
```

This will break the build if any unittest failed.