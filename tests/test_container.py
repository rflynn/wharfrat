from mock import MagicMock, patch
from unittest import TestCase
import yaml

from wharfrat.container import Container, TaskContainer


class TestContainer(TestCase):

    def test_container_image(self):
        data = yaml.load('''
        test-instance:
            type: instance
            image: this/image
        ''')

        con = Container('test-instance', data['test-instance'])
        command = con.get_run_command('test-task')
        expected = 'this/image'
        self.assertTrue(command.endswith(expected))

    def test_set_env_variable(self):
        data = yaml.load('''
        test-instance:
            type: instance
            image: this/image
            environment:
                - VAR=test
                - VAR2=other
        ''')

        con = Container('test-instance', data['test-instance'])
        command = con.get_run_command('test-task')
        expected = '-e VAR=test -e VAR2=other'
        self.assertIn(expected, command)

    def test_set_command(self):
        data = yaml.load('''
        test-instance:
            type: instance
            image: this/image
            command: fake command
        ''')

        container = Container('test-instance', data['test-instance'])
        command = container.get_run_command('test-task')
        expected = 'fake command'
        self.assertTrue(command.endswith(expected))

    def test_link_container(self):
        data = yaml.load('''
        test-instance:
            type: instance
            image: this/image
            links:
                - test-instance2:test-instance2
        ''')

        container = Container('test-instance', data['test-instance'])
        command = container.get_run_command('test-task')
        expected = ' --link test-task-test-instance2:test-instance2'
        self.assertIn(expected, command)

    def test_auto_remove_container(self):
        data = yaml.load('''
        test-instance:
            type: instance
            image: this/image
        ''')

        con = Container('test-instance', data['test-instance'])
        fake_task = MagicMock()
        fake_task.name = 'the_task'
        tc = TaskContainer(con, fake_task, remove=True)
        command = tc.get_run_command()
        self.assertIn('--rm', command)
        self.assertNotIn('-d', command)

    def test_daemonize_container(self):
        data = yaml.load('''
        test-instance:
            type: instance
            image: this/image
        ''')

        con = Container('test-instance', data['test-instance'])
        fake_task = MagicMock()
        fake_task.name = 'the_task'
        tc = TaskContainer(con, fake_task)
        command = tc.get_run_command()
        self.assertIn('-d', command)
        self.assertNotIn('--rm', command)

    def test_cleanup_daemonized_container(self):
        data = yaml.load('''
        test-instance:
            type: instance
            image: this/image
        ''')

        con = Container('test-instance', data['test-instance'])
        fake_task = MagicMock()
        fake_task.name = 'the_task'
        tc = TaskContainer(con, fake_task)
        command = tc.get_cleanup_command()
        self.assertEqual('docker rm -fv the_task-test-instance', command)

    def test_specify_volume(self):
        data = yaml.load('''
        test-instance:
            type: instance
            image: this/image
            volumes:
              - /root:/root
        ''')

        container = Container('test-instance', data['test-instance'])
        command = container.get_run_command('test-task')
        expected = ' -v /root:/root'
        self.assertIn(expected, command)

    @patch('wharfrat.DIRECTORY', '/root')
    def test_relative_volume(self):
        data = yaml.load('''
        test-instance:
            type: instance
            image: this/image
            volumes:
              - a/directory:/data
        ''')

        container = Container('test-instance', data['test-instance'])
        command = container.get_run_command('test-task')
        expected = ' -v /root/a/directory:/data'
        self.assertIn(expected, command)

    def test_volumes_from(self):
        data = yaml.load('''
        test-instance:
            type: instance
            image: this/image
            volumes-from:
              - another-instance
        ''')
        container = Container('test-instance', data['test-instance'])
        command = container.get_run_command('test-task')
        expected = ' --volumes-from another-instance'
        self.assertIn(expected, command)

    def test_ports(self):
        data = yaml.load('''
        test-instance:
            type: instance
            image: this/image
            ports:
              - "80:80"
        ''')

        container = Container('test-instance', data['test-instance'])
        command = container.get_run_command('test-task')
        expected = ' -p 80:80'
        self.assertIn(expected, command)

    def test_set_entrypoint(self):
        data = yaml.load('''
        test-instance:
            type: instance
            image: this/image
            entrypoint: bash
        ''')

        container = Container('test-instance', data['test-instance'])
        command = container.get_run_command('test-task')
        expected = '--entrypoint bash'
        self.assertIn(expected, command)

    def test_build_command(self):
        data = yaml.load('''
        test-instance:
            type: instance
            build: /a/directory
        ''')

        container = Container('test-instance', data['test-instance'])
        command = container.get_setup_command('test-task')
        expected = 'docker build -t test-task/test-instance /a/directory'
        self.assertEqual(expected, command)

    @patch('wharfrat.DIRECTORY', '/root')
    def test_relative_build_command(self):
        data = yaml.load('''
        test-instance:
            type: instance
            build: a/directory
        ''')

        container = Container('test-instance', data['test-instance'])
        command = container.get_setup_command('test-task')
        expected = 'docker build -t test-task/test-instance /root/a/directory'
        self.assertEqual(expected, command)
