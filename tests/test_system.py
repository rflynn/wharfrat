from unittest import TestCase, skip
from subprocess import check_output

class TestSystem(TestCase):

    @skip
    def test_start_task(self):

        # The system will have a command line interface and a config file
        # The user will issue commands from the directory with the file
        # in it

        # Ryan wants to fire up his development environment.  First,
        # he creates a wharfrat.yml file with his task definition

        with open('wharfrat.yml', 'w') as f:
            f.write('''
                front:
                    type: instance
                    image: busybox
                    environment:
                        - VAR=test
                        - VAR2=other
                back:
                    type: instance
                    image: busybox
                    links:
                        - test-instance
                basic:
                    type: task
                    images:
                        - front
                        - back
            ''')

        # He changes to
        # the directory with his wharf.yml file and runs wharfrat dev run

        output = check_output('./wharf-rat dev run', shell=True)

        # He sees from this output that a front and a back container were
        # started

        self.assertIn('container basic-front started', output)
        self.assertIn('container basic-back started', output)

        # He wonders whether the correct image was used, environment
        # variables set, and links properly established.
        # He runs wharfrat dev inspect and looks at the output

        output = check_output('./wharf-rat dev inspect', shell=True)

        self.assertIn('basic.', output)
        self.assertIn('container basic-back started', output)
