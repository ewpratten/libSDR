import re
import subprocess
import os

def getDevices():
	device_re = re.compile("Bus\s+(?P<bus>\d+)\s+Device\s+(?P<device>\d+).+ID\s(?P<id>\w+:\w+)\s(?P<tag>.+)$", re.I)
	df = subprocess.check_output("lsusb").decode()
	devices = []
	for i in df.split('\n'):
		if i:
			info = device_re.match(i)
			if info:
				dinfo = info.groupdict()
				dinfo['device'] = '/dev/bus/usb/%s/%s' % (dinfo.pop('bus'), dinfo.pop('device'))
				devices.append(dinfo)
	return devices

def findSDR(devices):
	known_vendors = ["0bda"]
	output = []
	for device in devices:
		for vendor in known_vendors:
			if vendor in device["id"]:
				output.append({"path":device["device"], "name":device["tag"], "id":device["id"]})
	return output

def getAccess(devices):
	print("Enter your password to get device permission")
	for device in devices:
		os.system("sudo chmod 0666 " + str(device["path"]))
		