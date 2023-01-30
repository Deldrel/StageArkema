BASE:=$(shell /bin/pwd)

all: sensor

sensor: data-sensor iot-sensor

data-sensor:
	/bin/bash ${BASE}/data-sensor.bash

#iot-sensor:
#	/bin/bash ${BASE}/iot-sensor.bash