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
		#Data Model VideoObject
		'id',
		'camera_id',
		'latitude',			#added
		'longitude',		#added
		'size_on_disk',  	#contentSize
		'width',
		'height',
		'duration',
		'bit_rate', 		#added
		'fps',
		'encoding',
		'length',
		'date',
		'time',
	# 	TODO: Agregar atributos de archivo data models gdoc
	# 	External functions
		'movement_percent',
	# 	Calculated attributes
		'size_length_ratio'
	]
	cv2Initiated=False

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
		cv2Initiated=True

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

	def getId(self):
		'''Consecutive number'''
		Id = self.video.index
		return Id

	def getDuration(self):
		'''Time expressed in seconds'''
		fps = self.getFps()
		length = self.getLength()
		if(fps==0 or length==0):
			return 0
		duration = length / fps
		return duration

	def getWidth(self):
		'''Number of pixels in horizontal axis'''
		# CV_CAP_PROP_FRAME_WIDTH
		if(not self.cv2Initiated):
			self.Cv2Init()
		return self.width

	def getHeight(self):
		'''Number of pixels in vertical axis'''
		if (not self.cv2Initiated):
			self.Cv2Init()
		return self.height

	def getLength(self):
		'''Frame count'''
		if (not self.cv2Initiated):
			self.Cv2Init()
		if int(self.cv2_major_ver) < 3:
			length = int(self.videoCapture.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))
		else:
			length = int(self.videoCapture.get(cv2.CAP_PROP_FRAME_COUNT))
		return length

	def getFps(self):
		if (not self.cv2Initiated):
			self.Cv2Init()
		if int(self.cv2_major_ver) < 3:
			fps = self.videoCapture.get(cv2.cv.CV_CAP_PROP_FPS)
		else:
			fps = self.videoCapture.get(cv2.CAP_PROP_FPS)
		return fps

	def getEncoding(self):
		'''The four digit code corresponding to the video codec'''
		if (not self.cv2Initiated):
			self.Cv2Init()
		if int(self.cv2_major_ver) < 3:
			encoding = self.videoCapture.get(cv2.cv.CV_CAP_PROP_FOURCC)
		else:
			encoding = self.videoCapture.get(cv2.CAP_PROP_FOURCC)
		return encoding

	def getSizeOnDisk(self):
		'''Size of the file expressed in bytes'''
		sizeOnDisk = os.path.getsize(self.filePath)
		return sizeOnDisk

	def getTimestamp(self):
		'''modified date in floating point'''
		if (not hasattr(self, "timestamp")):
			self.timestamp = os.path.getmtime(self.filePath)
		return self.timestamp

	def getDate(self):
		if(not hasattr(self,"timestamp")):
			self.timestamp = os.path.getmtime(self.filePath)
		date = datetime.datetime.fromtimestamp(self.timestamp).strftime('%Y-%m-%d')
		return date

	def getTime(self):
		if (not hasattr(self, "timestamp")):
			self.timestamp = os.path.getmtime(self.filePath)
		time = datetime.datetime.fromtimestamp(self.timestamp).strftime('%H:%M:%S')
		return time

	def getCameraId(self):
		ip = su.getIp(self.filePath)
		camera = cam.Camera(ip=ip)
		id = camera["id"]
		return id

	def getSizeLengthRatio(self):
		if(self.getLength()==0):
			return 0
		sizeLengthRatio = self.getSizeOnDisk()/self.getLength()
		return sizeLengthRatio

	def getMovementPercent(self):
		if (not self.cv2Initiated):
			self.Cv2Init()
		movement_percent=0
		motionDetector = md.MotionDetectorContour(video=self.videoCapture)
		(frame_counter, analyzed_frames, frames_with_motion, percentage, percentage_of_mov,
		result)= motionDetector.run()
		return '%f.2' % (percentage)

	def getLatitude(self):
		'''retrieved from camera model'''
		ip = su.getIp(self.filePath)
		camera = cam.Camera(ip=ip)
		latitude = camera["latitude"]
		return latitude

	def getLongitude(self):
		'''retrieved from camera model'''
		ip = su.getIp(self.filePath)
		camera = cam.Camera(ip=ip)
		latitude = camera["longitude"]
		return latitude

	def getBitRate(self):
		'''bps = bits per second'''
		sizeOnDisk = self.getSizeOnDisk()
		duration = self.getDuration()
		if(sizeOnDisk == 0 or duration == 0):
			return 0
		bitRate = sizeOnDisk*8/duration
		return bitRate

	def __del__(self):
		if (hasattr(self, "videoCapture") and self.videoCapture is not None):
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
