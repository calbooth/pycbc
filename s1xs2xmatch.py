#!/bin/bash
from pycbc.waveform import get_td_waveform
from pycbc.filter import match
from pycbc.psd import aLIGOZeroDetHighPower
import numpy as np
import matplotlib.pyplot as plt

f_low = 30.0
sample_rate = 4096.0

MATCH = np.zeros([100,100])

h = -0.5
j = -0.5

k = 0
l = 0

while h < 0.5:
	l = 0
	while j < 0.5:
		
		# Generate the two waveforms to compare
		hp, hc = get_td_waveform(approximant="IMRPhenomPv2",
                	         mass1=20,
                        	 mass2=30,
                         	 f_lower=f_low,
                         	 delta_t=1.0/sample_rate)
		
		sp, sc = get_td_waveform(approximant="IMRPhenomPv2",
                	         mass1=20,
                        	 mass2=30,
				 spin1x=h,
				 spin1y=j,
				 spin1z=0.5,
                         	 f_lower=f_low,
                         	 delta_t=1.0/sample_rate)
                         

		# Resize the waveforms to the same length
		tlen = max(len(sp), len(hp))
		sp.resize(tlen)
		hp.resize(tlen)

		# Generate the aLIGO ZDHP PSD
		delta_f = 1.0 / sp.duration
		flen = tlen/2 + 1
		psd = aLIGOZeroDetHighPower(flen, delta_f, f_low) 

		# Note: This takes a while the first time as an FFT plan is generated
		# subsequent calls are much faster.
		m, i = match(hp, sp, psd=psd, low_frequency_cutoff=f_low)
		#print 'The match is: %1.3f' % m
		MATCH[k,l] = m
		

		j +=0.01
		l +=1
	h+=0.01
	k +=1

sx1 = np.arange(-0.5, 0.5, len(MATCH[:,0]))
sx2 = np.arange(-0.5, 0.5, len(MATCH[0,:]))
 
plt.figure()
#plt.contour(sx1, sx2, MATCH)
plt.imshow(MATCH, origin='lower', interpolation='nearest')
#plt.contourf(sx1, sx2, MATCH, 100)
plt.colorbar()
plt.show()
