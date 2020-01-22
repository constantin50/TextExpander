# program replace defined sequence of symbols with another one
# example: '\delta' -> 'δ' 
#
# above: 
# preimage - sequence of symbols that is replaced
# image - sequence of symbols that preimage is replaced with

import tkinter
from tkinter import *
import pickle
import keyboard
import os

class GUI:

	window = None
	slots = list() # list of pairs of entries  
	pairs = list() # list of pairs where each pais is [preimage, image]
	functions = list() # list of functions that implement replacement preimage with image

	def __init__(self):

		self.window = Tk();
		self.window.title("Text Expander")
		self.window.geometry("350x600")
		self.window.resizable(0, 0)
		self.window.iconbitmap(r'C:\Users\kkons\OneDrive\Документы\Код\Current Projects\Text Exp\icon.ico')

		submit_button = Button(self.window, text="submit", height = 1, width = 9, command = self.submit)
		submit_button.place(x = 150, y = 540)

		k = 0;
		for i in range(20):
			entry1 = Entry(self.window)
			entry1.place(x = 50, y = 20+k)

			entry2 = Entry(self.window)
			entry2.place(x = 200, y = 20+k)

			k += 25;

			self.slots.append([entry1,entry2])
			self.pairs.append(["",""])
			self.functions.append(None)

		if (os.path.exists(r"C:\Users\kkons\OneDrive\Документы\Код\Current Projects\Text Exp\slots.pkl") and
			os.stat(r"C:\Users\kkons\OneDrive\Документы\Код\Current Projects\Text Exp\slots.pkl").st_size != 0):
			self.load()
			self.submit()

		self.window.mainloop()


	# make function that erases preimage and writes image		
	def make_func(self,preimage,image):

		def func():
			for i in range(len(preimage)+1):
				keyboard.press_and_release("backspace")
			keyboard.write(image)
		print("function with ", preimage, " and ", image)
		return func

	# save current slots 
	def save(self):

		for slot in self.slots:
			
			preimage = slot[0].get();
			image = slot[1].get()

			self.pairs.append([preimage, image])
			replace = self.make_func(preimage,image)

			self.functions.append(replace)

		file = open(r"C:\Users\kkons\OneDrive\Документы\Код\Current Projects\Text Exp\slots.pkl", "wb");
		pickle.dump(self.pairs, file)

	# load slots of previous session
	def load(self):

		file = open(r"C:\Users\kkons\OneDrive\Документы\Код\Current Projects\Text Exp\slots.pkl", "rb");
		self.pairs = pickle.load(file)

		for i in range(len(self.slots)):
			
			preimage = self.pairs[i][0]
			image = self.pairs[i][1]

			self.slots[i][0].insert(0,preimage)
			self.slots[i][1].insert(0,image)

			replace = self.make_func(preimage,image)

			self.functions[i] = replace



	def submit(self):
		
		for i in range(len(self.slots)):

			preimage  = self.slots[i][0].get() # entry 1
			image = self.slots[i][1].get() # entry 2

			temp = image

			# check: whether some phrase was removed

			if (preimage != self.pairs[i][0] and self.pairs[i][0] != "" ):
				keyboard.remove_word_listener(self.pairs[i][0])
				self.pairs[i][0] = preimage
				self.pairs[i][1] = image
				self.functions[i] = self.make_func(preimage, image)
				print(self.pairs[i][0], " was removed")


			if (preimage != "" and image != ""):

				replace = self.make_func(preimage,image)
				self.functions.append(replace)

			self.pairs[i][0] = preimage
			self.pairs[i][1] = image
			print(preimage, "->", image)
			keyboard.add_word_listener(preimage, self.functions[i])

		self.save()

		print("slots have been saved")

t = GUI()
