from unittest import TestCase

# You don't need to worry about this yet.
class PublicTestSuite(TestCase):

    def test_x_is_number(self):
        import script
        x = script.x
        assert(isinstance(x, (int, float)))

