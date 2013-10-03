#!/bin/bash
#
# Create symlinks in local filesystem for each repository file listed

export REPODIR=$(pwd)
export HN=$(hostname)

source bash/linking_functions.sh

create_symlinks () {
    safe_mkdir $HOME/bin/

    # dotfiles
    link_to_git_repo $HOME/.bashrc   $REPODIR/dotfiles/bashrc
    link_to_git_repo $HOME/.screenrc $REPODIR/dotfiles/screenrc
    link_to_git_repo $HOME/.vimrc    $REPODIR/dotfiles/vimrc
    link_to_git_repo $HOME/.zshrc    $REPODIR/dotfiles/zshrc

    # programs/scripts
    link_to_git_repo $HOME/bin/latex2png $REPODIR/latex/latex2png.sh
}

SUCCESS_COUNTER=0
echo "Creating links for git-versioned files for $USER on $HN"
create_symlinks
echo "  OK: $SUCCESS_COUNTER files"
