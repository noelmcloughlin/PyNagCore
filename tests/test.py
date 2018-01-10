from unittest import TestCase

from nagioscore import cmd

class Test(TestCase):
    def test_is_string(self):
        s = funniest.joke()
        self.assertTrue(isinstance(s, basestring))
