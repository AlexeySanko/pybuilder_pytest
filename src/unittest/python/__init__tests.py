import os
from sys import path as sys_path

from unittest import TestCase
from pybuilder.core import Project
from test_utils import Mock
from pybuilder_pytest import initialize_pytest_plugin, run_unit_tests


class PytestPluginInitializationTests(TestCase):
    def setUp(self):
        self.project = Project("basedir")

    def test_should_set_dependency(self):
        mock_project = Mock(Project)
        initialize_pytest_plugin(mock_project)
        mock_project.plugin_depends_on.assert_called_with('pytest')

    def test_should_leave_user_specified_properties_when_initializing_plugin(self):

        expected_properties = {
            "dir_source_pytest_python": "src/unittest/python"
            }
        for property_name, property_value in expected_properties.items():
            self.project.set_property(property_name, property_value)

            initialize_pytest_plugin(self.project)

        for property_name, property_value in expected_properties.items():
            self.assertEquals(
                self.project.get_property(property_name), property_value)


class PytestPluginRunUnitTestsTests(TestCase):
    def setUp(self):
        self.mock_logger = Mock()
        test_dir = os.path.dirname(os.path.abspath(__file__))
        self.project = Project(test_dir)
        self.project.set_property('dir_source_main_python', 'resources')
        initialize_pytest_plugin(self.project)

    def test_should_run_pytest_tests(self):
        self.project.set_property('dir_source_pytest_python',
                                  os.path.join(self.project.expand('$dir_source_main_python'), 'pytest_base_success'))
        run_unit_tests(self.project, self.mock_logger)
        self.assertTrue(self.project.expand_path('$dir_source_main_python') in sys_path)
        self.assertTrue(self.project.expand_path('$dir_source_pytest_python') in sys_path)
