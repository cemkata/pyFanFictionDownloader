#!/bin/sh

##
STARTERVER="v0.3"
APP_HOME="/opt/ficdownloader"
DIRECTORY='/mnt/ramdiskficdownloader'

# Check if running as root in a bash script
if [ `id -u` -ne 0 ];
  then echo "Please run as root"
  exit
fi

function createRAMDrive() {
  testRamDrive=`grep "RAM_DRIVE" $APP_HOME/static.py | cut -d' ' -f3`
  if [ $testRamDrive = "True" ]; then
    ###################
    ##Start Ram drive##
    ###################
    # Here, size=256M means, the RAMDISK will be 256 MB in size. To create RAMDISK of several MB, use M. For example, to create 2 GB RAMDISK, put size=2G
    SIZE=256M
    echo "Using RAM drive"
    mkramdisk="mount -t tmpfs -o rw,size=$SIZE tmpfs $DIRECTORY"
    $mkramdisk

    ###############################
    ##Create the necessary folders#
    ###############################
    if [ ! -d "$DIRECTORY" ]; then
       # Control will enter here if $DIRECTORY exists.
       echo "Creating $DIRECTORY"
       mkdir -p $DIRECTORY
    fi

    mkdir -p $DIRECTORY/output
    mkdir -p $DIRECTORY/download
  
  else
    ###################
    ##Start HDD drive##
    ###################
    echo "Using HDD drive"
    #DIRECTORY=`grep "WORKING_DIR =" static.py | cut -d' ' -f3`
  fi


}

function removeRAMDrive() {
  ##When stopping clear the ram drive
  testRamDrive=`grep "RAM_DRIVE" static.py | cut -d' ' -f3`
  if [ $testRamDrive = "True" ]; then
    # Control will enter here if $DIRECTORY exists.
    echo "Removing the ram drive."
    umount $DIRECTORY
  fi
}



case $1 in
    start)
        createRAMDrive
        break
        ;;

    stop)
        removeRAMDrive
        break
        ;;

    restart)
        removeRAMDrive
        createRAMDrive
        break
        ;;

        *)
            echo "Usage: $0 {start|stop|restart}"
            exit 1
            ;;
esac