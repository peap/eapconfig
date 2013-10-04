#!/bin/bash
#
# (un)mount a remote filesystem over SSH at ~/remotefs
#

MOUNT_BASE=~/remotefs

show_usage () {
    echo "usage: $0 <target> up|down"
    exit 1
}

if [ -z "$1" ] ; then
    echo "No target specified!"
    show_usage 
fi

case "$2" in
    "up") ACTION=up ;;
    "down") ACTION=down ;;
    *) show_usage  ;;
esac

MOUNT_DIR="$MOUNT_BASE/$2"

case $ACTION in
    up)
        if [ ! -d "$2" ] ; then
            mkdir -p $MOUNT_DIR
        fi
        sshfs "$2:/" $MOUNT_DIR
        ;;
    down)
        fusermount -u $MOUNT_DIR && rmdir $MOUNT_DIR
        ;;
    *)
        echo "Impossible value for \$ACTION: $ACTION"
        show_usage 
        ;;
esac

exit 0
