import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mc
import sigpyproc as spp
import pickle as pkl
import gc
#################
PNG  = "err/frame_{}.png"
FIL  = "./2010-12-12-03:46:51.fil"
OIL  = "./test_2bit.fil"
GULP = 256000
NCH  = 1024
#################
fil  = spp.FilReader (FIL)
frp  = fil.readPlan (GULP, verbose=True)
oil  = spp.FilReader (OIL)
orp  = oil.readPlan (GULP, verbose=True)
ERR  = []
#################
NFRAMES = 0
fb     = np.zeros ((GULP, NCH), dtype=np.uint8)
ob     = np.zeros ((GULP, NCH), dtype=np.uint8)
for fread, oread in zip(frp, orp):
    fi,_,fx = fread
    oi,_,ox = oread
    fb[:fi,:] = fx.reshape ((-1, NCH))
    if fi != GULP:
        fb[fi:,:] = 0
    ob[:oi,:] = ox.reshape ((-1, NCH))
    if oi != GULP:
        ob[oi:,:] = 0
    #
    # ob  = ob / 84
    db  = fb - ob
    err = np.mean (db)
    ERR.append (err)
    print ("NFRAME:", NFRAMES, " err:",err)
    #
    NFRAMES = NFRAMES + 1
    gc.collect ()
#################
print ("")
print ("NFRAMES = ", NFRAMES)
np.save ("oerr.npy", np.array (ERR))
