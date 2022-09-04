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

class myDataService(Service):
    uuid = StandardUUID(0xA000) # (0xA000 - my/Custom Service ID)
    myOutData = Uint8Characteristic(
        max_value=255,
        properties=Characteristic.READ | Characteristic.NOTIFY  ,
        uuid=StandardUUID(0xA001), #0ls -alcat xA002 -my/ID Write-to-Leds ID
    )
    
    myInData = Uint8Characteristic(
        max_value=255,
        properties=Characteristic.WRITE ,
        uuid=StandardUUID(0xA002), #0ls -alcat xA002 -my/ID Write-to-Leds ID
    )
#CircuitPython Bug (removes old 0xA000 - service)
_bleio.adapter.enabled=0
_bleio.adapter.enabled=1

# Create Service width Characteristics
dataService=myDataService()

#Start BLE-Radio
ble = BLERadio()
ble._clean_connection_cache()
ble.name = "RunesBLE"

#Fortell verden hvem du er og hva du kan gjøre
advertisement = ProvideServicesAdvertisement(dataService)
ble.start_advertising(advertisement)

print("Venter på tilkobling/bonding ")
while not ble.connected:
        pass
print("Bluetooth enhet er tilkoblet/bondet ")

#Ikke vis verden lengere hvem du er :)
ble.stop_advertising()
    
oldVal=0
firstTime=True
while ble.connected:
    
    if(firstTime):
        firstTime=False
        dataService.myOutData=0
            
    newValue=dataService.myInData
    if(oldVal != newValue) :
        print("Data skrevet til Characteristic 0xA002 (myInData) " + str(newValue))
        oldVal=newValue                     # Lagrer ny-verdi 
        dataService.myOutData=0x10+oldVal   # Lagrer ny-verdi + 0x10 i Characteristic 0xA001      
    
print("Bluetooth enhet er frakoblet")