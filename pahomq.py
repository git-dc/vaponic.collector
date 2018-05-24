#! /usr/bin/env python3

import paho.mqtt.client as mqtt
import datetime
import time
from influxdb import InfluxDBClient
from hashlib import md5

influxDB = "mydb"
influxUsr="admin"
influxPsk="admin"
influxPort=8086
influxHost="lubuntuN7"

msqttPort=1883
mqttHost="lubuntuN7"
mqttTopic="vaponic/tele/SENSOR"

dbclient = InfluxDBClient(influxHost,influxPort,influxUsr,influxPsk,influxDB)
log = open("logs/paho.%s.log"% get_time(),"w")
log.write("%s Log of paho client mqtt->influx.%s. Started at %s.\n" % (get_time(), influxDB, str(datetime.datetime.now())))
def main():
    # set up a client for influxdb
    # initialize the mqtt client that should connect to the mosquitto broker
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    connOK=False
    while(connOK == False):
        try:
            client.connect(mqttHost,mqttPort,60)
            connOK=True
        except:
            connOK=False
            time.sleep(2)
            # blocking loop to the mosquitto broker
    client.loop_forever()


def hash(packet): # returns a hash of the packet to act as an id
    return str(md5(str(packet).encode("utf-8")).hexdigest()[:6])

def get_time(): # generates a unix timestamp
    return str(time.time()).split(".")[0]

# converts YYYY-MM-DD:hh:mm:ss time format to unix timestamp format
def stampGen(s): # generates isoformat timestamp
    return datetime.datetime.strptime(s,"%Y-%m-%dT%H:%M:%S")

# takes a tasmota json and converts it to a dictionary 
def strip(message):
    junk = ["{","}",'"','ENERGY:'] # these will be removed from the input string (json object)
    tags='' # any measurement tags should be added here
    msgDict = {} # the return dict
    
    for thing in junk: message = message.replace(thing,"") # removes junk (see above) from message
    msgDec = [item.split(":") for item in message.split(',')] # split the input string into a list of measurements
    
    for item in msgDec:
        header = item.pop(0)
        if len(item)>1:

            #the timestamp contains some ":", so it gets split into multiple entries under key "Time" in msgDec; if length of the list is more than 1 after the header is popped, it should be the timestamp entry
            
            item=[stampGen(':'.join(item))+datetime.timedelta(hours=-4)]
            # puts in list to conform with format; timedelta of -4 to account for timezone - influx expects utc
        if header != "Period": msgDict[header] = item[0] # put the header:val, where val is item[0], key-value pairs into msgDict; Period is a trash value - always 0
    return msgDict

# takes a tasmota json and converts it to a dictionary 
def convert_to_influx(message):
    junk = ["{","}",'"','ENERGY:'] # these will be removed from the input string (json object)
    tags='' # any measurement tags should be added here
    msgDict = {} # the return dict
    
    for thing in junk: message = message.replace(thing,"") # removes junk (see above) from message
    msgDec = [item.split(":") for item in message.split(',')] # split the input string into a list of measurements
    
    for item in msgDec:
        header = item.pop(0)
        if len(item)>1:

            #the timestamp contains some ":", so it gets split into multiple entries under key "Time" in msgDec; if length of the list is more than 1 after the header is popped, it should be the timestamp entry
            
            item=[stampGen(':'.join(item))+datetime.timedelta(hours=-4)]
            # puts in list to conform with format; timedelta of -4 to account for timezone - influx expects utc

        msgDict[header] = item[0] # put the header:val, where val is item[0], key-value pairs into msgDict
    return msgDict

# paho.mqtt.client function overload
def on_connect(client, userdata, flags, rc):
    log.write("%s Connected to mosquitto broker %s with result code %s"% (get_time(), str(mqttHost), str(rc)))
    client.subscribe(mqttTopic)
    log.write("%s Subscribed to %s"% (get_time(), str(mqttTopic)))

# paho.mqtt.client function overload
def on_message(client, userdata, msg):
    #print("received a message on topic " + msg.topic)
    #use UTC as timestamp
    receiveTime=datetime.datetime.utcnow()
    message=msg.payload.decode("utf-8")
    msgs=strip(message)
    keys = [key for key in msgs] # extract keys only from msgDict // ===msgs
    msgs["id"] = str(hash(msgs["Time"]))
    keys.remove("Time") # otherwise Time will be a measurement in influx
    json_body = []
    for key in keys:
        try: # convert the value to a float so that it is stored as a number in influx and not as a string in the db
            val=float(msgs[key])
            log.write("%s Valid entry found in %s: '%s':'%s' (utc) %s at (utc) %s."% (get_time(), msgs["id"], key, str(val), str(msgs["Time"]), str(datetime.datetime.now())))
            entry = {
                "measurement":key,
                "time":msgs["Time"],
                "fields":
                {
                    "value":val
                }
            }
            json_body.append(entry)
            log.write(" Inserted into payload.\n")
        except:
            log.write("%s Could not convert '%s':'%s' to a float value, skipping it.\n"% (get_time(), key, msgs[key]))
            #user = input("Would you like to skip and proceed? (Y/n)")
            #if user.lower() == "y": continue
            #else: data.close()
    if len(json_body) > 0:
        dbclient.write_points(json_body)
        log.write("%s Pushed payload with id %s to %s at %s.\n"% (get_time(), msgs["id"], influxDB, get_time()))

main()
