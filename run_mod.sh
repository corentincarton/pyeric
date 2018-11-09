#!/usr/bin/env bash

echo "Calling old scripts for mean (python)" 
for i in {3..20}
do
  t=$(printf '%0.3d\n' $i)
  echo $t
  python probCOS.py $t Kp1Alert Kp1Prob0_$i . 20
  mv Kp1Prob0_$i.map Kp1Prob0.$t
done

echo "Calling old scripts for max" 
pcrcalc -f max.mod 3 20 Kp1Prob . .

#echo
#echo "New python script for max"
#time python max.py
#diff Kp1Prob_max.map Kp1Prob.map
