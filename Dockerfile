FROM resin/rpi-raspbian
RUN apt-get update \
 && apt-get install -y python3-pip python3-dev python3-smbus\
 && pip3 install --upgrade pip \
 && pip3 install paho-mqtt \
 && pip3 install requests

COPY sensorT-V1.py /home/
CMD python3 /home/sensorT-V1.py
