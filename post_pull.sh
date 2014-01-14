#!/bin/bash
#
# Script to run after pulling in changes to this repo; create directories and
# symlinks in local filesystem that we expect to manage.

export REPODIR=$(pwd)

# safe_mkdir, link_to_git_repo
source bash/linking_functions.sh

create_symlinks () {
    safe_mkdir $HOME/bin/
    safe_mkdir $HOME/remotefs/

    # dot files
    link_to_git_repo $HOME/.ackrc    $REPODIR/dotfiles/ackrc
    link_to_git_repo $HOME/.bashrc   $REPODIR/dotfiles/bashrc
    link_to_git_repo $HOME/.screenrc $REPODIR/dotfiles/screenrc
    link_to_git_repo $HOME/.vimrc    $REPODIR/dotfiles/vimrc
    link_to_git_repo $HOME/.zshrc    $REPODIR/dotfiles/zshrc

    # programs/scripts
    link_to_git_repo $HOME/bin/latex2png      $REPODIR/latex/latex2png.sh
    link_to_git_repo $HOME/bin/convert_to_mp3 $REPODIR/bash/convert_to_mp3.sh
    link_to_git_repo $HOME/bin/remotefs       $REPODIR/bash/remotefs.sh
}

SUCCESS_COUNTER=0
FAILURE_COUNTER=0
echo "Creating symlinks to $(basename $REPODIR) files for $USER on $HOSTNAME..."
create_symlinks
echo "  OK: $SUCCESS_COUNTER files"
echo "FAIL: $FAILURE_COUNTER files"
