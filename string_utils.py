import re

def getTitlecaseFromSnakecase(s):
   words = s.split('_')
   return ''.join(word.capitalize() for word in words)

def getIp(s):
	return re.findall(r'[0-9]+(?:\.[0-9]+){3}', s)[0]