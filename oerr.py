import numpy as np
import pandas as pd

import sigpyproc as spp

from skimage.metrics import structural_similarity as ssim
import sys
import gc
#################
FIL  = sys.argv[1]
OIL  = sys.argv[2]
EIL  = sys.argv[3]
GULP = 25600
#################
fil  = spp.FilReader (FIL)
frp  = fil.readPlan (GULP, verbose=True)
oil  = spp.FilReader (OIL)
orp  = oil.readPlan (GULP, verbose=True)
f_nc = fil.header['nchans']
o_nc = fil.header['nchans']
#################
MSE  = []
SSE  = []
SSIM = []
#################
NFRAMES = 0
fb     = np.zeros ((GULP, f_nc), dtype=np.uint8)
ob     = np.zeros ((GULP, o_nc), dtype=np.uint8)
for fread, oread in zip(frp, orp):
    fi,_,fx = fread
    oi,_,ox = oread
    fb[:fi,:] = fx.reshape ((-1, f_nc))
    if fi != GULP:
        fb[fi:,:] = 0
    ob[:oi,:] = ox.reshape ((-1, o_nc))
    if oi != GULP:
        ob[oi:,:] = 0
    #
    db  = np.power (fb - ob,2)
    MSE.append (np.mean (db))
    SSE.append (np.sum (db))
    SSIM.append (ssim (fb, ob))
    #
    NFRAMES = NFRAMES + 1
    gc.collect ()
#################
df = pd.DataFrame ({'mse':MSE, 'sse':SSE, 'ssim':SSIM})
df.to_pickle (EIL)
