from pcraster import *
from pcraster.framework import *
from numpy import *
from decimal import Decimal

print("Number of threads: " + str(nr_worker_threads()))
def format_e(n):
    a = '%e' % n
    return a.split('e')[0].rstrip('0').rstrip('.') + 'e' + a.split('e')[1]

def num2txt(fn, na, x, y, *maps):
  ni = len(x)
  nj = len(x[0])
  if (len(y) != ni or len(y[0]) != nj):
    print("Error! Number of data in y not coherent!")
    print("x=(" + str(ni) + "," + str(nj) + ")")
    print("y=(" + str(len(y)) + "," + str(len(y[0])) + ")")
    exit(1)
  for map in maps:
    if (len(map) != ni or len(map[0]) != nj):
      print("Error! Number of data in map not coherent!")
      exit(1)

  f = open(fn, 'w')

  for i in arange(ni):
    for j in arange(nj):
      exist = False
      for map in maps:
        if (map[i][j] != na):
          exist = True
      
      if exist:
        f.write("%2.4e," % x[i][j] + "%2.4e" % y[i][j])
        f.write("," + str(map[i][j]))        
#        for map in maps:
#          if (map[i][j] > 1e4):
#            f.write(','+format_e(map[i][j]))
#          else:  
#            f.write(",%d" % map[i][j])
        f.write("\n")

  print("Calling with map " + str(len(maps)))

def MaxTimeEnsemble(ens, time):
  mapmax = scalar(0)
  for t in time:
    print('Timestep: ' + str(t))
  
    mapmean = scalar(0)
    for e in ens:
      mapval = readmap(str(e) + '/Kp1Alert.{:03}'.format(t))
      mapmean = mapmean + mapval
    mapmean = mapmean/nens
    #report(mapmean, 'Kp1Prob_mean.{:03}'.format(t))

    mapmax = max(mapmax, mapmean)
  
  return mapmax


setclone('area.map')

ldd = readmap('ldd.map')
grad = readmap('gradient.map')
ups = readmap('ups.map')

nens = 20
ens = arange(1, nens+1)

tstart = 3
tend = 20
time = arange(tstart, tend+1)

#mapmax = MaxTimeEnsemble(ens, time)
#report(mapmax, "Kp1Prob_max.map")
mapmax = readmap("Kp1Prob_max.map")

mapmax100 = ifthen((mapmax > 0), mapmax*100)
#report(mapmax100, "Kp1Prob_max100.map")

mapsub = subcatchment(ldd, ordinal(mapmax100))
#report(mapsub, "Kp1Sub.map")

print(mapsub)

# Filter parameters
gradFF = 0.03
MemberTH1 = 4
upsmin = 50000000

threshold = MemberTH1*100/nens

Kp1PaT = (mapmax100 >= MemberTH1*100/nens)
Kp1PaT2 = catchment(ldd, Kp1PaT)
Kp1PaT1 = ifthen(Kp1PaT2, clump(Kp1PaT2))
LDDKp1P = lddmask(ldd, boolean(Kp1PaT1))
MaxGrad1 = areamaximum(grad, Kp1PaT1)
gr1Mask = ifthen(MaxGrad1 > gradFF, boolean(1))
RepP1 = ifthen(boolean(pit(LDDKp1P)) & boolean(gr1Mask) & (ups > upsmin), mapmax100)
report(RepP1, "RepP1_py.map")

RepP = nominal(uniqueid(ifthen(defined(RepP1), boolean(1))))
#report(RepP, "RepP_py.map")
UpsRepP = ifthen(boolean(RepP), ups)
#report(UpsRepP, "UpsRepP_py.map")
RepP1x = ifthen(defined(RepP1), RepP)
#report(RepP1x, "RepP1x_py.map")

na = -9999
RepP_num = pcr2numpy(RepP, na)
RepP1_num = pcr2numpy(RepP1, na)
RepP1_num = RepP1_num.astype(int)
RepP1x_num = pcr2numpy(RepP1x, na)
UpsRepP_num = pcr2numpy(UpsRepP, na)
UpsRepP_num = UpsRepP_num.astype(int)
ni = len(RepP_num)
nj = len(RepP_num[0])

x = xcoordinate(boolean(RepP))
y = ycoordinate(boolean(RepP))
x_num = pcr2numpy(x, na)
y_num = pcr2numpy(y, na)

num2txt("RepP1_py.txt", na, x_num, y_num, RepP1_num, RepP1x_num)
num2txt("RepP_py.txt", na, x_num, y_num, RepP_num)
num2txt("UpsRepP_py.txt", na, x_num, y_num, RepP_num, UpsRepP_num)

