#!/bin/sh

##
STARTERVER="v0.2"

#Prepere the python
PY=`which  python3`
#Prepere script name
SCRIPT='rootApp.py'
#Prepere the comand
command="$PY $SCRIPT"
#Execute the comand
$command&
