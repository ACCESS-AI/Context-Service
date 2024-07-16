from unittest import TestCase

from task import script

class PublicTestSuite(TestCase):

    def test_1234(self):
        import os.path
        self.assertTrue(os.path.isfile("ball.png"))

