import time

class Temperature:
    def __init__(self, sensorid):
        self.sensorid = sensorid

    def get_temperature(self):
        sensor_file_name = '/sys/bus/w1/devices/' + self.sensorid + '/w1_slave'
        sensor_file = open(sensor_file_name, 'r')
        value = 0
        for line in sensor_file:
            if "YES" not in line:
                plaats = line.find("t")
                # print(f"De temperatuur is {float(line[plaats+2:])/1000} °Celsius")
                tempvalue = float(line[plaats+2:])/1000
        sensor_file.close()
        return tempvalue
        
