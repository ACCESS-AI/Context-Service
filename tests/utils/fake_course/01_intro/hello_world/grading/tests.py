#!/usr/bin/env python3

# Scaffolding necessary to set up ACCESS test
import sys
try: from universal.harness import *
except: sys.path.append("../../universal/"); from harness import *

# Grading test suite starts here
from io import StringIO

class GradingTests(AccessTestCase):
    """This particular test case is a bit special, because we need to capture
       output that happens during the solution import. The import only happens
       once, so we capture the output and read it in the test methods."""
    output = None

    def import_script(self):
        if GradingTests.output == None:
            capture = StringIO()
            sys.stdout = capture
            implementation = grading_import("task", "script")
            sys.stdout = sys.__stdout__
            GradingTests.output = capture.getvalue()

    @weight(0)
    def test_prints_something(self):
        self.import_script()
        self.hint("The script does not produce any output. Are you printing something?")
        self.assertGreater(len(GradingTests.output), 0)

    def test_prints_hello_world(self):
        self.import_script()
        self.hint("The output is not 'Hello, World!'")
        self.assertEqual(GradingTests.output, "Hello, World!\n")

TestRunner().run(AccessTestSuite(1, [GradingTests]))
