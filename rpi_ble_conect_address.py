import time
import _bleio
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import Advertisement
from adafruit_ble.services.standard.device_info import DeviceInfoService

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

radio = BLERadio()

nrf52_connection=0
myDeviceAddressStr="EB:E1:24:47:80:51"
print("Trying to connnection to : %r!" % myDeviceAddressStr)

try:
    nrf52_connection = radio.connect( _bleio.Address(string=myDeviceAddressStr))
        
    if nrf52_connection and nrf52_connection.connected:
            print("Connected to %r!" % myDeviceAddressStr)

            if StandardUUID(0xA000) in nrf52_connection:
                 print("0xA000 - service found")
                
            if myDataService in nrf52_connection:
                print("switch service available")
                ds = nrf52_connection[myDataService]
                
                while nrf52_connection.connected:
                    for i in range(0,4):
                        ds.myInData=i # Send value
                        print("Sets new data to ch 0xA002 : ", i)
                        time.sleep(0.3)
                    ds.myInData=0     # Send value 0
                    break;
                print("Disconnect")
                nrf52_connection.disconnect()
            else:
                print("myDataService service not available")         
except:
        print("Error connecting to device %r!" % myDeviceAddressStr)
    