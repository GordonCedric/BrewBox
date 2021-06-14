from helpers.Klasse_LCD import LCD
from RPi import GPIO
import time

E = 20
RS = 21

def setup():  # b
    GPIO.setmode(GPIO.BCM)
    
try: 
    setup()   
    scherm = LCD()
    scherm.setup()
    scherm.init_LCD()
    scherm.write_message("Hoi ik ben cedric")

except KeyboardInterrupt as e:
    print(e)
    # pass

finally:
    GPIO.cleanup()
    print("Script has stopped!!!")