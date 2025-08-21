#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o pipefail
if [[ "${TRACE-0}" == "1" ]]; then
    set -o xtrace
fi

if [[ "${1-}" =~ ^-*h(elp)?$ ]]; then
    echo 'Usage: ./mosquitto_password_helper.sh user1 password1 user2 password2 ... usern passwordn

This script creates an encrypted `./password.txt` given the user name and its password for use with mosquitto, see https://mosquitto.org/man/mosquitto_passwd-1.html for details

'
    exit
fi

OUTFILE="./password.txt"

# the following does work, but only with a single user/password combination instead of n many
# cat <<EOF | docker run -i --rm -v $OUTFILE:/tmp/password.txt`` eclipse-mosquitto:2 sh
# touch /tmp/password.txt
# mosquitto_passwd -b /tmp/password.txt $@
# echo "$@"
# EOF

counter=0

echo "Writing plain text '$OUTFILE', note that this will override any existent file"
echo -n "" > $OUTFILE

MQTT_USER=""
MQTT_PASSWD=""
for param in "$@"
do
    if ((counter % 2 == 0)); then
        # we are procerring them in pairs, skip odd numbers
        MQTT_USER="$param"
    else
        MQTT_PASSWD="$param"
        echo "${MQTT_USER}:${MQTT_PASSWD}" >> $OUTFILE
    fi
    counter=$((counter + 1))
done

echo "Encrypting '$OUTFILE' file"
docker run -it --rm -v $OUTFILE:/tmp/password.txt eclipse-mosquitto:2 mosquitto_passwd -U /tmp/password.txt

echo "All done."
