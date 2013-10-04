#!/bin/bash
#
# (un)mount a remote filesystem over SSH at ~/remotefs
#

if ! TEST=$(which sshfs) ; then
    echo "You must install sshfs."
    exit 1
fi

REMOTE_HOST=$1
ACTION=$2

MOUNT_BASE=~/remotefs
MOUNT_DIR="$MOUNT_BASE/$REMOTE_HOST"

show_usage () {
    echo "usage: $0 <target> up|down"
}

if [ -z "$REMOTE_HOST" ] ; then
    echo "No target specified!"
    show_usage 
    exit 2
fi

if [ -z "$ACTION" ] ; then
    echo "No action specified!"
    show_usage 
    exit 3
fi

case $ACTION in
    up)
        if [ ! -d "$MOUNT_DIR" ] ; then
            mkdir -p $MOUNT_DIR
        fi
        sshfs "$REMOTE_HOST:/" $MOUNT_DIR
        ;;
    down)
        fusermount -u $MOUNT_DIR && rmdir $MOUNT_DIR
        ;;
    *)
        echo "Invalid value for \$ACTION: $ACTION"
        show_usage 
        exit 4
        ;;
esac

exit 0
