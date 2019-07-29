import unittest
import asyncio
import main_desktop
from tkinter import *


class TestBuildString(unittest.TestCase):

    uut = main_desktop.Desktop()

    def test_between_0_255(self):
        """Verifies that when all inputs are valid they are put into a string of the proper form """
        self.uut.input1.set(1)
        self.uut.input2.set(2)
        self.uut.input3.set(3)
        self.uut.input4.set(4)
        self.uut.input5.set(5)
        self.uut.input6.set(6)
        self.uut.input7.set(7)
        self.uut.input8.set(8)
        self.uut.input9.set(9)

        asyncio.run(self.uut.build_string())
        self.assertEqual(self.uut.tx_string, "[[1, 2, 3], [4, 5, 6], [7, 8, 9]]")

    def test_greater_than_255(self):
        """Verifies that any inputs over 255 are mapped to the value 255"""
        self.uut.input1.set(256)
        self.uut.input2.set(256)
        self.uut.input3.set(256)
        self.uut.input4.set(256)
        self.uut.input5.set(256)
        self.uut.input6.set(256)
        self.uut.input7.set(256)
        self.uut.input8.set(256)
        self.uut.input9.set(256)

        asyncio.run(self.uut.build_string())
        self.assertEqual(self.uut.tx_string, "[[255, 255, 255], [255, 255, 255], [255, 255, 255]]")

    def test_less_than_0(self):
        """Verifies that any values under 0 are mapped to the value 0"""
        self.uut.input1.set(-1)
        self.uut.input2.set(-1)
        self.uut.input3.set(-1)
        self.uut.input4.set(-1)
        self.uut.input5.set(-1)
        self.uut.input6.set(-1)
        self.uut.input7.set(-1)
        self.uut.input8.set(-1)
        self.uut.input9.set(-1)

        asyncio.run(self.uut.build_string())
        self.assertEqual(self.uut.tx_string, "[[0, 0, 0], [0, 0, 0], [0, 0, 0]]")


if __name__ == '__main__':
    Tk()
    unittest.main()