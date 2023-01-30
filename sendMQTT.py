import os
import time
import datetime
import json
import random
import AWSIoTPythonSDK.MQTTLib as AWSIoTPyMQTT
import smbus

#define ENDPOINT, CLIENT_ID, PATH_TO_CERT, PATH_TO_KEY, PATH_TO_ROOT, MESSAGE, TOPIC, and RANGE

ENDPOINT = "a3aivly5j8p5oa-ats.iot.eu-west-1.amazonaws.com"
CLIENT_ID = "myClientID"
PATH_TO_CERT = "certs/certificate.pem.crt"
PATH_TO_KEY = "certs/private.pem.key"
PATH_TO_ROOT = "certs/Amazon-root-CA-1.pem"
TOPIC = "myTopic"

DEVICE_BUS = 1
DEVICE_ADDR = 0x17

TEMP_REG = 0x01
LIGHT_REG_L = 0x02
LIGHT_REG_H = 0x03
STATUS_REG = 0x04
ON_BOARD_TEMP_REG = 0x05
ON_BOARD_HUMIDITY_REG = 0x06
ON_BOARD_SENSOR_ERROR = 0x07
BMP280_TEMP_REG = 0x08
BMP280_PRESSURE_REG_L = 0x09
BMP280_PRESSURE_REG_M = 0x0A
BMP280_PRESSURE_REG_H = 0x0B
BMP280_STATUS = 0x0C
HUMAN_DETECT = 0x0D

bus = smbus.SMBus(DEVICE_BUS)
aReceiveBuf = []
aReceiveBuf.append(0x00)

for i in range(TEMP_REG,HUMAN_DETECT + 1):
    aReceiveBuf.append(bus.read_byte_data(DEVICE_ADDR, i))

sensorTemp = aReceiveBuf[TEMP_REG]
onboardBrightness = (aReceiveBuf[LIGHT_REG_H] << 8 | aReceiveBuf[LIGHT_REG_L])
onboardSensorTemp = aReceiveBuf[ON_BOARD_TEMP_REG]
onboardSensorHum = aReceiveBuf[ON_BOARD_HUMIDITY_REG]
baroTemp = aReceiveBuf[BMP280_TEMP_REG]
baroPress = (aReceiveBuf[BMP280_PRESSURE_REG_L] | aReceiveBuf[BMP280_PRESSURE_REG_M] << 8 | aReceiveBuf[BMP280_PRESSURE_REG_H] << 16)
	
myAWSIoMQTTClient = AWSIoTPyMQTT.AWSIoTMQTTClient(CLIENT_ID)
myAWSIoMQTTClient.configureEndpoint(ENDPOINT, 8883)
myAWSIoMQTTClient.configureCredentials(PATH_TO_ROOT, PATH_TO_KEY, PATH_TO_CERT)
myAWSIoMQTTClient.connect()

message = {
	"sensorTemp" : sensorTemp,
	"onboardBrightness" : onboardBrightness,
	"onboardSensorTemp" : onboardSensorTemp,
	"onboardSensorHum" : onboardSensorHum,
	"baroTemp" : baroTemp,
	"baroPress" : baroPress,
	"timestamp" : str(round(time.time()))
}

myAWSIoMQTTClient.publish(TOPIC, json.dumps(message), 1)
print("Published: '" + json.dumps(message) + "' to the topic :" + TOPIC)

myAWSIoMQTTClient.disconnect()
