from pycbc.io import InferenceFile
fp = InferenceFile("cbc_example-n1e4.hdf.hdf", "r")

samples = fp.read_samples("mass1", walkers = 0)
print samples.mass1
