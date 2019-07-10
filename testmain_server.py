import unittest
import asyncio
import main_server


class TestValidateString(unittest.TestCase):
    def test_valid_string_valid(self):
        asyncio.run(main_server.validate_string("[[1, 1, 1], [1, 1, 1], [1, 1, 1]]"))
        for vals in main_server.get_colors():
            self.assertEqual(vals, 1)


if __name__ == '__main__':
    unittest.main()