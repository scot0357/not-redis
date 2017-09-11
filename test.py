import unittest
import command


class TestSet(unittest.TestCase):

    def test_set_string(self):
        c = command.exec_command("set x 'i was here'")
        self.assertEqual(c, "OK")


class TestExists(unittest.TestCase):

    def setUp(self):
        command.NAMESPACE['__SINGLE'] = {}

    def test_exists_none(self):
        c = command.exec_command("exists x")
        self.assertEqual(c, "(integer) 0")

    def test_exists_one(self):
        command.NAMESPACE['__SINGLE']['x'] = True
        c = command.exec_command("exists x")
        self.assertEqual(c, "(integer) 1")


if __name__ == "__main__":
    unittest.main()
