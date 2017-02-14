import pylab
from pycbc.waveform import get_td_waveform
from pycbc.filter import match
from pycbc.psd import aLIGOZeroDetHighPower


hp, hc = get_td_waveform(approximant='SEOBNRv2',
                                 mass1=30,
                                 mass2=30,
                                 spin1z=0.9,
                                 delta_t=1.0/4096,
                                 f_lower=40)

sp, sc = get_td_waveform(approximant='IMRPhenomD',
                                 mass1=30,
                                 mass2=30,
                                 spin1z=0.9,
                                 delta_t=1.0/4096,
                                 f_lower=40)

pylab.plot(sp.sample_times, sp, label='IMRPhenomD')
pylab.plot(hp.sample_times, hp, label='SEOBNRv2')
pylab.ylabel('Strain')
pylab.xlabel('Time (s)')
pylab.legend()
pylab.show()


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
print 'The match is: %1.3f' % m

