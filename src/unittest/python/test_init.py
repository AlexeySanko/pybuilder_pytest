import os
from sys import path as sys_path

from pybuilder.core import Project
from pytest import fixture

sys_path.insert(0, '/media/sf_Ubuntu-01/AlexeySanko/pybuilder_pytest/src/main/python')
from test_utils import Mock
from pybuilder_pytest import initialize_pytest_plugin


@fixture
# test_project???
def project():
    test_dir = os.path.dirname(os.path.abspath(__file__))
    project = Project(test_dir)
    project.set_property('dir_source_main_python', 'resources')
    initialize_pytest_plugin(project)
    return project


def test_should_set_dependency():
    mock_project = Mock(Project)
    initialize_pytest_plugin(mock_project)
    mock_project.plugin_depends_on.assert_called_with('pytest')


# expected_properties = {
#         "dir_source_pytest_python": "src/unittest/python"
#         }

def test_should_leave_user_specified_properties_when_initializing_plugin(project):
    expected_properties = {
        "dir_source_pytest_python": "some/path"
        }
    for property_name, property_value in expected_properties.items():
        project.set_property(property_name, property_value)

    initialize_pytest_plugin(project)

    for property_name, property_value in expected_properties.items():
        assert project.get_property(property_name) == property_value


# class PytestPluginRunUnitTestsTests(TestCase):
#     def setUp(self):
#         self.mock_logger = Mock()
#         test_dir = os.path.dirname(os.path.abspath(__file__))
#         self.project = Project(test_dir)
#         self.project.set_property('dir_source_main_python', 'resources')
#         initialize_pytest_plugin(self.project)
#
#     def test_should_run_pytest_tests(self):
#         self.project.set_property('dir_source_pytest_python',
#                                   os.path.join(self.project.expand('$dir_source_main_python'), 'pytest_base_success'))
#         run_unit_tests(self.project, Mock())
#         self.assertTrue(self.project.expand_path('$dir_source_main_python') in sys_path)
#         self.assertTrue(self.project.expand_path('$dir_source_pytest_python') in sys_path)
