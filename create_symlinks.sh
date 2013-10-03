#!/bin/bash
#
# Create symlinks in local filesystem for each repository file listed

export REPODIR=$(pwd)
export HN=$(hostname)

source bash/linking_functions.sh

create_symlinks () {
    link_to_git_repo $HOME/.screenrc $REPODIR/dotfiles/screenrc
}

SUCCESS_COUNTER=0
create_symlinks
echo "  OK: $SUCCESS_COUNTER files"