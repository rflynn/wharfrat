from tests.helper import TestHelper
from subprocess import check_output
import yaml

from wharfrat.command import read_file, create_parser, get_command
from wharfrat.wharf_rat import WharfRat

class TestCommands(TestHelper):

    def test_binary(self):

        response = check_output('./wharf-rat --help'.split())
        self.assertIn('wharf-rat', response)

    def test_reads_file(self):
        with open('wharf-rat.yml', 'w') as f:
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

        response = read_file(args)
        with open('wharf-rat.yml', 'r') as f:
            self.assertEqual(yaml.load(f), response)

    def test_alternate_file(self):
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

        response = read_file(args)
        with open('filename.yml', 'r') as f:
            self.assertEqual(yaml.load(f), response)

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
