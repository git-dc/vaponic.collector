#! /usr/bin/env python3

import paho.mqtt.client as mqtt
import datetime
import time
from influxdb import InfluxDBClient


# converts YYYY-MM-DD:hh:mm:ss time format to unix timestamp format
def stampGen(s): # the +14400 is to correct for the inexplicable 4 hour lag introduced by .mktime(...)
    return datetime.datetime.strptime(s,"%Y-%m-%dT%H:%M:%S")
    #return str(time.mktime(datetime.datetime.strptime(s,"%Y-%m-%dT%H:%M:%S").timetuple())+14400)


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
    print("connected to mosquitto broker with result code " + str(rc))
    client.subscribe("vaponic/tele/SENSOR")
    print('subscribed to "vaponic/tele/SENSOR"')

# paho.mqtt.client function overload
def on_message(client, userdata, msg):
    print("received a message on topic " + msg.topic)
    #use UTC as timestamp
    receiveTime=datetime.datetime.utcnow()
    message=msg.payload.decode("utf-8")
    msgs=convert_to_influx(message)
    keys = [key for key in msgs] # extract keys only from msgDict // ===msgs
    keys.remove("Time") # otherwise Time will be a measurement in influx
    for key in keys:
        isfloatValue=False
        try: # convert the value to a float so that it is stored as a number in influx and not as a string in the db
            val=float(msgs[key])
            isfloatValue=True
        except:
            print("Could not convert " + msgs[key] + " to a float value, skipping "+key+":"+msgs[key])
            isfloatValue=False
        if isfloatValue:
            print("Received "+key+":"+str(val)+" (utc) "+str(msgs["Time"])+" at (utc) "+str(receiveTime))
            json_body = [
                {
                    "measurement":key,
                    "time":msgs["Time"],
                    #"time":receiveTime,
                    "fields":
                    {
                        "value":val
                    }
                }
            ]
            dbclient.write_points(json_body)
            print("Finished writing to InfluxDB")

# set up a client for influxdb
dbclient = InfluxDBClient('localhost',8086,'admin','admin','mydb')

# initialize the mqtt client that should connect to the mosquitto broker
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
connOK=False
while(connOK == False):
    try:
        client.connect("localhost",1883,60)
        connOK=True
    except:
        connOK=False
    time.sleep(2)
    
# blocking loop to the mosquitto broker
client.loop_forever()

