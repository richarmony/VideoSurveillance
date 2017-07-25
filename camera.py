import argparse
import pandas as pd


class Camera:
	CAMERAS_CSV = 'cameras.csv'

	def __init__(self, id=None, ip=None, cameras=None):
		if (cameras is None):
			self.cameras = pd.DataFrame.from_csv(self.CAMERAS_CSV, index_col=None)
		else:
			self.cameras = cameras
		if (id is None and ip is None):
			raise ValueError('ID or IP must be set.')
		if (id is not None):
			self.camera = self.cameras.loc[self.cameras['id'] == id]
		if (ip is not None):
			self.camera = self.cameras.loc[self.cameras['ip'] == ip]
		if (self.camera is None):
			raise ValueError('Camera id not found.')

	def __getitem__(self, key):
		return self.getAttribute(key)

	def getAttribute(self, name):
		"""
		Get attribute value
		:param name:
		:return:
		"""
		attribute = self.camera[name].iloc[0]
		return attribute


if __name__ == '__main__':
	ap = argparse.ArgumentParser()
	ap.add_argument('--id', required=True)
	ap.add_argument('--getAttribute', required=False)
	ap.add_argument('--method', required=False)
	args = vars(ap.parse_args(()))
	obj = Camera(args['id'])
	getAttribute = args['getAttribute']
	staticMethod = args['staticMethod']
	if (getAttribute is not None):
		print obj.getAttribute(getAttribute)
	if(staticMethod is not None):
		eval('obj.'+staticMethod)
