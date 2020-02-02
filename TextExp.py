# program func defined sequence of symbols with another one
# example: '\delta' -> 'δ' 
#
# terminology: 
# preimage - sequence of symbols that is replaced
# image - sequence of symbols that preimage is replaced with
#

import wx
import wx.adv
import os
import keyboard
import pickle


# icon in tray
class CustomTaskIcon(wx.adv.TaskBarIcon):

	def __init__(self, frame):
		wx.adv.TaskBarIcon.__init__(self)
		self.frame = frame

		icon = wx.Icon((str(os.path.dirname(os.path.abspath(__file__))) + '\\icon.ico'), wx.BITMAP_TYPE_ICO)
		self.SetIcon(icon, "Text Expander")

		self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.OnTaskBarLeftClick)
	
	def OnTaskBarActivate(self, evt):
		pass
	
	# destroy app
	def OnTaskBarClose(self, evt):
		self.frame.Close()

	# unfold menu
	def OnTaskBarLeftClick(self, evt):
		self.frame.Show()
		self.frame.Restore()


class MainFrame(wx.Frame):

	window = None
	entries = list() # list of pairs of GUI-entries  
	pairs = list() # list of pairs where each pair is list [preimage, image]
	functions = list() # functions that implement replacement the preimage with the image
	path = None

	def __init__(self):

		# path to saved values
		self.path = os.path.dirname(os.path.abspath(__file__))

		# gui details
		wx.Frame.__init__(self, None, title='Text Expander', size=(240, 720))
		panel = wx.Panel(self)

		button = wx.Button(panel, label='SUBMIT', pos=(60, 640))
		self.tbIcon = CustomTaskIcon(self)

		icon = wx.Icon((str(os.path.dirname(os.path.abspath(__file__))) + '\\icon.ico'))
		self.SetIcon(icon)


		k = 0;
		for i in range(20):

			self.entries.append([wx.TextCtrl(panel, size=(70,20), pos=(20,30+k)),
				wx.TextCtrl(panel, size=(70,20), pos=(120,30+k))])
			k += 30;

			self.pairs.append(["",""])
			self.functions.append(None)

		self.Bind(wx.EVT_BUTTON, self.submit)
		self.Bind(wx.EVT_ICONIZE, self.onMinimize)
		self.Bind(wx.EVT_CLOSE, self.onClose)


		# if there are saved entries then open them	
		if (os.path.exists(str(self.path) + '\\slots.pkl') and
			os.stat(str(self.path) + '\\slots.pkl').st_size != 0):
			self.load()
			self.submit()



		self.Show()


	# make function that erases preimage and writes image		
	def make_func(self,preimage,image):

		def func():
			for i in range(len(preimage)+1):
				keyboard.press_and_release("backspace")
			keyboard.write(image)
		return func


	# save entries of current session 
	def save(self):

		for entry in self.entries:
			
			preimage = entry[0].GetValue();
			image = entry[1].GetValue()

			self.pairs.append([preimage, image])
			func = self.make_func(preimage,image)

			self.functions.append(func)

		file = open(str(self.path) + '\\slots.pkl', "wb");
		pickle.dump(self.pairs, file)


	# load entries of previous session
	def load(self):

		file = open(str(self.path) + '\\slots.pkl', "rb");
		self.pairs = pickle.load(file)

		for i in range(len(self.entries)):
			
			preimage = self.pairs[i][0]
			image = self.pairs[i][1]

			self.entries[i][0].SetValue(preimage)
			self.entries[i][1].SetValue(image)
			func = self.make_func(preimage,image)
			self.functions[i] = func


	# get info form entries, make functions, save changes
	def submit(self):
		
		for i in range(len(self.entries)):

			preimage  = self.entries[i][0].GetValue() # entry 1
			image = self.entries[i][1].GetValue() # entry 2

			# check: whether some phrases were removed

			if (preimage != self.pairs[i][0] and self.pairs[i][0] != "" ):
				keyboard.remove_word_listener(self.pairs[i][0])
				self.pairs[i][0] = preimage
				self.pairs[i][1] = image


			if (preimage != "" and image != ""):

				self.functions[i] = self.make_func(preimage, image)
				self.pairs[i][0] = preimage
				self.pairs[i][1] = image
				keyboard.add_word_listener(preimage, self.functions[i], match_suffix=True)

		self.save()

	# destroy frame and icon in taskbar 
	def onClose(self, evt):
		self.tbIcon.RemoveIcon()
		self.tbIcon.Destroy()
		self.Destroy()

	# send the app in tray
	def onMinimize(self, evt):
		if self.IsIconized():
			self.Hide()


def main():
	app = wx.App(False)
	frame = MainFrame()
	app.MainLoop()

main()

