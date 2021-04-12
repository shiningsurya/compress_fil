import numpy as np
import sigpyproc as spp
import ffmpeg
import sys
import gc
#################
FIL  = sys.argv[1]
OIL  = sys.argv[2]
print (f" Input fil file  = {FIL}")
print (f" Output MP4 file = {OIL}")
GULP = 2560
NCH  = 1024
#################
pp   = (
    ffmpeg
    .input  ("pipe:", format='rawvideo', pix_fmt='gray', s='{}x{}'.format(GULP, NCH))
    .output (OIL,     format='mp4',      pix_fmt='yuv420p', r=25)
    .overwrite_output ()
    .run_async (pipe_stdin=True)
    )
#################
fil  = spp.FilReader (FIL)
rp   = fil.readPlan (GULP, verbose=True)
oo   = np.empty ((GULP, NCH,), dtype=np.uint8)
#################
NFRAMES = 0
for i,_,x in rp:
    oo[:i,:] = x.reshape ((-1, NCH))
    if i != GULP:
        oo[i:,:] = 0
    #
    pp.stdin.write (oo.tobytes())
    NFRAMES = NFRAMES + 1
    gc.collect ()
#################
print (f" Number of FRAMES = {NFRAMES}")
pp.stdin.close ()
pp.wait()
