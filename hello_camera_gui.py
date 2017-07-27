import cv2
import Tkinter as tki
import tkMessageBox
import pandas as pd
import threading as th
from PIL import Image
from PIL import ImageTk
import camera as cm

class HelloCameraGui:
	"""
		List of cameras for visualization
	"""
	def __init__(self):
		self.cameras = cm.Camera.getCameras()
		self.user = 'live'
		self.password = 'GB98!1er@'

		self.root = tki.Tk()
		self.tkFrame = tki.Frame(self.root, width=900, height=900)
		self.tkFrame.pack(fill="both", expand=True)
		lb1 = tki.Listbox(self.tkFrame)
		for i, camera in self.cameras.iterrows():
			lb1.insert(i, camera["id"])
		lb1.pack()
		lb1.bind('<<ListboxSelect>>', self.onSelect)

		self.stopEvent = th.Event()
		self.thread = th.Thread(target=self.videoloop, args=())
		self.thread.start()

		self.root.wm_title("Camera test - Video Surveillance Tec")
		self.root.wm_protocol("WM_DELETE_WINDOW", self.onClose)

	def videoloop(self):
		while not self.stopEvent.is_set():
			print "loop"
		return

	def onSelect(self):
		tkMessageBox.showinfo("Title", "a Tk MessageBox")

	def onClose(self):
		self.stopEvent.set()
		self.root.quit()

if __name__=="__main__":
    t = HelloCameraGui()
    t.root.mainloop()