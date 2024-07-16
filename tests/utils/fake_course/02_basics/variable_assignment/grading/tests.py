#!/usr/bin/env python3

# Scaffolding necessary to set up ACCESS test
import sys
try: from universal.harness import *
except: sys.path.append("../../universal/"); from harness import *

# Grading test suite starts here
import inspect

# Instead of doing the usual
# import task.script as implementation
# use grading_import which will take care of catching and reporting import errors
implementation = grading_import("task", "script")

class GradingTests(AccessTestCase):

    def test_x_is_42(self):
        self.hint("x is not 42")
        self.assertEqual(implementation.x, 42)

    def test_x_is_not_literally_42(self):
        self.test_x_is_42()
        self.hint("The solution seems to contain x = 42, please assign something slighty more complex")
        source = inspect.getsource(implementation)
        self.assertTrue("x=42" not in ''.join(source.split()))

TestRunner().run(AccessTestSuite(2, [GradingTests]))

