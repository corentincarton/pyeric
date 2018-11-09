from pcraster import *
from pcraster.framework import *
from numpy import *

setclone('area.map')

nens = 20
ens = arange(1, nens+1)

tstart = 3
tend = 20
time = arange(tstart, tend+1)

mapmax = scalar(0)
for t in time:
  print('Timestep: ' + str(t))
  
  mapmean = scalar(0)
  for e in ens:
    #print('Accumulating ensemble ' + str(e))
    mapval = readmap(str(e) + '/Kp1Alert.{:03}'.format(t))
    mapmean = mapmean + mapval
  mapmean = mapmean/nens
  report(mapmean, 'Kp1Prob_mean.{:03}'.format(t))

  mapmax = max(mapmax, mapmean)

report(mapmax, "Kp1Prob_max.map")
