#!/usr/bin/env bash

#echo "Calling old scripts for mean (python)" 
#for i in {3..20}
#do
#  t=$(printf '%0.3d\n' $i)
#  echo $t
#  python $SCRIPT_DIR/eric/probCOS.py $t Kp1Alert Kp1Prob0_$i . 20
#  mv Kp1Prob0_$i.map Kp1Prob0.$t
#done

#echo "Calling old scripts for max" 
#pcrcalc -f $SCRIPT_DIR/eric/max.mod 3 20 Kp1Prob . .

#echo
#echo "New python script for max"
#time python max.py
#diff Kp1Prob_max.map Kp1Prob.map

time pcrcalc "Kp1P_2018.map"'='"if(Kp1Prob.map gt 0,Kp1Prob.map * 100)"

time pcrcalc "Kp1PX_2018.map"'='"subcatchment(ldd.map,ordinal(Kp1P_2018.map))"

MemberMin1=4
MemberMin2=3
time pcrcalc -f $SCRIPT_DIR/eric/FFRepPoints.mod . 2018 $MemberMin1 $MemberMin2 . 20 

pcrcalc "RepP.map"'='"nominal(uniqueid(if(defined(RepP1.map) then 1)))"
pcrcalc "UpsRepP.map"'='"if(boolean(RepP.map),ups.map)"    #Upstream area of Reporting points - Threshold 1
pcrcalc "RepP1x.map"'='"if(defined(RepP1.map) then RepP.map)"

map2col --coorcentre -s , RepP1.map RepP1x.map RepP1_2018.txt
map2col --coorcentre -s , RepP.map  RepP_2018.txt
map2col --coorcentre -s , RepP.map  UpsRepP.map UpsRepP_2018.txt

