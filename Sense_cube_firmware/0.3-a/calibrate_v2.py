"""
full asynchronous module for calibrating sensetivy of touch sensor


"""

from chrg_isconnected import chrg_isconnected as on_charge
from machine import TouchPad, Pin
import uasyncio as asyncio
import neopixel

top = neopixel.NeoPixel(Pin(19), 2)
t = TouchPad(Pin(33))


async def calibrate():
    r = 55
    for i in range(3):
        while r < 220:
            r += 1
            top.fill([r,0,0])
            top.write()
            await asyncio.sleep_ms(6)
            
        while r > 55:
            r -= 1
            top.fill([r,0,0])
            top.write()
            await asyncio.sleep_ms(6)
    is_charging = on_charge()    
    await asyncio.sleep_ms(100)    
    top.fill((0,0,100))
    top.write()
    non_push = t.read()
    print("no push:", non_push)
    while True:
        if t.read() < non_push - 3:
            print("has touch", t.read())
            await asyncio.sleep(5)
            top.fill((0,100,0))
            top.write()
            pushed = t.read()
            await asyncio.sleep(1)
            g = 55
            for i in range(3):
                while g < 220:
                    g += 1
                    top.fill([0,g,0])
                    top.write()
                    await asyncio.sleep_ms(6)
                    
                while g > 55:
                    g -= 1
                    top.fill([0,g,0])
                    top.write()
                    await asyncio.sleep_ms(6)
            
            
            print("no touch: {}, with touch: {}, on dock: {}".format(non_push, pushed, is_charging))
            return(non_push - 3, is_charging)
        await asyncio.sleep_ms(50)
        
    



#conf = asyncio.run(calibrate())
# print(conf)




