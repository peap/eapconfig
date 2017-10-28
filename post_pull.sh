#!/bin/bash

###
# Script to run after pulling in changes to this repo; create directories and
# symlinks in local filesystem that we expect to manage.
###

_repo=$(pwd)

source bash/post_pull_functions.sh

create_symlinks () {
    echo -n "Creating directories and symlinks for $(basename $_repo) "
    echo "on behalf of $(whoami) on $(hostname)..."

    safe_mkdir $HOME/.vimswp/
    safe_mkdir $HOME/bin/
    safe_mkdir $HOME/bin/py3status/
    safe_mkdir $HOME/remotefs/

    # dot files
    link_to_git_repo $HOME/.ackrc        $_repo/dotfiles/ackrc
    link_to_git_repo $HOME/.bashrc       $_repo/dotfiles/bashrc
    link_to_git_repo $HOME/.bash_profile $_repo/dotfiles/bash_profile
    link_to_git_repo $HOME/.inputrc      $_repo/dotfiles/inputrc
    link_to_git_repo $HOME/.profile      $_repo/dotfiles/profile
    link_to_git_repo $HOME/.pylintrc     $_repo/dotfiles/pylintrc
    link_to_git_repo $HOME/.screenrc     $_repo/dotfiles/screenrc
    link_to_git_repo $HOME/.vimrc        $_repo/dotfiles/vimrc
    link_to_git_repo $HOME/.Xresources   $_repo/dotfiles/Xresources
    link_to_git_repo $HOME/.zshrc        $_repo/dotfiles/zshrc

    # i3
    link_to_git_repo $HOME/bin/i3-suspend $_repo/scripts/i3-suspend.sh

    # programs/scripts
    link_to_git_repo $HOME/bin/latex2png      $_repo/latex/latex2png.sh
    link_to_git_repo $HOME/bin/convert_to_mp3 $_repo/scripts/convert_to_mp3.sh
    link_to_git_repo $HOME/bin/remotefs       $_repo/scripts/remotefs.py
    link_to_git_repo $HOME/bin/random_words   $_repo/scripts/random_words.py
    link_to_git_repo $HOME/bin/eapy           $_repo/scripts/eapy/
}

if [ ! $SUCCESS_COUNTER ] ; then
    SUCCESS_COUNTER=0
    FAILURE_COUNTER=0
    IGNORED_COUNTER=0
    local_counters_only="yep"
fi

create_symlinks

if [ $local_counters_only ] ; then
    echo "  OK: $SUCCESS_COUNTER files"
    echo "FAIL: $FAILURE_COUNTER files"
    echo "IGNR: $IGNORED_COUNTER files"
fi
