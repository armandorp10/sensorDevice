import smbus
import os
import glob
import time
import datetime
import requests


class MLX90614():

    MLX90614_RAWIR1=0x04
    MLX90614_RAWIR2=0x05
    MLX90614_TA=0x06
    MLX90614_TOBJ1=0x07
    MLX90614_TOBJ2=0x08

    MLX90614_TOMAX=0x20
    MLX90614_TOMIN=0x21
    MLX90614_PWMCTRL=0x22
    MLX90614_TARANGE=0x23
    MLX90614_EMISS=0x24
    MLX90614_CONFIG=0x25
    MLX90614_ADDR=0x0E
    MLX90614_ID1=0x3C
    MLX90614_ID2=0x3D
    MLX90614_ID3=0x3E
    MLX90614_ID4=0x3F

    def __init__(self, address=0x5a, bus_num=1):
        self.bus_num = bus_num
        self.address = address
        self.bus = smbus.SMBus(bus=bus_num)

    def read_reg(self, reg_addr):
        return self.bus.read_word_data(self.address, reg_addr)

    def data_to_temp(self, data):
        temp = (data*0.02) - 273.15
        return temp

    def get_amb_temp(self):
        data = self.read_reg(self.MLX90614_TA)
        return self.data_to_temp(data)

    def get_obj_temp(self):
        data = self.read_reg(self.MLX90614_TOBJ1)
        return self.data_to_temp(data)

exists = os.path.exists('/sys/bus/w1')

if exists == True:
    Sensor_dir = glob.glob('/sys/bus/w1/devices/' + '28*')[0]
    while True:
        try:    
            average = 0.0
            cont = 0

            fSensor = open(Sensor_dir + '/w1_slave', 'r')
            linSensor = fSensor.readlines()
            fSensor.close()

            posTemp = linSensor[1].find('t=')
            # If is a valid position
            if posTemp != -1:
                strTemp = linSensor[1][posTemp+2:]
                temperature = float(strTemp) / 1000.0

            # Obtener promedio de temperaturas
            for i in range(9):
                time.sleep(0.1)
                cont = cont + temperature

            average = cont / 10
            data = {
                "value": average,
                "unit": "C",
                "date": datetime.datetime.now()
            }

            # Enviar promedio a web service
            requests.post("http://172.24.41.194:5000/", data)
            print(data)
        except:
            print("An exception ocurred")
        time.sleep(5)
        
else:
    sensor = MLX90614()
    while True:
        try:
            average = 0.0
            cont = 0

            temperature = sensor.get_amb_temp()

            # Obtener promedio de temperaturas
            for i in range(9):
                time.sleep(0.1)
                cont = cont + temperature

            average = cont / 10
            data = {
                "value": average,
                "unit": "C",
                "date": datetime.datetime.now()
            }

            # Enviar promedio a web service
            requests.post("http://172.24.41.194:5000/", data)
            print (data)
        except:
            print("An exception ocurred")
        time.sleep(5)
        