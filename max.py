from pcraster import *
from pcraster.framework import *
from numpy import *
import netCDF4 as nc4

class MaxModel(DynamicModel):

  def __init__(self, clonemap):
    DynamicModel.__init__(self)
    setclone(clonemap)
    self.maxmap = "Kp1Prob_max.map"

  def initial(self):
    self.max = scalar(0)

  def dynamic(self):
    value = self.readmap("Kp1Prob")
    self.max = max(self.max, value)
#    report(self.max, self.maxmap)

  def write(self):
    report(self.max, self.maxmap)

myModel = MaxModel("area.map")
dynModelFw = DynamicFramework(myModel, firstTimestep=3, lastTimeStep=20)
dynModelFw.run()

myModel.write()
