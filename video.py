import argparse
import os
import datetime
import pandas as pd
import string_utils as su
import cv2
import logging
import camera as cam
import motionDetector as md

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Video:
	FRAMES_READ_MIN = 10
	VIDEOS_CSV_DEFAULT = 'videos.csv'
	ATTRIBUTES = [
		'length',
		'width',
		'height',
		'fps',
		'encoding',
		'size_on_disk',
		'date',
		'time',
		'camera_id',
	# 	TODO: Agregar atributos de archivo data models gdoc
	# 	External functions
		'movement_percent',
	# 	Calculated attributes
		'size_length_ratio'
	]

	@classmethod
	def getAttributeList(self):
		return self.ATTRIBUTES

	def __init__(self, filePath, videos=None):
		self.filePath = filePath
		if (videos is None):
			self.videos = pd.DataFrame.from_csv(self.VIDEOS_CSV_DEFAULT, index_col=None)
		else:
			self.videos = videos
		self.video = self.videos.loc[self.videos['filePath'] == self.filePath]
		if (self.video is None):
			raise ValueError('Video id not found.')
		if (not os.path.exists(self.filePath)):
			raise ValueError('Video file path does not exist.')
		self.timestamp = os.path.getmtime(self.filePath)
		self.Cv2Init()

	def Cv2Init(self):
		try:
			(self.cv2_major_ver, self.cv2_minor_ver, self.cv2_subminor_ver) = (cv2.__version__).split('.')
			self.height, self.width, self.channels = (0, 0, 0)
			self.videoCapture = cv2.VideoCapture(self.filePath)
			for i in range(self.FRAMES_READ_MIN):
				(grabbed, frame) = self.videoCapture.read()
				if (grabbed):
					self.height, self.width, self.channels = frame.shape
					break
		except:
			# TODO: logger
			raise

	def __getitem__(self, key):
		return self.getAttribute(key)

	def getAttribute(self, name):
		"""

		:rtype: str
		:param attributeName: 
		:return: 
		"""
		if (name not in self.ATTRIBUTES):
			raise ValueError('Video attribute out of scope.')
		try:
			if(self.video.isnull().values.any()):
				attribute = self.computeAttribute(name)
				self.setAttribute(name, attribute)
			else:
				attribute = self.video[name].iloc[0]
		except:
			attribute = self.computeAttribute(name)
			self.setAttribute(name, attribute)
			pass
		return attribute

	def __setitem__(self, key, value):
		self.setAttribute(key, value)

	def setAttribute(self, name, value):
		self.videos.loc[self.videos['filePath'] == self.filePath, name] = value
		self.video[name] = value

	def computeAttribute(self, name, externalFunction=None):
		"""

		:rtype: str
		:param attributeName:
		:param externalFunction: 
		:return: 
		"""
		if (name not in self.ATTRIBUTES):
			raise ValueError('Video attribute out of scope.')
		attribute = eval(
			'self.get' + su.getTitlecaseFromSnakecase(name) + '()' if externalFunction is None else externalFunction + '(self)')
		return attribute

	def getDuration(self):
		duration = self.getFps() / self.getLength()
		return duration

	def getWidth(self):
		return self.width

	def getHeight(self):
		return self.height

	def getLength(self):
		if int(self.cv2_major_ver) < 3:
			length = int(self.videoCapture.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))
		else:
			length = int(self.videoCapture.get(cv2.CAP_PROP_FRAME_COUNT))
		return length

	def getFps(self):
		if int(self.cv2_major_ver) < 3:
			fps = self.videoCapture.get(cv2.cv.CV_CAP_PROP_FPS)
		else:
			fps = self.videoCapture.get(cv2.CAP_PROP_FPS)
		return fps

	def getEncoding(self):
		if int(self.cv2_major_ver) < 3:
			encoding = self.videoCapture.get(cv2.cv.CV_CAP_PROP_FOURCC)
		else:
			encoding = self.videoCapture.get(cv2.CAP_PROP_FOURCC)
		return encoding

	def getSizeOnDisk(self):
		sizeOnDisk = os.path.getsize(self.filePath)
		return sizeOnDisk

	def getTimestamp(self):
		return self.timestamp

	def getDate(self):
		date = datetime.datetime.fromtimestamp(self.timestamp).strftime('%Y-%m-%d')
		return date

	def getTime(self):
		time = datetime.datetime.fromtimestamp(self.timestamp).strftime('%H:%M:%S')
		return time

	def getCameraId(self):
		ip = su.getIp(self.filePath)
		camera = cam.Camera(ip=ip)
		return camera["id"]

	def getSizeLengthRatio(self):
		if(self.getLength()==0):
			return 0
		sizeLengthRatio = self.getSizeOnDisk()/self.getLength()
		return sizeLengthRatio

	def getMovementPercent(self):
		movement_percent=0
		# motionDetector = md.MotionDetectorContour(videoPath=self.filePath)
		# (movement_percent, delete)=motionDetector.run()
		return movement_percent

	def __del__(self):
		if (self.videoCapture is not None):
			self.videoCapture.release()


if __name__ == '__main__':
	ap = argparse.ArgumentParser()
	ap.add_argument('--filePath', required=True)
	ap.add_argument('--getAttribute', required=False)
	ap.add_argument('--staticMethod', required=False)
	args = vars(ap.parse_args(()))
	obj = Video(args['filePath'])
	getAttribute = args['getAttribute']
	staticMethod = args['staticMethod']
	if (getAttribute is not None):
		print obj.getAttribute(getAttribute)
	if (staticMethod is not None):
		eval('obj.' + staticMethod+'()')
