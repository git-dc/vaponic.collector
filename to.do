[x] install latest influxdb and grafana (0)
[x] set up an influxdb server and create a database (1)
[x] write data to the influx db with curl (2)
[x] set up a grafana server (1)
[x] plot with grafana from an influx db (3)_
[x] rx from sensor through mqtt with mosquitto_sub and write to file (4)
[x] write util to convert mqtt sensor format to influx format (5)
[x] write util to import collected data to influx from file (8)
[x] write util to post from mosquitto_sub directly to influx (6)
[x] unify mqtt-to-grafana (7)
[x] make regular imports automatic (9)
[ ] add core utils for convenience






____________________________________________________________________
0. in vaponic.collector repo: serives.install
1. (0) && in vaponic.collector repo: services.start
2. in influxdb.testbed repo: cpuValToInfluxDB.sh
3. (1) && localhost:3000 && see dashboard
4. in vaponic.collector repo: services.start; some data is collected on lubuntuN7 in dir data/
5. in vaponic.collector repo: pahomq.py::convert_to_influx()
6. in vaponic.collector repo: pahomq.py	
7. in vaponic.collector repo: services.install && services.start
8. in vaponic.collector repo: import.py
9. in vaponic.collector repo: services.start && cronjob