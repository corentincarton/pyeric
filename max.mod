# Maximum value of a map stack 
#
# usage: pcrcalc -f max.mod <StartStep> <EndStep> <prefix> <mapsdir> <workdir>


binding

 MaxVal = $5\$3.map;

 Val = $5\$3;

 area = $4\area.map;

areamap
 area;

timer
 $1 $2 1;

initial
 MaxVal = scalar(0);

dynamic
 ValIn = timeinput(Val);
 report MaxVal = max(MaxVal,ValIn);
