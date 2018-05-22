# vaponic.collector

Collects power consumption data from the mqtt sensor and pushes it into the local influx db. Grafana is running in the background to plot the uploading data.

To start mosquitto, influxdb, grafana services, local vaponic.pow backup client, and paho mqtt-influx client, run
$ ./services.start
