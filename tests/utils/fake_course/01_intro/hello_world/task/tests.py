import sys
from unittest import TestCase

class PublicTests(TestCase):

    def test_import_does_not_crash(self):
        from task import script

