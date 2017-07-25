import os
import re
import cv2
import pandas as pd
import video as vi

camera_dict = {
	'25': 'CE_1',
	'46': 'CE_2',
	'125': 'CE_3',
	'27': 'PB_1',
	'28': 'PB_2',
	'55': 'PB_3',
	'145': 'PS_1',
	'146': 'PS_2',
	'36': 'EP_1',
	'61': 'EP_2',
	'62': 'EP_3',
	'63': 'EP_4',
	'82': 'EP_5',
	'83': 'EP_6',
	'88': 'EP_7'
}
ipAddress_test_list = '105.161.191.227, 97.133.165.17, 76.49.110.168, 17.111.236.104, 130.107.223.34, 197.254.39.90, 114.134.26.234, 1.61.211.168, 207.92.10.168, 107.204.197.196, 46.27.97.177, 87.187.84.183, 158.33.23.194, 122.62.102.90, 124.185.142.53, 237.176.124.144, 139.194.73.140, 25.89.134.194, 200.239.249.5, 77.9.132.133, 168.222.238.76, 181.57.233.247, 9.193.68.132, 188.57.121.184, 8.74.235.49, 199.30.32.24, 110.217.26.62, 222.149.31.250, 51.152.49.133, 234.159.182.101, 115.207.246.106, 166.254.191.171, 130.6.187.107, 133.128.89.165, 221.235.78.208, 178.91.166.206, 94.64.88.206, 89.97.224.234, 180.184.7.1, 73.103.63.160, 102.224.129.18, 86.38.248.238, 197.96.26.122, 110.125.16.54, 171.196.195.20, 243.20.59.175, 32.80.240.66, 74.40.209.65, 34.95.213.253, 172.89.215.190, 124.85.99.95, 220.145.15.80, 90.172.50.254, 232.14.39.6, 198.147.55.249, 213.49.244.193, 253.127.101.191, 128.92.198.198, 2.104.138.93, 152.88.179.199, 159.77.24.175, 67.134.72.10, 72.160.194.121, 104.21.8.223, 199.52.197.25, 0.101.83.92, 240.178.169.144, 194.33.93.51, 36.247.224.110, 118.126.185.189, 167.150.211.178, 146.114.207.30, 66.158.177.234, 82.54.230.84, 205.239.87.173, 96.238.174.18, 171.174.26.134, 199.153.151.224, 245.109.54.197, 2.35.243.63, 104.73.3.24, 197.101.3.231, 4.77.73.221, 129.37.216.218, 205.15.92.123, 20.121.225.133, 74.129.7.178, 91.168.100.69, 22.87.142.43, 128.211.203.161, 167.229.52.120, 63.239.154.125, 238.118.179.132, 210.169.89.235, 242.112.167.56, 185.194.97.10, 103.126.250.73, 32.30.161.66, 198.217.54.243, 201.236.55.181, 111.69.2.149, 224.172.40.9, 167.21.139.5, 153.69.235.177, 199.18.201.122, 69.89.211.19, 180.114.217.160, 52.184.1.179, 203.25.33.205, 39.73.222.135, 93.237.51.101, 171.25.79.203, 204.187.41.146, 84.248.134.6, 14.238.4.224, 247.102.101.246, 162.159.205.146, 83.97.117.236, 77.41.96.42, 142.130.189.74, 182.214.168.9, 89.203.45.154, 226.116.62.51, 219.226.121.130, 114.48.134.36, 151.14.155.79, 177.91.61.16, 132.25.135.186, 120.42.170.69, 178.141.96.11, 209.188.6.207, 152.225.246.249, 88.108.40.226, 210.194.138.33, 76.50.132.223, 231.120.215.87, 119.173.108.242, 198.30.228.73, 130.251.180.191, 151.52.30.101, 160.130.105.218, 91.79.185.116, 48.129.128.3, 49.55.123.100, 69.180.237.37, 182.171.53.246, 237.253.166.150, 136.63.199.31, 139.12.207.254, 125.142.46.239, 67.133.107.222, 52.235.190.97, 12.254.16.68, 198.56.196.84, 65.143.191.197, 144.241.218.158, 212.208.235.14, 49.218.48.247, 207.39.139.78, 194.102.111.45, 102.162.216.10, 71.45.16.71, 132.248.86.181, 189.180.10.62, 93.13.151.180, 145.5.119.73, 205.79.210.3, 44.250.47.52, 142.50.151.198, 188.236.225.175, 214.174.182.106, 6.250.205.221, 195.224.209.179, 111.26.221.52, 202.4.48.243, 224.97.179.118, 180.6.39.215, 15.235.39.144, 20.198.98.16, 94.234.61.175, 183.87.63.217, 144.184.43.186, 168.157.41.245, 41.190.254.211, 93.30.163.148, 215.111.61.116, 85.200.7.241, 151.9.227.103, 205.64.66.178, 245.174.85.75, 15.180.150.97, 18.165.204.209, 253.251.246.150, 201.50.168.7, 175.58.3.246, 50.9.185.156, 39.25.131.59, 168.247.103.226, 28.31.215.95, 39.99.108.229'
good_filename = r"D:\Server\camaras_Nov_24_2016\camaras_11_00\11.40.54.27\PB_1-01080-01140.mp4"
wrong_filename = r"D:\Server\camaras_Nov_24_2016\camaras_11_00\11.40.54.27\PB_2-01080-01141.mp4"


