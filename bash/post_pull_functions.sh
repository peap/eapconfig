#!/bin/bash
#
# Functions for tasks like creating symlinks and setting permissions after
# pulling in changes to a repo.
#

_count_success () {
    # Call after a command to increment a success counter
    SUCCESS_COUNTER=$((SUCCESS_COUNTER+1))
}

_count_failure () {
    # Call after a command to increment a failure counter
    FAILURE_COUNTER=$((FAILURE_COUNTER+1))
}

_count_ignored () {
    # Call after a command to increment an ignored operations counter
    IGNORED_COUNTER=$((IGNORED_COUNTER+1))
}

count_result () {
    if [ "$?" -eq "0" ] ; then
        _count_success
    else
        _count_failure
    fi
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

chmod_if_changed () {
    new_perms=$1
    file=$2

    if [ "$OSTYPE" = "msys" ] ; then
        # don't bother; windows file perms are not UNIXy
        _count_ignored && return 0
    fi

    curr_perms=$(stat -c "%a" $file)

    if [ "$new_perms" = "$curr_perms" ] ; then
        _count_success && return 0
    else
        result=$(chmod $new_perms $file)
        if [ $? -eq 0 ] ; then
            _count_success
            echo "  OK: Set permissions to $new_perms for $file"
            return 0
        else
            _count_failure
            echo "FAIL: $result"
            return 1
        fi
    fi
}

chmod_children_if_changed () {
    new_perms=$1
    directory=$2

    if [ ! -d $directory ] ; then
        echo "FAIL: Not a directory -> $directory"
    fi

    find $directory -type f | while read file; do chmod_if_changed $new_perms "$file"; done
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

link_to_git_repo_per_host () {
    LOCALFILE=$1
    REPOFILE=$2

    REPOFILE_FOR_HOST="${REPOFILE}-${HOSTNAME}"
  
    if [ -e $REPOFILE_FOR_HOST ] ; then
        link_to_git_repo $LOCALFILE $REPOFILE_FOR_HOST
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
  
    if [ "$OSTYPE" = "msys" ] ; then
        # Until I figure out if I can really use mklink, let's just remove the
        # file/directory and create a new copy. These changes should be confirmed.
        rm -rf $LOCALFILE
        cp -a $REPOFILE $LOCALFILE
        _count_success && return 0
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

