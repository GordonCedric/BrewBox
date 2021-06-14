import RPi.GPIO as GPIO
import time

class Ultrasone:
    def __init__(self, trig, echo):
        self.__trig = trig
        self.__echo = echo

    def setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.__trig,GPIO.OUT)
        GPIO.setup(self.__echo,GPIO.IN)

    def get_distance(self):
        GPIO.output(self.__trig,False)
        time.sleep(2)
        GPIO.output(self.__trig, True)
        time.sleep(0.00001)
        GPIO.output(self.__trig, False)
        while GPIO.input(self.__echo)==0:
            pulse_start = time.time()
        while GPIO.input(self.__echo)==1:
            pulse_end = time.time()
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150
        # distance = (pulse_duration * 340)/100/2
        distance = round(distance, 2)
        return distance

    def cleanup_GPIO(self):
        GPIO.cleanup()