#!/bin/bash

# Check passwords by hashing them, calling the prefix API from
# https://www.troyhunt.com/ive-just-launched-pwned-passwords-version-2/#cloudflareprivacyandkanonymity,
# and checking the results.
#
# Returns 1 if the password was found, 0 if not.

read -s -p "Enter password: " pw
thehash=$(echo -n "${pw}" | sha1sum | cut -d' ' -f1 | tr '[a-z]' '[A-Z]') 
echo
echo "The hash: ${thehash}"

prefix=${thehash:0:5}
url="https://api.pwnedpasswords.com/range/${prefix}"
echo "Contacting ${url}..."
results=$(curl -s ${url})
echo "Checking $(echo "$results" | wc -l) possibilities..."
echo

for line in $results ; do
    subhash="${line:0:35}"
    thishash="${prefix}${subhash}"
    if [ "${thishash}" == "${thehash}" ] ; then
        count="$(echo "$line" | cut -d: -f2 | tr -d '\n\r')"
        echo "Password was found ${count} times"
        exit 1
    fi
done

echo "Not found, congrats!"
exit 0
