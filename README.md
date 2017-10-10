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
```

This will break the build if any unittest failed.

Coverage measure
----------------------------------

For coverage measure is recommended to use pytest plugins.
For example, `pytest-cov`.

```python
from pybuilder.utils import discover_modules

@init
def set_properties(project, logger):
    project.build_depends_on('pytest-cov')
    
    for module_name in discover_modules(project.expand_path("$dir_source_main_python")):
        project.get_property("pytest_extra_args").append("--cov=" + module_name)
    project.get_property("pytest_extra_args").append("--cov-report=term-missing")
```

If You need to pass result to file You can use 
```python
project.get_property("pytest_extra_args").append("--cov-report=xml:target/reports/pytest_coverage.xml")
```

If You use `pytest-cov` do not forget to disable PyBuilder `coverage` plugin, 
for avoiding unexpected results or exception:

~~use_plugin("python.coverage")~~