#####               ######
#   Import basic libtaties   #
#####               ######
import sys
import board
import analogio
from time import sleep
from analogio import AnalogIn
from digitalio import DigitalInOut, Direction, Pull

# Library for BLE Radio Advertising
#######################################
import _bleio
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement

# Libray For grenerating a new Service
########################################
from adafruit_ble.services import Service
from adafruit_ble.uuid import StandardUUID
from adafruit_ble.characteristics import Characteristic
from adafruit_ble.characteristics.int import Uint8Characteristic
from adafruit_ble.characteristics.int import Uint16Characteristic
from adafruit_ble.characteristics.int import Uint32Characteristic

button_state = 0

class myDataService(Service):
    uuid = StandardUUID(0xA000) # (0xA000 - my/Custom Service ID)
    myOutData = Uint8Characteristic(
        max_value=255,
        properties=Characteristic.READ | Characteristic.NOTIFY  ,
        uuid=StandardUUID(0xA001), #0ls -alcat xA002 -my/ID Write-to-Leds ID
#        value=bytes([button_state])
    )

    myInData = Uint8Characteristic(
        max_value=255,
        properties=Characteristic.WRITE ,
        uuid=StandardUUID(0xA002), #0ls -alcat xA002 -my/ID Write-to-Leds ID
    )
#CircuitPython Bug (removes old 0xA000 - service)
_bleio.adapter.enabled=0
_bleio.adapter.enabled=1


# oprett BLE - Bateri service med batteli level
dataService=myDataService()

#Start BLE-Radio
ble = BLERadio()
ble.name = "RunesBLE"

#Fortell verden hvem du er og hva du kan gjøre
advertisement = ProvideServicesAdvertisement(myDataService)

led1 = DigitalInOut(board.LED1)    # led Hvit
led1.direction = Direction.OUTPUT
led1.value=True

led2_r = DigitalInOut(board.LED2_R)    # led Rød
led2_r.direction = Direction.OUTPUT
led2_r.value=True

led2_g = DigitalInOut(board.LED2_G)    # led Grønn
led2_g.direction = Direction.OUTPUT
led2_g.value=True

led2_b = DigitalInOut(board.LED2_B)    # led Blå
led2_b.direction = Direction.OUTPUT
led2_b.value=True


switch = DigitalInOut(board.SW1)
switch.direction.INPUT



while True:

    print("Venter på tilkobling/bonding ")
    ble.start_advertising(advertisement)
    while not ble.connected:
        pass
    print("Bluetooth enhet er tilkoblet/bondet ")

    #Ikke vis verden hvem du er :)
    ble.stop_advertising()
    batNivaa=80
    oldLedVal=0
    buttonVal=False
    while ble.connected:
        if(buttonVal != switch.value):
             buttonVal = switch.value
             dataService.myOutData=buttonVal
             
        newLedValue=dataService.myInData # Leser verdien som kommer inn fra bruker
        if(oldLedVal != newLedValue) :
            if(newLedValue == 1): #Slår på LED 1 
                print("New Led data " + str(newLedValue))
                led1.value=False
                oldLedVal=newLedValue
            elif(newLedValue == 2):#Slår på LED 2, med farge rød
                print("New Led data " + str(newLedValue))
                led1.value=True
                led2_r.value=False
                led2_g.value=True
                led2_b.value=True
                oldLedVal=newLedValue
            elif(newLedValue == 3): #Slår på LED 2, med farge grønn
                print("New Led data " + str(newLedValue))
                led1.value=True
                led2_r.value=True
                led2_g.value=False
                led2_b.value=True
                oldLedVal=newLedValue  
            elif(newLedValue == 4): #Slår på LED 2, med farge Blå
                print("New Led data " + str(newLedValue))
                led1.value=True
                led2_r.value=True
                led2_g.value=True
                led2_b.value=False
                oldLedVal=newLedValue
            elif(newLedValue == 0): #Slår av alle LED's
                led1.value=True
                led2_r.value=True
                led2_b.value=True
                led2_g.value=True
            
        sleep(.001)

    print("Bluetooth enhet er frakoblet")

