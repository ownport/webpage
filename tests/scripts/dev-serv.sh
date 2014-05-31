#!/bin/sh
#
#	start/stop bottle server
#

NAME=dev-serv.py
DEV_SERV_PATH=`pwd`/tests
DEV_SERV=$DEV_SERV_PATH/bin/$NAME
PIDFILE=$DEV_SERV_PATH/run/$NAME.pid
DEV_SERV_LOG=$DEV_SERV_PATH/logs/dev-server.log
OPTIONS=" --logfile=$DEV_SERV_LOG --datapath=$DEV_SERV_PATH/data/"

test -f $DEV_SERV || exit 0

. /lib/lsb/init-functions

case "$1" in

    start)  
        log_daemon_msg "Starting dev-server" "dev-server"
        start-stop-daemon --start --quiet -b -m --pidfile $PIDFILE --startas $DEV_SERV -- $OPTIONS
        log_end_msg $?
        ;;

    stop)  
        log_daemon_msg "Stopping dev-server" "dev-server"
        start-stop-daemon --stop --quiet --pidfile $PIDFILE
        log_end_msg $?
        ;;

    restart|reload|force-reload)
        log_daemon_msg "Restarting dev-server" "dev-server"
        start-stop-daemon --stop --retry 5 --quiet --pidfile $PIDFILE
        start-stop-daemon --start --quiet -b -m --pidfile $PIDFILE --startas $DEV_SERV -- $OPTIONS
        log_end_msg $?
        ;;

    status)
        status_of_proc -p $PIDFILE $DEV_SERV dev-serv && exit 0 || exit $?
        ;;

    *)
        log_action_msg "Usage: dev-serv.sh {start|stop|restart|reload|force-reload|status}"
        exit 2
        ;;
esac
exit 0