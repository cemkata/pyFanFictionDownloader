#!/bin/sh

##
STARTERVER="v0.5"

#Prepere the python
PY=`which  python3`
#Prepere script name
SCRIPT='rootApp.py'
#Prepere the comand
command="$PY $SCRIPT"



# Check if running as root in a bash script
if [ `id -u` -ne 0 ];
  then echo "Please run as root"
  exit
fi

DIRECTORY=`grep "WORKING_DIR =" static.py | cut -d' ' -f3`
echo $DIRECTORY

## Debuging
##mkdir -p $DIRECTORY
##

exit


test=`grep "RAM_DRIVE" static.py | cut -d' ' -f3`
if [ $test = "True" ]; then
  echo "Using RAM drive"
exit
  ###################
  ##Start Ram drive##
  ###################
  DIRECTORY='/mnt/ramdiskficdownloader'

  # Here, size=256M means, the RAMDISK will be 256 MB in size. To create RAMDISK of several MB, use M. For example, to create 2 GB RAMDISK, put size=2G
  SIZE=256M

  if [ ! -d "$DIRECTORY" ]; then
    # Control will enter here if $DIRECTORY exists.
    echo "Creating $DIRECTORY"
    mkdir $DIRECTORY
  fi

  mkdir $DIRECTORY/output
  mkdir $DIRECTORY/download

  mkramdisk="mount -t tmpfs -o rw,size=$SIZE tmpfs $DIRECTORY"
  $mkramdisk
###################
##End Ram drive  ##
###################
else
  echo "Using HDD drive"
fi

exit

umount $DIRECTORY

#Execute the comand
$command
