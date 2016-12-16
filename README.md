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
    # pytest
    project.set_property("dir_source_pytest_python", "src/unittest/python")
```

This will break the build if any unittest failed.