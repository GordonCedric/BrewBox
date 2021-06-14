from helpers.TemperatuurKlasse import Temperature
from helpers.UltrasoneKlasse import Ultrasone
from helpers.Klasse_LCD import LCD
from RPi import GPIO
import time

class Project:
    def __init__(self):
        self.__pomp1 = 23
        self.__pomp2 = 24
        self.__t1sensor = Temperature('28-012033bb2a6e')
        self.__t2sensor = Temperature('28-012033b34017')
        self.__u1sensor = Ultrasone(17, 27)
        self.__scherm = LCD()
        self.__u2sensor = Ultrasone(26, 19)
        
    
    def setup(self):
        self.__scherm.setup()
        self.__scherm.init_LCD()
        self.__u1sensor.setup()
        self.__u2sensor.setup()
        GPIO.setup(self.__pomp1, GPIO.OUT)
        GPIO.setup(self.__pomp2, GPIO.OUT)

        pass

    def __getIP(self, interface):
        ips = str(check_output(['ip', 'a']))
        wlan = ips[ips.find(interface + ':'):]
        wlan = wlan[wlan.find('inet ') + 5:]
        wlan = wlan[:wlan.find('/')]
        return wlan
    
    def get_temperatures(self):
        sensor1 = self.__t1sensor.get_temperature()
        sensor2 = self.__t2sensor.get_temperature()
        return sensor1,sensor2

    def get_volumes(self):
        sensor1 = self.__u1sensor.get_distance()
        sensor2 = self.__u2sensor.get_distance()
        volume1 = (sensor1 / 18)*100 # Delen door 18 gebaseerd op de bidons aangezien de maximum afstand 18 is
        if volume1 > 100: #Indien er gevuld wordt tot boven de aangegeven lijn 100% vol doorgeven.
            volume1 = 100
        volume2 = (sensor2 / 18)*100 # Delen door 18 gebaseerd op de bidons aangezien de maximum afstand 18 is
        if volume2 > 100: #Indien er gevuld wordt tot boven de aangegeven lijn 100% vol doorgeven.
            volume2 = 100
        return round(volume1, 2), round(volume2, 2)

    def write_message(self, value):
        self.__scherm.write_message(value)
        pass

    def clear_lcd(self):
        self.__scherm.send_instruction(0b00000001)
    
    def dispense_drink(self, percentage, pump):
        pumptime = round(33*(percentage/100), 2)
        print(pumptime)
        GPIO.output(self.__pomp1, GPIO.LOW)
        GPIO.output(self.__pomp2, GPIO.LOW)
        if(pump == 1):
            GPIO.output(self.__pomp1, GPIO.HIGH)
            time.sleep(pumptime)
            GPIO.output(self.__pomp1, GPIO.LOW)
        elif(pump == 2):
            GPIO.output(self.__pomp2, GPIO.HIGH)
            time.sleep(pumptime)
            GPIO.output(self.__pomp2, GPIO.LOW)

    def fill_pumps(self):
        GPIO.output(self.__pomp1, GPIO.HIGH)
        GPIO.output(self.__pomp2, GPIO.HIGH)
        time.sleep(2.5)
        GPIO.output(self.__pomp1, GPIO.LOW)
        GPIO.output(self.__pomp2, GPIO.LOW)

    def empty_pumps(self):
        GPIO.output(self.__pomp1, GPIO.HIGH)
        GPIO.output(self.__pomp2, GPIO.HIGH)
        time.sleep(10)
        GPIO.output(self.__pomp1, GPIO.LOW)
        GPIO.output(self.__pomp2, GPIO.LOW)

    def stop_pumps(self):
        GPIO.output(self.__pomp1, GPIO.LOW)
        GPIO.output(self.__pomp2, GPIO.LOW)

    def cleanup_GPIO(self):
        GPIO.cleanup()
        
        self.__scherm.cleanup_GPIO()
        self.__u1sensor.cleanup_GPIO()
        self.__u2sensor.cleanup_GPIO()
            