import time
import board
import busio
import displayio


import board
import busio
import time
import displayio

# Release any old display allocations before touching I2C
displayio.release_displays()

i2c = busio.I2C(board.GP1, board.GP0)

def i2c_scan():
    """Performs a single non-blocking scan of the I2C bus."""
    while not i2c.try_lock():
        pass

    print("I2C scan...")
    devices = i2c.scan()

    if devices:
        for device in devices:
            print("Found device at:", hex(device))
    else:
        print("No I2C devices found")

    i2c.unlock()        
