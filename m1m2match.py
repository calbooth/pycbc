#!/bin/bash
from pycbc.waveform import get_td_waveform
from pycbc.filter import match
from pycbc.psd import aLIGOZeroDetHighPower
import numpy as np
import matplotlib.pyplot as plt

f_low = 30.0
sample_rate = 4096.0

MATCH = np.zeros([100,100])

i = 1
j = 1

while i < 100:
	while j < 100:
		# Generate the two waveforms to compare
		hp, hc = get_td_waveform(approximant="IMRPhenomPv2",
                	         mass1=i,
                        	 mass2=i,
                         	 f_lower=f_low,
                         	 delta_t=1.0/sample_rate)
		
		sp, sc = get_td_waveform(approximant="IMRPhenomPv2",
                	         mass1=i,
                        	 mass2=j,
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
		m, i = match(hp, hc, psd=psd, low_frequency_cutoff=f_low)
		#print 'The match is: %1.3f' % m
		MATCH[i,j] = m
		j +=1
	i+=1
M = np.arange(1, 101, 1)

plt.figure()
plt.contour(M, M, MATCH)
plt.colorbar()
