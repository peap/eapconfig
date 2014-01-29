#!/bin/bash
#
# Script to run after pulling in changes to this repo; create directories and
# symlinks in local filesystem that we expect to manage.

export REPODIR=$(pwd)

source bash/post_pull_functions.sh

create_symlinks () {
    echo "Creating symlinks to $(basename $REPODIR) files for $USERNAME on $HOSTNAME..."

    safe_mkdir $HOME/.i3/
    safe_mkdir $HOME/bin/
    safe_mkdir $HOME/remotefs/

    # dot files
    link_to_git_repo $HOME/.ackrc    $REPODIR/dotfiles/ackrc
    link_to_git_repo $HOME/.bashrc   $REPODIR/dotfiles/bashrc
    link_to_git_repo $HOME/.screenrc $REPODIR/dotfiles/screenrc
    link_to_git_repo $HOME/.vimrc    $REPODIR/dotfiles/vimrc
    link_to_git_repo $HOME/.zshrc    $REPODIR/dotfiles/zshrc

    # i3
    link_to_git_repo $HOME/.i3/config     $REPODIR/dotfiles/i3-config
    link_to_git_repo $HOME/.i3status.conf $REPODIR/dotfiles/i3status.conf

    # programs/scripts
    link_to_git_repo $HOME/bin/latex2png      $REPODIR/latex/latex2png.sh
    link_to_git_repo $HOME/bin/convert_to_mp3 $REPODIR/bash/convert_to_mp3.sh
    link_to_git_repo $HOME/bin/remotefs       $REPODIR/scripts/remotefs.py
    link_to_git_repo $HOME/bin/eapy           $REPODIR/scripts/eapy/
}


SUCCESS_COUNTER=0
FAILURE_COUNTER=0
IGNORED_COUNTER=0

create_symlinks

echo "  OK: $SUCCESS_COUNTER files"
echo "FAIL: $FAILURE_COUNTER files"
echo "IGNR: $IGNORED_COUNTER files"
