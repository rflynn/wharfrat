from mock import patch
from tests.helper import TestHelper
import yaml

from wharfrat.command import create_parser, get_command
from wharfrat.wharf_rat import WharfRat


class TestCommands(TestHelper):

    @patch('wharfrat.wharf_rat.WharfRat._load')
    def test_reads_file(self, mock_load):
        with open('wharfrat.yml', 'w') as f:
            f.write('''
                front:
                    type: instance
                    image: busybox
                basic:
                    type: task
                    images:
                        - front
                        - back
            ''')
        class args:
            filename = None

        WharfRat.build(args)
        mock_load.assert_called_with('wharfrat.yml')

    @patch('wharfrat.wharf_rat.WharfRat._load')
    def test_alternate_file(self, mock_load):
        with open('filename.yml', 'w') as f:
            f.write('''
                front:
                    type: instance
                    image: busybox
                basic:
                    type: task
                    images:
                        - front
                        - back
            ''')
        class args:
            filename = 'filename.yml'

        WharfRat.build(args)
        mock_load.assert_called_with('filename.yml')

    def test_filename_argument(self):
        args = ['-f', 'othername.yml', 'run', 'task']
        parser = create_parser()
        _args = parser.parse_args(args)
        self.assertEqual(_args.filename, 'othername.yml')

    def test_run_command(self):
        args = ['run', 'task']
        parser = create_parser()
        _args = parser.parse_args(args)
        self.assertEqual(_args.command, 'run')

    def test_task_command(self):
        args = ['run', 'task']
        parser = create_parser()
        _args = parser.parse_args(args)
        self.assertEqual(_args.task, 'task')

    def test_method_runner(self):
        class args:
            command = 'run'

        command = get_command(args)
        self.assertEqual(command, WharfRat.run)
