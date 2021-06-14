import time
from RPi import GPIO

# default pin numbers (BCM) - pas aan indien nodig
DS = 16  # serial data
OE = 12  # output enable (active low)
STCP = 7  # storage register clock pulse
SHCP = 25  # shift register clock pulse
MR = 15  # master reset (active low)


DELAY = 0.001

class ShiftRegister:
    def __init__(self, ds_pin=DS, shcp_pin=SHCP, stcp_pin=STCP, mr_pin=MR, oe_pin=OE):
       
        self.ds_pin = ds_pin
        self.shcp_pin = shcp_pin
        self.stcp_pin = stcp_pin
        self.mr_pin = mr_pin
        self.oe_pin = oe_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup([self.ds_pin, self.oe_pin, self.shcp_pin, self.stcp_pin, self.mr_pin], GPIO.OUT, initial=GPIO.LOW)
        # volgende kan ook
        # for pin in self.ds_pin, self.oe_pin, self.shcp_pin, self.stcp_pin, self.mr_pin:
        #     GPIO.setup(pin, GPIO.OUT)
        #     GPIO.output(pin, GPIO.LOW)
        GPIO.output(self.mr_pin, GPIO.HIGH)

    def write_bit(self, value):
        GPIO.output(self.shcp_pin, GPIO.LOW)
        GPIO.output(self.ds_pin,value)
        #time.sleep(0.1)
        GPIO.output(self.shcp_pin, GPIO.HIGH)
        # vul hier zelf aan, gebruik self.ds_pin en self.shcp_pin als pin variabelen  
        pass
      
    
    def copy_to_storage_register(self):
        GPIO.output(self.stcp_pin, GPIO.HIGH)
        #time.sleep(0.1)
        GPIO.output(self.stcp_pin, GPIO.LOW)
        # vul hier zelf aan, gebruik self.ds_pin en self.shcp_pin als pin variabelen  
        pass       
        
    def write_byte(self, value):
        mask = 0x80
        for i in range (0,8):
            if value & (mask >> i):
                self.write_bit(True)
            else:
                self.write_bit(False)
        self.copy_to_storage_register()
        # vul hier zelf aan: code om een byte uit te splitsen in bits...
        pass

    @property
    def output_enabled(self):
        return not GPIO.input(self.oe_pin)

    @output_enabled.setter
    def output_enabled(self, value):
        GPIO.output(self.oe_pin, not value)

    def reset_shift_register(self):
        
        GPIO.output(self.mr_pin, GPIO.LOW)
        time.sleep(DELAY)
        GPIO.output(self.mr_pin, GPIO.HIGH)
        time.sleep(DELAY)

    def reset_storage_register(self):
        
        self.reset_shift_register()
        self.copy_to_storage_register()

    def cleanup_GPIO(self):
        GPIO.cleanup()


def shiftreg_demo():
   
    shreg = ShiftRegister()
    value = 1
    while value < 0x100:
        shreg.write_byte(value)
        shreg.copy_to_storage_register()
        time.sleep(1)
        value <<= 1

def teller():
    shreg = ShiftRegister()
    for i in range (0,16):
        shreg.write_byte(SEGMENTS[i])
        shreg.copy_to_storage_register()
        time.sleep(1)


# Juiste bit voor elk segment: vul/pas aan
A = 1 << 0
B = 1 << 1
C = 1 << 2
D = 1 << 3
E = 1 << 4
F = 1 << 5
G = 1 << 6
DP = 1 << 7

# Juist segment voor elk (hex) cijfer: vul/pas aan
SEGMENTS = {
    0x0: A | B | C | D | E | F,
    0x1: B | C,
    0x2: A | B | G | E | D,
    0x3: A | B | C | D | G,
    0x4: F | G | B | C,
    0x5: A | F | G | C | D,
    0x6: A | C | D | E | F | G,
    0x7: A | B | C,
    0x8: A | B | C | D | E | F | G,
    0x9: A | B | C | D | F | G,
    0xA: A | B | C | E | F | G,
    0xb: C | D | E | F | G,
    0xC: A | F | E | D,
    0xd: B | C | D | E | G,
    0xE: A | F | G | E | D,
    0xF: A | G | F | E,
}



def main():
    GPIO.setmode(GPIO.BCM)
    try:
        # Hier kan je jouw functies/klassen oproepen om ze te testen
        shiftreg_demo()
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()


if __name__ == '__main__':
    main()