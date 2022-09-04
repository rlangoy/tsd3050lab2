import board  
from digitalio import DigitalInOut, Direction 

led = DigitalInOut(board.LED2_B)  
led.direction = Direction.OUTPUT  
SW = DigitalInOut(board.SW1)
SW.direction = Direction.INPUT  
  
while 1:  
    if (SW.value == 1):  
        led.value = 1  
    else:  
        led.value = 0  