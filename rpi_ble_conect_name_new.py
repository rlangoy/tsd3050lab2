import time
import _bleio
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import Advertisement
from adafruit_ble.services.standard.device_info import DeviceInfoService

# Libray For grenerating a new Service
########################################
from adafruit_ble.services import Service
from adafruit_ble.uuid import StandardUUID , VendorUUID
from adafruit_ble.characteristics import Characteristic
from adafruit_ble.characteristics.int import Uint8Characteristic

class myDataService(Service) :
    #uuid = StandardUUID(0xA000)                               # (0xA000 - my/Custom Service ID)
    uuid = VendorUUID("0000a000-0000-1000-8000-00805f9b34fb")  # (0xA000 - my/Custom Service ID)
    myOutData = Uint8Characteristic(
        max_value=255,
        properties=Characteristic.READ | Characteristic.NOTIFY  ,
        #uuid=StandardUUID(0xA001), #0ls -alcat xA002 -my/ID Write-to-Leds ID
        uuid = VendorUUID("0000a001-0000-1000-8000-00805f9b34fb") # UUID 0xA001 - Read from device
    )
    
    myInData = Uint8Characteristic(
        max_value=255,
        properties=Characteristic.WRITE ,
        #uuid=StandardUUID(0xA002), #0ls -alcat xA002 -my/ID Write-to-Leds ID
        uuid = VendorUUID("0000a002-0000-1000-8000-00805f9b34fb") # UUID 0xA002 - write to device 
    )

radio = BLERadio()
print("scanning")

nrf52_connection=0

for adv in radio.start_scan(Advertisement, timeout=10):
    name = adv.complete_name
    if not name:
        continue
    #  devices may have trailing nulls on their name.
    if name.strip("\x00") ==  "RunesBLE":        
        nrf52_connection = radio.connect(adv)
        #Stop scanning whether or not we are connected.
        radio.stop_scan()
        print("Connected to " + adv.address.string)
        print(nrf52_connection)
        break

if nrf52_connection and nrf52_connection.connected:
        print("Connected to %r!" % name)

        if StandardUUID(0xA000) in nrf52_connection:
             print("0xA000 - service found")
            
        if myDataService in nrf52_connection:
            print("switch service available")
            ds = nrf52_connection[myDataService]
            
            while nrf52_connection.connected:
                #print("status %r" % dataService.read_status())
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
