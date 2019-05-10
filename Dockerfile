FROM resin/rpi-raspbian
RUN apt-get update \
 && apt-get install -y python3-pip python3-dev python3-smbus\
 && pip3 install --upgrade pip \
 && pip3 install paho-mqtt

COPY sensorT-V1.py /home/
