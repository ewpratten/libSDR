from rtlsdr import RtlSdr
import matplotlib
matplotlib.use("agg")
from matplotlib.pyplot import psd

import devicelookup as devl

class RTLsdr(object):
	def __init__(self,  freq, gain, rate=2.4e6, correction=60):
		# Load the device
		if not self.__loadDevice():
			devl.getAccess(devl.findSDR(devl.getDevices()))
			self.__loadDevice()
		# Set up sdr
		self.setParams(rate, freq, correction, gain)
	
	def __loadDevice(self):
		try:
			self.radio = RtlSdr()
			return True
		except:
			return False
	
	def read(self,width:int):
		return self.radio.read_samples(width).tolist()
	
	def readPSD(self,width:int):
		samples = self.read(width)
		return psd(samples, NFFT=1024, Fs=self.radio.sample_rate/1e6, Fc=self.radio.center_freq/1e6, return_line=True)
	
	def setParams(self, rate, freq, correction, gain):
		self.radio.sample_rate     = rate
		self.radio.center_freq     = freq
		self.radio.freq_correction = correction
		self.radio.gain            = gain