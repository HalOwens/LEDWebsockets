import unittest
import asyncio
import main_server


class TestValidateString(unittest.TestCase):
    def test_validate_string_valid(self):
        asyncio.run(main_server.validate_string("[[1, 1, 1], [1, 1, 1], [1, 1, 1]]"))
        for vals in main_server.get_colors():
            self.assertEqual(vals, 1)

    def test_validate_string_invalid(self):
        asyncio.run(main_server.validate_string("this string should not work"))
        vals = main_server.get_colors()
        self.assertEqual(vals.__next__(), 255)
        self.assertEqual(vals.__next__(), 0)
        self.assertEqual(vals.__next__(), 0)
        self.assertEqual(vals.__next__(), 255)
        self.assertEqual(vals.__next__(), 0)
        self.assertEqual(vals.__next__(), 0)
        self.assertEqual(vals.__next__(), 255)
        self.assertEqual(vals.__next__(), 0)
        self.assertEqual(vals.__next__(), 0)

if __name__ == '__main__':
    unittest.main()