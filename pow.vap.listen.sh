#! /bin/bash

mosquitto_sub -h lubuntuN7 -p 1883 -i "pow.vap.listen" -t vaponic/tele/SENSOR >> data/vaponicData.log &



