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
        self.project = Project("basedir")
        self.mock_logger = Mock()
        self.project.set_property('dir_source_main_python', 'src')

    def test_should_set_dependency(self):
        initialize_pytest_plugin(self.project)
        run_unit_tests(self.project, self.mock_logger)
