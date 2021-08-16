#!/bin/bash

# GETTING PATH
crapdir="$(dirname $(realpath $0))"
# SHOWING HELP MESSAGE
cat "$crapdir"/elbarto.txt "$crapdir"/craplogo.txt "$crapdir"/help.txt
# CLOSE WHEN READY
printf "\n$(tput setaf 8)Press any key to continue ...$(tput sgr0)"
read closing
printf "\n"
