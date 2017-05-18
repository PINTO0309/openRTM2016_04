#!/bin/sh

#Assign result to variable
A=$(ps -aux | grep "Zumo" | grep -v grep)

#Confirm whether characters are include
#Rewrite file
if echo ${A} | grep "Zumo" ; then
echo -n "Active"> /home/pi/stateComp.txt
else
echo -n "Deactive"> /home/pi/stateComp.txt
fi