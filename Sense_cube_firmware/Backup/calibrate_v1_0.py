import machine
import neopixel
from machine import TouchPad, Pin
import uasyncio as asyncio
from transmit import globl


gl = globl()
top = neopixel.NeoPixel(Pin(19), 2)
t = TouchPad(Pin(33))
non_push = t.read()
print("non push: ", non_push)
top.fill((0,0,0))
top.write()

async def calibrate():
    r = 55
    print("yes")
    for i in range(2):
        while r < 220:
            r += 1
            top.fill([r,0,0])
            top.write()
            await asyncio.sleep_ms(7)
            
        while r > 55:
            r -= 1
            top.fill([r,0,0])
            top.write()
            await asyncio.sleep_ms(7)
            
        
    top.fill((0,0,255))
    top.write()
    await asyncio.sleep(2)
    clbr = t.read()
    gl.touch = clbr
    print(clbr)
    
    g = 10
    for i in range(2):
        while g < 200:
            g += 1
            top.fill([0,g,0])
            top.write()
            await asyncio.sleep_ms(7)
            
        while g > 11:
            g -= 1
            top.fill([0,g,0])
            top.write()
            await asyncio.sleep_ms(7)    
    
    
    

            


async def calibrate_manager():
    asyncio.run(calibrate())
    delta_touch = non_push - gl.touch
    if delta_touch < 7:
        while delta_touch < 7:
            asyncio.run(calibrate())
            delta_touch = non_push - gl.touch
    top.fill((0,0,0))
    top.write()
            

asyncio.run(calibrate_manager())




