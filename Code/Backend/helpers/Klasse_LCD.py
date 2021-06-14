from RPi import GPIO
from helpers.shiftklasse import ShiftRegister
import time 

# pinnen = [16, 12, 25, 24, 23, 26, 19, 13]
E = 20
RS = 21

class LCD:
    def __init__(self):
        pass

    def setup(self):
        self.shreg = ShiftRegister()
        GPIO.setup(E, GPIO.OUT)
        GPIO.setup(RS, GPIO.OUT)
        # for i in pinnen:
        #     GPIO.setup(i, GPIO.OUT, initial=GPIO.LOW)
        GPIO.output(E, GPIO.HIGH)
        self.shreg.reset_storage_register()

    def set_data_bits(self, value):  # C
        # mask = 0b00000001
        # for bit in range(0, 8):
        #     pin = pinnen[bit]
        #     if value & mask:  # als de bit van mask en value 1 is
        #         GPIO.output(pin, GPIO.HIGH)
        #     else:  # als de bit van mask en value 0 is
        #         GPIO.output(pin, GPIO.LOW)
        #     mask = mask << 1
        self.shreg.write_byte(value)



    def send_instruction(self, value):  # d
        GPIO.output(RS, GPIO.LOW)
        self.set_data_bits(value)
        GPIO.output(E, GPIO.LOW)
        GPIO.output(E, GPIO.HIGH)
        time.sleep(0.01)


    def send_character(self, value):  # e
        GPIO.output(RS, GPIO.HIGH)
        self.set_data_bits(value)
        GPIO.output(E, GPIO.LOW)
        GPIO.output(E, GPIO.HIGH)
        time.sleep(0.01)


    def init_LCD(self):  # f
        self.send_instruction(0b00111000)
        self.send_instruction(0b00001111)
        self.send_instruction(0b00000001)

    def write_message(self, bericht):
        counter = 0
        for letter in bericht:
            counter += 1
            if (counter == 16):
                self.send_instruction(0xC0)
            self.send_character(ord(letter))

    def cleanup_GPIO(self):
        self.shreg.cleanup_GPIO()
        GPIO.cleanup()