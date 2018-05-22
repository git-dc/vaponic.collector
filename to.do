[x] install latest influxdb and grafana (0)
[x] set up an influxdb server and create a database (1)
[x] write data to the influx db with curl (2)
[x] set up a grafana server (1)
[x] plot with grafana from an influx db (3)_
[x] rx from sensor through mqtt with mosquitto_sub and write to file (4)
[x] write util to convert mqtt sensor format to influx format (5)
[ ] write util to import collected data to influx from file
[x] write util to post from mosquitto_sub directly to influx (6)
[ ] 
[ ] unify mqtt-to-grafana






____________________________________________________________________
0. in influxdb.testbed repo: installSerives.sh
1. (0) and in influxdb.testbed repo: services.start
2. in influxdb.testbed repo: cpuValToInfluxDB.sh
3. after (1), localhost:3000, see dashboard
4. in vaponic.collector repo: mosquitto.run.sh and pow.vap.listen.sh; some data is collected on lubuntuN7 in dir data/
5. in pahoqm repo: converter.py
6. in pahomq repo: pahomq.py	
