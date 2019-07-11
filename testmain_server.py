import unittest
import asyncio
import main_server


class TestValidateString(unittest.TestCase):
    host = main_server.Server()

    def test_validate_string_valid(self):
        """Verifies that a correct string is mapped to the _vld variables"""
        asyncio.run(self.host.validate_string("[[1, 1, 1], [1, 1, 1], [1, 1, 1]]"))
        self.assertEqual(self.host.r1_vld, 1)
        self.assertEqual(self.host.g1_vld, 1)
        self.assertEqual(self.host.b1_vld, 1)
        self.assertEqual(self.host.r2_vld, 1)
        self.assertEqual(self.host.g2_vld, 1)
        self.assertEqual(self.host.b2_vld, 1)
        self.assertEqual(self.host.r3_vld, 1)
        self.assertEqual(self.host.g3_vld, 1)
        self.assertEqual(self.host.b3_vld, 1)

    def test_validate_string_invalid(self):
        """Makes sure that any strings that are invalid cause the _vld variables to show the error code"""
        asyncio.run(self.host.validate_string("[[1, 1, 1], ")) #"this string should not work"))
        self.assertEqual(self.host.r1_vld, 255)
        self.assertEqual(self.host.g1_vld, 0)
        self.assertEqual(self.host.b1_vld, 0)
        self.assertEqual(self.host.r2_vld, 255)
        self.assertEqual(self.host.g2_vld, 0)
        self.assertEqual(self.host.b2_vld, 0)
        self.assertEqual(self.host.r3_vld, 255)
        self.assertEqual(self.host.g3_vld, 0)
        self.assertEqual(self.host.b3_vld, 0)


if __name__ == '__main__':
    unittest.main()