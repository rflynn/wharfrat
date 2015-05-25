from mock import MagicMock, patch
from unittest import TestCase
import yaml

from wharfrat.task import Task


class TestTask(TestCase):

    def test_multiple_instance_task(self):
        data = yaml.load('''
        test-task:
            type: task
            primary: test-instance
            images:
                - test-instance2
        ''')
        fake = MagicMock()
        fake.get_run_command.return_value = 'working'
        fake.get_cleanup_command.return_value = 'cleaning'
        containers = {
            'test-instance': fake,
            'test-instance2': fake
        }

        task = Task('test-task', data['test-task'], containers)
        commands = task.run()
        expected = ['working', 'working', 'cleaning']
        self.assertEqual(expected, commands[-3:])

    @patch('wharfrat.task.TaskContainer')
    def test_primary_container_created_with_rm(self, mock_container):
        data = yaml.load('''
        test-task:
            type: task
            primary: test-instance
        ''')

        fake = MagicMock()
        containers = {
            'test-instance': fake
        }
        Task('test-task', data['test-task'], containers)
        args, kwargs = mock_container.call_args

        self.assertTrue(kwargs['remove'])

    @patch('wharfrat.task.TaskContainer')
    def test_other_container_created_without_rm(self, mock_container):
        data = yaml.load('''
        test-task:
            type: task
            images:
              - test-instance
        ''')

        fake = MagicMock()
        containers = {
            'test-instance': fake
        }
        Task('test-task', data['test-task'], containers)
        args, kwargs = mock_container.call_args

        self.assertFalse(kwargs.get('remove'))

    def test_build_container_uses_setup_commands(self):
        data = yaml.load('''
        test-task:
            type: task
            images:
              - test-instance
        ''')

        fake = MagicMock()
        fake.build = "/root"
        fake.get_setup_command.return_value = "setup"
        fake.get_run_command.return_value = "run"
        fake.get_cleanup_command.return_value = "cleanup"
        containers = {
            'test-instance': fake
        }
        task = Task('test-task', data['test-task'], containers)
        commands = task.run()
        self.assertIn('setup', commands)
