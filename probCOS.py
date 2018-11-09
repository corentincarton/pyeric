from pcraster import *
from pcraster.framework import *
import sys

# Sum COSMO boolean maps and calculate the probability
#
# usage: python probCOS.py <Step> <prefixIn> <prefixOut> <rootdir> <folder date> <CLEPS version folder>
# e.g:   python probCOS.py 016 Kp2Alert Kp2Prob0 '\nahaUsers\raynada\ERIC_2013\CaseStudies' 20101031 

class Prob_Model(StaticModel):
  def __init__(self, cloneMap,timestep,infile,outfile,direc,ens_mems):
    StaticModel.__init__(self)
    setclone(cloneMap)
    self.timestep = timestep
    self.infile = infile
    self.outfile = outfile
    self.direc = direc
    self.ens_mems = ens_mems

  def initial(self):
    for i in range(self.ens_mems):
      if i == 0:
        self.KpSum = scalar(readmap(self.direc+'/'+str(i+1)+'/'+self.infile+'.'+self.timestep))
      else:
        self.KpSum = self.KpSum + scalar(readmap(self.direc+'/'+str(i+1)+'/'+self.infile+'.'+self.timestep))
    
    self.KpProbOut = self.KpSum / self.ens_mems
    
    self.report(self.KpProbOut, self.direc + '/' + self.outfile)

tstep = sys.argv[1]
input_fname = sys.argv[2]
output_fname = sys.argv[3]
directory = sys.argv[4]
nENS = int(sys.argv[5])

myModel = Prob_Model(directory + "/area.map",tstep,input_fname,output_fname,directory,nENS)
stModelFw = StaticFramework(myModel)
stModelFw.run()
