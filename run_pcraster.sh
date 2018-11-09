#!/usr/bin/env bash

function diff_mean() {
  for i in {3..20}
  do
    t=$(printf '%0.3d\n' $i)
    diff Kp1Prob_mean.$t Kp1Prob0.$t
  done
}
 
module unload python
module load python pcraster/4.0.1
#module load python/3.7.0-miniconda pcraster/git
#source activate pcraster
#export LD_LIBRARY_PATH=~/install/miniconda3/envs/pcraster/lib:$LD_LIBRARY_PATH

export SCRIPT_DIR=~/git/pcraster-example

echo
echo "Calling old scripts (python and mod)" 
time $SCRIPT_DIR/run_mod.sh

echo
echo "New global python script"
time python $SCRIPT_DIR/compute_stats.py
diff Kp1Prob_max.map Kp1Prob.map
diff_mean

