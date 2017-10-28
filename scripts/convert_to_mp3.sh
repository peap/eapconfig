#!/bin/sh
#
# Dump music files to wav, then mp3, and rename
#
# see: http://www.linuxquestions.org/questions/linux-general-1/converting-m4a-to-mp3-170553/
#

if ! TEST=$(which mplayer) ; then 
  echo "You must install mplayer."
  exit 1
fi

if ! TEST=$(which lame) ; then
  echo "You must install lame."
  exit 2
fi

show_usage () {
    echo "usage: $0 m4a|mp4|flac|ogg|wma 128|192|320"
    echo "purpose: convert files of a given format in the current directory"
    echo "to 128, 192 or 320 kbps MP3, and delete the old files"
}

case "$1" in
  m4a|mp4|flac|ogg|wma)
    FORMAT="$1"
    ;;
  *)
    show_usage
    exit 1
    ;;
esac

case "$2" in
  128|192|320)
    BITRATE="$2"
    ;;
  *)
    show_usage
    exit 2
    ;;
esac

CWD=`pwd`

for i in *.$FORMAT
do
  if ! [ -e "$i" ] ; then
    continue
  fi
  mplayer -ao pcm "$i"
#  mplayer -ao pcm:fast:file=%`expr length "$i.wav"`%"$i.wav"
#  mplayer -ao pcm:fast:file="$1.wav" "$i"
  lame -h -b "$BITRATE" "audiodump.wav" "audiodump.mp3"
  rm audiodump.wav
  x=`echo "$i" | sed -e "s/$FORMAT/mp3/"`
  mv "audiodump.mp3" "$x"
done

NUMFILES=`ls -1 *.$FORMAT 2>/dev/null | wc -l`

if [ $NUMFILES -gt 0 ] ; then
  echo "Removing $FORMAT files..."
  rm *.$FORMAT
else
  echo "No $FORMAT files found in $CWD."
fi

exit 0
