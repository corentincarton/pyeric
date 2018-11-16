# Select points to report possible flash floods to occur from Kp1P.map and Kp2P.map
# Then these points are exported through a table
#
# usage: pcrcalc -f FFRepPoints.mod <workdir> <date> <nmin members - TH_med> <nmin members - TH_high> <static maps folder>
# e.g:   pcrcalc -f FFRepPoints.mod './' 2010111600 4 3 /gpfs/r_lxab/efas/emos/efas/lib/ff/maps/20y7km


binding
 Kp1P = $1\Kp1P_$2.map;	#Threshold exceedance probability - Medium Threshold
 Kp2P = $1\Kp2P_$2.map;	#Threshold exceedance probability - High Threshold
 
 area = $5\area.map;
 grad = $5\gradient.map;
 Ldd = $5\ldd.map;
 Ups = $5\ups.map;
 
 RepP1 = $1\RepP1.map;
 RepP2 = $1\RepP2.map;
 
 nENS = $6;
 
areamap
 area; 

timer
 1 1 1;
 
initial
 gradFF = 0.03;	 #Minimum gradient for having a Flash Flood
 MemberTH1 = $3;	 #Minimum number of members for having a Reporting Point (Medium threshold)
# MemberTH2 = $4;	 #Minimum number of members for having a Reporting Point (High threshold)
 upsmin = 50000000; #Minimum catchment size for creating a reporting point (m^2)

dynamic
 
 Kp1PaT = (Kp1P ge MemberTH1*100/nENS); 	#Kp1PG above Threshold 1
# Kp2PaT = (Kp2P ge MemberTH2*100/nENS); 	#Kp2PG above Threshold 2
 
 Kp1PaT2=catchment(Ldd,Kp1PaT);	 #Cos prendo solo un punto anche se ho diversi threshold exceedances (disconnessi) pi a monte
# Kp2PaT2=catchment(Ldd,Kp2PaT);
 
 Kp1PaT1 = if(Kp1PaT2,clump(Kp1PaT2));	#Raggruppo insieme
# Kp2PaT1 = if(Kp2PaT2,clump(Kp2PaT2));
 
 LDDKp1P = lddmask(Ldd,boolean(Kp1PaT1));
# LDDKp2P = lddmask(Ldd,boolean(Kp2PaT1));
 
 MaxGrad1 = areamaximum(grad, Kp1PaT1);	 #Maximum gradient for each catchment where Kp1PG above Threshold 1
# MaxGrad2 = areamaximum(grad, Kp2PaT1);

 gr1Mask = if(MaxGrad1 > gradFF ,scalar(1));	 #Mask based on the maximum gradient of the catchment
# gr2Mask = if(MaxGrad2 > gradFF ,scalar(1)); 
 
 report RepP1 = if(boolean(pit(LDDKp1P)) and boolean(gr1Mask) and (Ups > upsmin),Kp1P);	 #Reporting points - Threshold 1
# report RepP2 = if(boolean(pit(LDDKp2P)) and boolean(gr2Mask) and (Ups > upsmin),Kp2P);	 #Reporting points - Threshold 2
 
