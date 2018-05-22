#! /bin/bash

# run me with sudo

echo 'run me with sudo'

source /etc/lsb-release

grafanaDeb='deb https://packagecloud.io/grafana/stable/debian/ stretch main'
influxDeb="deb https://repos.influxdata.com/${DISTRIB_ID,,} ${DISTRIB_CODENAME} stable"
sourcesFile='/etc/apt/sources.list'




if ! grep -q "$grafanaDeb" "$sourcesFile" ; then
    sudo echo "$grafanaDeb" >> "$sourcesFile"
    curl https://packagecloud.io/gpg.key | sudo apt-key add -
fi

if ! grep -q "$influxDeb" "$sourcesFile" ; then
    sudo echo "$influxDeb" >> "$sourcesFile"
    curl -sL https://repos.influxdata.com/influxdb.key | sudo apt-key add -
fi




sudo apt-get update
sudo apt-get install grafana
sudo apt-get install influxdb
