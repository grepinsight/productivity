#!/bin/bash


LIST_OF_FILES=$(git log --oneline --decorate --graph --format=format:"%C(bold blue)%h%C(reset) - %C(bold cyan)%aD%C(dim white) - %an%C(reset) %C(bold green)(%ar)%C(reset)%C(bold yellow)%d%C(reset)%n %C(white)%s%C(reset)" --name-only master.. | grep '/'| grep -v '*'| egrep -v '\|\s+$' | awk '{print $2}'| sed '/^$/d' | sort | uniq)

#echo "Modifies Files:"
#echo "---------------"

for i in $LIST_OF_FILES; do 
    test -f $i && echo "$i"
done
