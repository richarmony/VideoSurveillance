import cv2
import Tkinter as tki
import tkMessageBox
import pandas as pd
import threading as th
from PIL import Image
from PIL import ImageTk
import camera as cm
import imutils as imu


class HelloCameraGui:
	"""
		List of cameras for visualization
	"""

	def __init__(self):
		self.cameras = cm.Camera.getCameras()
		self.user = 'live'
		self.password = 'GB98!1er@'
		self.currentSelectedCamera = ''
		self.selectedCamera = ''

		self.root = tki.Tk()
		self.tkFrame = tki.Frame(self.root, width=900, height=900)
		self.tkFrame.pack(fill="both", expand=True)
		self.lb1 = tki.Listbox(self.tkFrame)
		for i, camera in self.cameras.iterrows():
			self.lb1.insert(i, camera["id"])
		self.lb1.pack()
		self.lb1.bind('<<ListboxSelect>>', self.onSelect)

		self.stopEvent = th.Event()
		self.thread = th.Thread(target=self.videoloop, args=())
		self.thread.start()

		self.root.wm_title("Camera test - Video Surveillance Tec")
		self.root.wm_protocol("WM_DELETE_WINDOW", self.onClose)

	def videoloop(self):
		while not self.stopEvent.is_set():
			if(hasattr(self, "cameraUrl")):
				if (self.currentSelectedCamera != self.selectedCamera and self.selectedCamera is not None):
					self.camera = self.getCameraObj(self.cameraUrl)
					self.currentSelectedCamera = self.selectedCamera
				if(hasattr(self, "camera") and self.camera):
					(grabbed, frame) = self.camera.read()
					if grabbed:
						# cv2.imshow("Tracking", frame)
						frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
						frame = Image.fromarray(frame)
						frame = ImageTk.PhotoImage(frame)
						if not hasattr(self, 'panel'):
							self.panel = tki.Label(self.tkFrame, image=frame)
							self.panel.image = frame
							self.panel.pack(side="left", padx=10, pady=10)
						else:
							self.panel.configure(image=frame)
							self.panel.image = frame

	def onSelect(self, e):
		index = int(self.lb1.curselection()[0])
		self.selectedCamera = self.lb1.get(index)
		print self.selectedCamera
		# print self.cameras
		self.cameraUrl = self.cameras[self.cameras["id"] == self.selectedCamera]["url"].iloc[0]
		print self.cameraUrl

	def getCameraObj(self, url):
		print url.replace('rtsp://', 'rtsp://live:GB98!1er@')
		return imu.getCamera(url.replace('rtsp://', 'rtsp://live:GB98!1er@'))

	def onClose(self):
		self.stopEvent.set()
		self.root.quit()


if __name__ == "__main__":
	t = HelloCameraGui()
	t.root.mainloop()
