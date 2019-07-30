#!/bin/sh

STARTERVER="v1.0"
SCRIPT='rootApp.py'
components=$SCRIPT
APP_HOME="/opt/ficdownloader"
cd $APP_HOME
pid="0"

function printUsage() {
cat 1>&2 <<EOT

usage: $0 {status|start|stop|restart} [ component ]

  status    Returns the status of the system or a single component.
  start     Starts the system or a single component.
  stop      Stops the system or a single component.
  restart   Restarts the system or a single component.
  
EOT

    echo -n "Components: " $components
    echo
}

function serverStatus() {
    pid=`ps -ef | grep "$SCRIPT" | grep -v "grep"  | head -n 1 | awk '{print $2}' 2>>/dev/null`

    if [ -z "$pid" ];
    then
        if [ "$silent" != "true" ]
        then
            echo $SCRIPT" is not up and running">&2
        fi
        pid=0
    else
        if [ "$silent" != "true" ]
        then
            echo $SCRIPT" is running with pid: " $pid >&2
        fi
    fi
}

function serverStop() {
    serverStatus true
    if [ "$pid" != "0" ]
    then
        kill -9 $pid
        echo $SCRIPT" is stopped"
    else
        echo $SCRIPT" is not up and running"
    fi
}

function serverStart() {
    serverStatus true
    if [ "$pid" = "0" ]
    then
        #Prepare the python#
        PY=`which  python3`
        #Prepare the command
        command="$PY $SCRIPT"
        #Execute the comand
        $command
        echo $SCRIPT" is started"
    else
        echo $SCRIPT" is already running"
    fi
}

function status() {
    case $1 in
    server)
        serverStatus
        ;;
    esac
}

function stop() {
    case $1 in
    server)
        serverStop
        ;;
    esac
}

function start() {
    case $1 in
    server)
        serverStart
        ;;
    esac
}

## check arguments begin ----------------

case $1 in
    status|start|stop|restart)

    if [ "$2" != "" ]
    then
        FOUND="false"
        for i in $components
        do
           if [ "$2" = "$i" ]
           then
                FOUND="true"
                break
           fi
        done
        if [ "$FOUND" = "false" ]
        then
            printUsage
            echo -n $2

        fi
    fi
esac

case $1 in
    start)
        if [ "$2" = "" ]
        then
            for comp in $components
            do
              start $comp
            done
        else
            start $2
        fi
        ;;

    stop)
        if [ "$2" = "" ]
        then
            for comp in $components
            do
              stop $comp
            done
        else
            stop $2
        fi
        ;;

    restart)
        if [ "$2" = "" ]
        then
            for comp in $components
            do
              stop $comp
              echo
              start $comp
            done
        else
            stop $2
        fi
        ;;

    status)
        if [ "$2" = "" ]
        then
        for comp in $components
        do
          status $comp
        done
        else
            status $2
        fi
        ;;

        *)
            echo "Usage: $0 {start|stop|status|restart} {server}"
            exit 1
            ;;
esac
