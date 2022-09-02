from adafruit_ble import BLERadio

radio = BLERadio()
print("scanning")
found = set()
for entry in radio.start_scan(timeout=60, minimum_rssi=-80):
    addr = entry.address
    if addr not in found:
        print(entry)
        print(addr)
    found.add(addr)

print("scan done")