def find_by_extension(extension, path=os.getcwd()):
	'''generate a list of files... same result as:
	windows: dir *expresion /s /b > file_search.txt
	linux:   find -type f | grep expresion -> file_search.txt'''
	file_list = []
	if extension.find('.') < 0:
		extension = '.' + extension
	fileRegex = re.compile(extension)
	f = open('file_search.txt', 'wb')
	for foldername, subfolders, filenames in os.walk(path):
		for filename in filenames:
			if fileRegex.search(filename) is not None:
				path = os.path.join(foldername, filename)
				file_list.append(path)
				path += '\n'
				print path
				f.write(path)
	f.close()
	return file_list


def find_videos(directory=os.getcwd()):
	'''generate a list of videos from folder... same result as:
		windows: dir *.mp4 /s /b > video_search.txt
		linux:   find -type f | grep .mp4 -> video_search.txt'''
	videoRegex = re.compile(r'\d.mp4')
	video_list = []
	f = open('video_search.txt', 'wb')
	for foldername, subfolders, filenames in os.walk(directory):
		for filename in filenames:
			if videoRegex.search(filename) is not None:
				path = os.path.join(foldername, filename)
				video_list.append(path)
				path += '\n'
				print path
				f.write(path)

	f.close()
	f.close()
	return video_list


def checkFileNames(videoPath):
	'''Check if the videos are correctly named according to IP address and filename'''
	if not os.path.exists(videoPath):
		return 'File does not exist'
	# Get filename
	original_filename = os.path.basename(videoPath)
	# Build regular expression compilers
	IPRegex = re.compile(r'(\d+.\d+.\d+.)(\d+)\\')  # regex to get an IP address
	FileNameRegex = re.compile(r'[CEP][EBSP]_\d')  # regex to get the filename prefix
	# Get IP's last 1-3 digits to compare with dictionary and get filename
	result = IPRegex.search(videoPath)
	result2 = FileNameRegex.search(videoPath)
	# Check results
	if result is None:
		return 'No IP Address found'
	if result2 is None:
		return 'No Filename prefix found'

	ipAddress = result.group(1) + result.group(2)
	last_digits = result.group(2)
	file_suffix = result2.group()
	dict_file_suffix = camera_dict[last_digits]  # look up in the dictionary :)
	if dict_file_suffix != file_suffix:
		# print "Incorrect filename, should be %s instead of %s" %(dict_file_suffix, file_suffix)
		new_filename = dict_file_suffix + str(original_filename[4:])
		videoDir = os.path.dirname(videoPath)
		new_videoPath = os.path.join(videoDir, new_filename)
		# print original_filename
		# print new_filename
		# print new_videoPath
		os.rename(videoPath, new_videoPath)
		# print "Changed filename from %s to %s" %(original_filename, new_videoPath)
		return "Changed %s -> %s" % (original_filename, new_filename)

	else:
		# print "Dict: %s is equal to filename: %s" %(camera_dict[last_digits], file_suffix)
		return "Correct filename %s" % (original_filename)


def save_video_attributes(inputFilepath="video_search.txt", outputFilepath="videos.csv"):
	"""
	TODO: C++ pandas integration?
	:param inputFilepath:
	:param outputFilepath:
	"""
	attributeList = vi.Video.getAttributeList()
	videos = pd.read_csv(inputFilepath, sep=',', names=['filePath'], index_col=None).head(100)
	videos = pd.DataFrame(videos, columns=['filePath'].extend(attributeList))
	(totalRows,_)=videos.shape
	for index, videoLine in videos.iterrows():
		print videoLine['filePath']
		video = vi.Video(videoLine['filePath'], videos=videos)
		for attributeName in attributeList:
			# print '\t' + str(video[attribute])
			read = video[attributeName]
	# TODO: Write attribute immediately
	videos.to_csv(outputFilepath)


if __name__ == '__main__':
	# print checkFileNames('D:\\Server\\video_list.txt')
	# print checkFileNames(good_filename)
	# print checkFileNames(wrong_filename)
	# print checkFileNames('sampleFile.txt')
	# print checkFileNames('someFile') #won't run ;)
	# print "camera_dict['55']:"
	# print camera_dict['55']

	# find_videos("/home/a00967373/data")
	save_video_attributes()
	# print vi.Video(r"/home/a00967373/data/2017_0406/03_00/10.48.34.125/CE_3-01500-01800.mp4")