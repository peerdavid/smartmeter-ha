# Mosquitto (MQTT)

Adapted from <https://github.com/vvatelot/mosquitto-docker-compose>.

## Authentication

Unfortunately, Mosquitto doesn't allow for authentication configuration using environment variables.
Instead, you need to run `mosquitto_password_helper.sh` which will create a `password.txt` file

the following are NOT passed as environment variables to the mosquitto container
instead they encrypted `password.txt` has been MANUALLY created using the  helper
so beware when changing these: you need to parametrize the arguments to said script, re-run it and make sure to commit those changes

## Verify functionality

In order to verify functionality, take an MQTT client of your choice, e.g. [MQTT Explorer](http://mqtt-explorer.com/) and connect to it using your configured credentials, you should see messages in at least the `$SYS` topic.
