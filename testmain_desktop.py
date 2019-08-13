import unittest
import main_desktop
from tkinter import *
from tkinter import ttk, StringVar
import asyncio
import websockets


class Test(unittest.TestCase):

	uut = main_desktop.Desktop()

	def test_less_than_0(self):
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

	def test_greater_than_255(self):
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

	def test_between_0_255(self):
		self.uut.input1.set(5)
		self.uut.input2.set(5)
		self.uut.input3.set(5)
		self.uut.input4.set(5)
		self.uut.input5.set(5)
		self.uut.input6.set(5)
		self.uut.input7.set(5)
		self.uut.input8.set(5)
		self.uut.input9.set(5)
		asyncio.run(self.uut.build_string())
		self.assertEqual(self.uut.tx_string, "[[5, 5, 5], [5, 5, 5], [5, 5, 5]]")


if __name__ == '__main__':
	Tk()
	unittest.main()