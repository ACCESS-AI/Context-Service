from unittest import TestCase

from task import script

class PublicTestSuite(TestCase):

    def test_1234(self):
        actual = script.calculate(1,2,3,4)
        expected = 1.44444
        self.assertAlmostEqual(expected, actual, 5)

