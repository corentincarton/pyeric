#from pcraster import *
from pcraster.framework import *
from numpy import *
from pcraster.multicore import *

import time as systime
print("Number of threads: " + str(nr_worker_threads()))

setclone('area.map')

nens = 20
ens = arange(1, nens+1)

tstart = 3
tend = 20
time = arange(tstart, tend+1)

mapmax = scalar(0)
maptime = []
for t in time:
  mapens = []
  for e in ens:
    mapens.append(readmap(str(e) + '/Kp1Alert.{:03}'.format(t)))
  maptime.append(mapens)
    
start_time = systime.time()

i = 0
for t in time:
  #print('Timestep: ' + str(t))
  
  mapmean = scalar(0)
  j = 0
  for e in ens:
    #print('Accumulating ensemble ' + str(e))
    mapval = maptime[i][j]
#    mapval = readmap(str(e) + '/Kp1Alert.{:03}'.format(t))
    mapmean = mapmean + mapval
    j=j+1
  mapmean = mapmean/nens
#  report(mapmean, 'Kp1Prob_mean.{:03}'.format(t))

  mapmax = max(mapmax, mapmean)
  i=i+1

#report(mapmax, "Kp1Prob_max.map")

print("--- %s seconds ---" % (systime.time() - start_time))
