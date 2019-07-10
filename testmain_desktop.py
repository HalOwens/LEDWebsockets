import unittest
import asyncio
import main_desktop
from tkinter import *


class TestBuildString(unittest.TestCase):
    def test_between_0_255(self):
        testList = [[StringVar() for i in range(3)] for i in range(3)]
        for x in range(3):
            for y in range(3):
                testList[x][y].set(str((x*3)+y+1))
        asyncio.run(main_desktop.build_string(testList))
        self.assertEqual(main_desktop.get_tx_string(), "[[1, 2, 3], [4, 5, 6], [7, 8, 9]]")

    def test_greater_than_255(self):
        testList = [[StringVar() for i in range(3)] for i in range(3)]
        for x in range(3):
            for y in range(3):
                testList[x][y].set(255+x)
        asyncio.run(main_desktop.build_string(testList))
        self.assertEqual(main_desktop.get_tx_string(), "[[255, 255, 255], [255, 255, 255], [255, 255, 255]]")

    def test_less_than_0(self):
        testList = [[StringVar() for i in range(3)] for i in range(3)]
        for x in range(3):
            for y in range(3):
                testList[x][y].set(str(0-x))
        asyncio.run(main_desktop.build_string(testList))
        self.assertEqual(main_desktop.get_tx_string(), "[[0, 0, 0], [0, 0, 0], [0, 0, 0]]")


if __name__ == '__main__':
    Tk()
    unittest.main()