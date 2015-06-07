from unittest import TestCase
from subprocess import CalledProcessError

from wharfrat import interface

class TestInterface(TestCase):
    # System test for the external interface

    def test_issue_command_print_result(self):

        command = 'echo hello'
        output = interface.issue(command)

        self.assertEqual(output, 'hello\n')

    def test_print_stderr(self):

        command = 'echo "error" >&2'
        output = interface.issue(command)

        self.assertEqual(output, 'error\n')

    def test_raises_on_err(self):
        with self.assertRaises(CalledProcessError) as e:

            command = 'echo "FAIL"; exit 1'
            interface.issue(command)

        self.assertEqual(e.exception.returncode, 1)
        self.assertEqual(e.exception.output, 'FAIL\n')
