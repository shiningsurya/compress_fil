import sys
import gc
import numpy as np

import ffmpeg
import sigpyproc as spp
#################
MP4  = sys.argv[1]
FIL  = sys.argv[2]
REF  = "/data/01_NGC6440_cdp_02sep2018_bs5_80us.fil"
print (MP4,FIL)
GULP = 2560
NCH  = 1024
M_FRAME = GULP * NCH
#################
pp   = (
    ffmpeg
    .input  (MP4)
    .output ('pipe:', format='rawvideo', pix_fmt='gray')
    .run_async (pipe_stdout=True)
    )
#################
ril  = spp.FilReader (REF)
rh   = ril.header.SPPHeader ()
ofil = spp.Utils.File (FIL, 'w', nbits=8)
ofil.write (rh)
jj   = np.zeros ((GULP,NCH), dtype=np.uint8)
#################
NFRAMES = 0
while True:
    in_bytes = pp.stdout.read (M_FRAME)
    if len(in_bytes) <= 0:
        break
    ii = np.frombuffer (in_bytes, np.uint8).reshape ((GULP,NCH))
    jj[:,:] = ii[:,:]
    ofil.cwrite (jj)
    NFRAMES = NFRAMES + 1
    gc.collect()
print ("NFRAMES = ", NFRAMES)
pp.stdout.close ()
pp.wait()
ofil.close ()
#################
