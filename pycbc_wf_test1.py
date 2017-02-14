import pylab
from pycbc.waveform import get_td_waveform


hp, hc = get_td_waveform(approximant='IMRPhenomD',
                                 mass1=25,
                                 mass2=40,
                                 spin1z=0.9,
                                 delta_t=1.0/4096,
                                 f_lower=40)

pylab.plot(hp.sample_times, hp, label='IMRPhenomD')

pylab.ylabel('Strain')
pylab.xlabel('Time (s)')
pylab.legend()
pylab.show()
