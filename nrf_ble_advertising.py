# Library for BLE Radio Advertising
#######################################
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement

#Start BLE-Radio
ble = BLERadio()
ble.name = "RunesBLE"
#Fortell verden hvem du er (neste oppgave forteller vi hva som kan gjøres)
advertisement = ProvideServicesAdvertisement()
ble.start_advertising(advertisement)

print("Venter på tilkobling/bonding ")
while not ble.connected:
        pass

print("Bluetooth enhet er tilkoblet/bondet ")
#Ikke vis verden hvem du er :)
ble.stop_advertising()
    
while ble.connected:
    batNivaa=0       #Mens BLE er tilkobler gjør noe
    
print("Bluetooth enhet er frakoblet")
