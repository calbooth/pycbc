# define coalescence time, observed masses, and waveform parameters
TRIGGER_TIME=1126259462.0
INJ_APPROX=SEOBNRv2threePointFivePN
MASS1=37.
MASS2=32.
RA=2.21535724066
DEC=-1.23649695537
INC=2.5
COA_PHASE=1.5
POLARIZATION=1.75
DISTANCE=100000 # in kpc
INJ_F_MIN=28.
TAPER="start"

# path of injection file that will be created in the example
INJ_PATH=injection.xml.gz

# lalapps_inspinj requires degrees on the command line
LONGITUDE=`python -c "import numpy; print ${RA} * 180/numpy.pi"`
LATITUDE=`python -c "import numpy; print ${DEC} * 180/numpy.pi"`
INC=`python -c "import numpy; print ${INC} * 180/numpy.pi"`
POLARIZATION=`python -c "import numpy; print ${POLARIZATION} * 180/numpy.pi"`
COA_PHASE=`python -c "import numpy; print ${COA_PHASE} * 180/numpy.pi"`

# sampler parameters
OUTPUT=cbc_example-n1e4.hdf
SEGLEN=8
PSD_INVERSE_LENGTH=4
IFOS="H1 L1"
STRAIN="H1:aLIGOZeroDetHighPower L1:aLIGOZeroDetHighPower"
SAMPLE_RATE=2048
F_MIN=30.
N_WALKERS=5000
N_ITERATIONS=1000
N_CHECKPOINT=100
PROCESSING_SCHEME=cpu
NPROCS=12
CONFIG_PATH=inference.ini

# get coalescence time as an integer
TRIGGER_TIME_INT=${TRIGGER_TIME%.*}

# start and end time of data to read in
GPS_START_TIME=$((${TRIGGER_TIME_INT} - ${SEGLEN}))
GPS_END_TIME=$((${TRIGGER_TIME_INT} + ${SEGLEN}))

# create injection file
lalapps_inspinj \
    --output ${INJ_PATH} \
    --seed 1000 \
    --f-lower ${INJ_F_MIN} \
    --waveform ${INJ_APPROX} \
    --amp-order 7 \
    --gps-start-time ${TRIGGER_TIME} \
    --gps-end-time ${TRIGGER_TIME} \
    --time-step 1 \
    --t-distr fixed \
    --l-distr fixed \
    --longitude ${LONGITUDE} \
    --latitude ${LATITUDE} \
    --d-distr uniform \
    --min-distance ${DISTANCE} \
    --max-distance ${DISTANCE} \
    --i-distr fixed \
    --fixed-inc ${INC} \
    --coa-phase-distr fixed \
    --fixed-coa-phase ${COA_PHASE} \
    --polarization ${POLARIZATION} \
    --m-distr fixMasses \
    --fixed-mass1 ${MASS1} \
    --fixed-mass2 ${MASS2} \
    --taper-injection ${TAPER} \
    --disable-spin

# run sampler
# specifies the number of threads for OpenMP
# Running with OMP_NUM_THREADS=1 stops lalsimulation
# to spawn multiple jobs that would otherwise be used
# by pycbc_inference and cause a reduced runtime.
OMP_NUM_THREADS=1 \
pycbc_inference --verbose \
    --instruments ${IFOS} \
    --gps-start-time ${GPS_START_TIME} \
    --gps-end-time ${GPS_END_TIME} \
    --psd-model ${STRAIN} \
    --psd-inverse-length ${PSD_INVERSE_LENGTH} \
    --fake-strain ${STRAIN} \
    --sample-rate ${SAMPLE_RATE} \
    --low-frequency-cutoff ${F_MIN} \
    --channel-name H1:FOOBAR L1:FOOBAR \
    --injection-file ${INJ_PATH} \
    --processing-scheme ${PROCESSING_SCHEME} \
    --sampler kombine \
    --likelihood-evaluator gaussian \
    --nwalkers ${N_WALKERS} \
    --niterations ${N_ITERATIONS} \
    --config-file ${CONFIG_PATH} \
    --output-file ${OUTPUT} \
    --checkpoint-interval ${N_CHECKPOINT} \
    --nprocesses ${NPROCS}
