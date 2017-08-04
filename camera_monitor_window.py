import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QTimer
from PyQt4.QtGui import QImage
import threading as th

import camera as cm
import imutils as imu
import cv2

class Credentials:
	def __init__(self, user, password):
		self.user = user
		self.password = password


class CameraMonitorWindow(QtGui.QMainWindow):
	def __init__(self):
		super(CameraMonitorWindow, self).__init__()

		self.read_configuration()

		self.cameraCB = QtGui.QComboBox(self)
		self.cameraCB.move(10,10)
		for i, camera in self.cameras.iterrows():
			self.cameraCB.addItem(camera["id"])
		self.cameraCB.activated[str].connect(self.camera_selected)
		self.pic = QtGui.QLabel(self)
		self.pic.move(10,45)
		self.pic.resize(300,300)


		self.setGeometry(5, 50, 800, 350)
		self.setWindowTitle("Camera monitor - Video Surveillance Tec")

		# self.stopEvent = th.Event()
		# self.thread = th.Thread(target=self.videoloop, args=())
		# self.thread.start()

		self._timer = QTimer(self)
		self._timer.timeout.connect(self.queryFrame)
		self._timer.start(50)

		self.cameraCB.setCurrentIndex(self.cameraCB.findText('CE_3', QtCore.Qt.MatchFixedString))
		self.camera_selected('CE_3')

		self.show()

	def camera_selected(self, text):
		self.camera = self.cameras[self.cameras["id"] == text].iloc[0]
		self.currCameraID = text

	def read_configuration(self):
		self.cameras = cm.Camera.getCameras()
		self.credentials = Credentials('live', 'GB98!1er@')
		self.prevCameraID = ''
		self.currCameraID = ''

	def get_camera_object(self):
		url = self.camera["url"].replace('rtsp://', 'rtsp://live:GB98!1er@')
		return imu.getCamera(url)

	def queryFrame(self):
		if (hasattr(self, "camera")):
			if (self.currCameraID != self.prevCameraID):
				self.cameraObj = self.get_camera_object()
				self.prevCameraID = self.currCameraID
			if (hasattr(self, "cameraObj") and self.cameraObj is not None):
				(grabbed, frame) = self.cameraObj.read()
				if grabbed:
					# cv2.imshow("Tracking", frame)
					# frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
					height, width, channel = frame.shape
					bytesPerLine = 3 * width
					qImg = QImage(frame.data, width, height, bytesPerLine, QImage.Format_RGB888)
					self.pic.setPixmap(QtGui.QPixmap(qImg))
					self.pic.resize(width,height)

	def videoloop(self):
		while not self.stopEvent.is_set():
			self.queryFrame()

	def __del__(self):
		self.stopEvent.set()

app = QtGui.QApplication(sys.argv)
GUI = CameraMonitorWindow()
sys.exit(app.exec_())
