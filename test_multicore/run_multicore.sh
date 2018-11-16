#!/usr/bin/env bash

module load python/3.7.0-miniconda pcraster/git
source activate pcraster
export LD_LIBRARY_PATH=~/install/miniconda3/envs/pcraster/lib:$LD_LIBRARY_PATH

export SCRIPT_DIR=~/git/pcraster-example/test_multicore

export PCRASTER_NR_WORKER_THREADS=1

echo
echo "New global python script"
time python $SCRIPT_DIR/compute_stats.py

export PCRASTER_NR_WORKER_THREADS=2

echo
echo "New global python script using multicore"
time python $SCRIPT_DIR/compute_stats.py

export PCRASTER_NR_WORKER_THREADS=4

echo
echo "New global python script using multicore"
time python $SCRIPT_DIR/compute_stats.py

export PCRASTER_NR_WORKER_THREADS=8

echo
echo "New global python script using multicore"
time python $SCRIPT_DIR/compute_stats.py

