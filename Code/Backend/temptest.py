from helpers.ProjectKlasse import Project
from RPi import GPIO
import time


try:
    project = Project()
    project.setup()

    print(project.get_temperatures())
    print(project.get_volumes())
    # project.fill_pumps()
    # time.sleep(2)
    # project.dispense_drink(20, 1)
    # time.sleep(3)
    # project.dispense_drink(80, 2)
    # time.sleep(2)
    # time.sleep(5)
    # project.empty_pumps()
    # project.dispense_drink(20, 2)
    GPIO.cleanup()
        
except KeyboardInterrupt as e:
    print(e)
finally:
    GPIO.cleanup()
    project.stop_pumps()
    print("script stopped")