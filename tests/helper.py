import os
from unittest import TestCase


class TestHelper(TestCase):

    def tearDown(self):
        if os.path.exists('wharf-rat.yml'):
            os.remove('wharf-rat.yml')
        if os.path.exists('filename.yml'):
            os.remove('filename.yml')
