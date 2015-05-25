from mock import patch
from unittest import TestCase
import yaml

from wharfrat.wharf_rat import WharfRat


class TestTranslate(TestCase):

    @patch('wharfrat.wharf_rat.Container')
    def test_create_containers(self, mock_container):
        data = yaml.load('''
        test-instance:
            type: instance
        ''')
        rat = WharfRat(data)
        mock_container.assert_called_once()

    @patch('wharfrat.wharf_rat.Task')
    def test_create_task(self, mock_task):
        data = yaml.load('''
        test-task:
            type: task
            images:
                - test-instance
                - test-instance2
        ''')
        rat = WharfRat(data)
        mock_task.assert_called_once()
