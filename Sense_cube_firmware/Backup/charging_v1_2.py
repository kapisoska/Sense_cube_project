import uasyncio as asyncio
from transmit import globl
from machine import Pin
import neopixel
from chrg_isconnected import chrg_isconnected


top = neopixel.NeoPixel(Pin(19), 2)
gl = globl() 



async def charging_deamon():
    while True:

        if chrg_isconnected():
            gl.charging = True
        else:
            gl.charging = False
        await asyncio.sleep_ms(70)
        


async def charge():
    g = 0
    r = 0
    while True:
        if gl.charging:
            r = 0
            while gl.charging:
                if g < 150:
                    while g < 150 and gl.charging:
                        g += 1
                        top.fill((0,g,0))
                        top.write()
                        await asyncio.sleep_ms(20)
                else:
                    while g > 0 and gl.charging:
                        g -= 1
                        top.fill((0,g,0))
                        top.write()
                        await asyncio.sleep_ms(20)               
        else:
            g = 0
            while not gl.charging:
                if r < 150:
                    while r < 150 and not gl.charging:
                        r += 1
                        top.fill((r,g,0))
                        top.write()
                        await asyncio.sleep_ms(20)
                else:
                    while r > 0 and not gl.charging:
                        r -= 1
                        top.fill((r,g,0))
                        top.write()
                        await asyncio.sleep_ms(20)
        await asyncio.sleep_ms(40)



        
        
"""
event_loop = uasyncio.get_event_loop()
event_loop.create_task( charging_deamon() )
event_loop.create_task( charge() )
# event_loop.create_task(  )
event_loop.run_forever()
"""
