#!/usr/bin/env python3
import sys
try: from universal.harness import *
except: sys.path.append("../../universal/"); from harness import *

implementation = grading_import("task", "script")

class GradingTests(AccessTestCase):

    def is_friendly_pair(self, num1, num2):
        self.reject_template(implementation.is_friendly_pair)
        try:
            return implementation.is_friendly_pair(num1, num2)
        except Exception as e:
            if type(e) == TypeError:
                message = ("For the given numbers {}, {} {} is raised. Maybe you forgot to "
                "check if the given numbers are integers.").format(num1, num2, type(e).__name__)
            else :
                message = "For the given numbers {}, {} {} is raised.".format(num1, num2, type(e).__name__)
            self.hint(message)
            raise type(e)(message)


    def assert_friendly(self, num1, num2):
        actual = self.is_friendly_pair(num1, num2)
        expected = True
        if actual == False:
            message = "{} and {} are wrongly detected as not friendly pair even though they are.".format(num1, num2)
        else :
            message = "For the numbers {} and {} the function should return {}, but it returns {}.".format(num1, num2, repr(expected), actual)
        self.hint(message)
        self.assertTrue(actual == True)

    def assert_not_friendly(self, num1, num2):
        actual = self.is_friendly_pair(num1, num2) 
        expected = False
        if actual == True:
            message = "{} and {} are wrongly detected as friendly pair even though they are not.".format(num1, num2, expected, actual)
        else :
            message = "For the numbers {} and {} the function should return {}, but it returns {}.".format(num1, num2, repr(expected), actual)
        self.hint(message)
        self.assertTrue(actual == False)

    def assert_invalid(self, num1, num2):
        actual = self.is_friendly_pair(num1, num2)
        expected = "Invalid"
        self.hint("For the numbers {} and {} the function should return {} but it returns {}.".format(num1, num2, repr(expected), actual))
        self.assertEqual(actual, expected)

    def assert_valid(self, num1, num2):
        actual = self.is_friendly_pair(num1, num2)
        notExpected = "Invalid"
        self.hint("For the numbers {} and {} received {} even though they are valid numbers . \
        To be valid they must be different natural numbers.".format(num1, num2, actual))
        self.assertNotEqual(actual, notExpected)

    def test_simple_friendly_pair(self):
        num1 = 6
        num2 = 28 
        self.assert_friendly(num1, num2)

    def test_medium_friendly_pair(self):
        num1 = 4320
        num2 = 4680  
        self.assert_friendly(num1, num2)

    def test_hard_friendly_pair(self):
        num1 = 24
        num2 = 91963648
        self.assert_friendly(num1, num2)

    def test_simple_not_friendly_pair(self):
        num1 = 2
        num2 = 5
        self.assert_not_friendly(num1, num2)

    def test_hard_not_friendly_pair(self):
        num1 = 14326
        num2 = 4999
        self.assert_not_friendly(num1, num2)

    def test_invalid_sameNumbers(self):
        num1 = 20
        num2 = 20
        self.assert_invalid(num1, num2)

    def test_invalid_negative_sameNumbers(self):
        num1 = -20
        num2 = -20
        self.assert_invalid(num1, num2)     

    def test_invalid_off_point_num1(self):
        num1 = 0.99
        num2 = 28 
        self.assert_invalid(num1, num2)

    def test_valid_on_point_num1(self):
        num1 = 1
        num2 = 28
        self.assert_valid(num1, num2)

    def test_invalid_off_point_num2(self):
        num1 = 6
        num2 = 0.99
        self.assert_invalid(num1, num2)

    def test_valid_on_point_num2(self):
        num1 = 28
        num2 = 1
        self.assert_valid(num1, num2)

    def test_valid_out_point_num1(self):
        num1 = 28
        num2 = 2 
        self.assert_valid(num1, num2)

    def test_invalid_float_num1(self):
        num1 = 2.6
        num2 = 28
        self.assert_invalid(num1, num2)

    def test_invalid_float_num2(self):
        num1 = 28
        num2 = 2.6
        self.assert_invalid(num1, num2)

    def test_invalid_float_num1_num2(self):
        num1 = 6.1
        num2 = 7.1
        self.assert_invalid(num1, num2)

TestRunner().run(AccessTestSuite(2, [GradingTests]))

