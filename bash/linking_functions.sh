#!/bin/bash
#
# Functions for creating links in the filesystem to files in this repository.
#

_count_success () {
    # Call after a command to increment a success counter
    if [ $? -eq 0 ] ; then
        SUCCESS_COUNTER=$((SUCCESS_COUNTER+1))
    fi
}

_count_failure () {
    # Call after a command to increment a failure counter
    FAILURE_COUNTER=$((FAILURE_COUNTER+1))
}

_safe_to_create_link () {
    # Inspect a proposed link path to check whether or not a link could be
    # created there
    #
    # Return values:
    #   0: nothing exists
    #   1: a link exists
    #   2: an actual file exists

    LNPATH=$1
    if [ -h $LNPATH ] ; then
        echo "File is already a symlink. ($LNPATH)"
        return 1
    fi
    if [ -e $LNPATH ] ; then
        echo "Actual file exists. ($LNPATH)"
        return 2
    fi
    return 0
}

safe_mkdir () {
    # Wrapper around mkdir so we can ignore existing directories

    NEWDIR=$1
    if [ -d $NEWDIR ] ; then
        return 0
    else
        mkdir -p $NEWDIR
    fi
}

link_to_git_repo () {
  # Create a symlink in the local filesystem to a file in this repo
  #
  # Example: link_to_git_repo .bashrc bash/bashrc

  LOCALFILE=$1
  REPOFILE=$2

  if [ -z $REPOFILE ] ; then
    echo "FAIL: No repository file provided for linking to. ($LOCALFILE)"
    _count_failure && return 1
  fi

  if [ ! -e $REPOFILE ] ; then
    echo "FAIL: Given repository file does not exist! ($REPOFILE)"
    _count_failure && return 2
  fi

  result=$(_safe_to_create_link $LOCALFILE)
  code=$?

  if [ $code -eq 0 ] ; then
    link_result=$(ln -s $REPOFILE $LOCALFILE)
    success=$?
    if [ $success -eq 0 ] ; then
      echo "  OK: Created link: $LOCALFILE --> $REPOFILE"
      _count_success && return 0
    else
      echo "FAIL: Could not create link. Reason: $link_result"
      _count_failure && return 3
    fi
  else
    if [ $code -eq 1 ] ; then
      current_link=`readlink $LOCALFILE`
      proposed_link=$REPOFILE
      if [ $current_link = $proposed_link ] ; then
        _count_success && return 0
        #echo "  OK: No need to create link: $result"
      else
        echo "FAIL: Existing link points to different file. ($current_link)."
        _count_failure && return 4
      fi
    else
      echo "FAIL: Did not create link. Reason: $result"
      _count_failure && return 5
    fi
  fi
}

