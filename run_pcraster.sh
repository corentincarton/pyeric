#!/usr/bin/env bash

function diff_mean() {
  for i in {3..20}
  do
    t=$(printf '%0.3d\n' $i)
    diff Kp1Prob_mean.$t Kp1Prob0.$t
  done
}
 
PCRASTER_INSTALL=~/install/pcraster-git
ENV_ROOT=~/install/miniconda3/envs/pcraster
 
source activate pcraster
conda env list
 
export PYTHONPATH=$PCRASTER_INSTALL/python:$PYTHONPATH
export LD_LIBRARY_PATH=$PCRASTER_INSTALL/lib:$LD_LIBRARY_PATH
export PATH=$PCRASTER_INSTALL/bin:$PATH
export LD_LIBRARY_PATH=$ENV_ROOT/lib:$LD_LIBRARY_PATH

echo
echo "Calling old scripts (python and mod)" 
time ./run_mod.sh

echo
echo "New global python script"
time python compute_stats.py
diff Kp1Prob_max.map Kp1Prob.map
diff_mean

