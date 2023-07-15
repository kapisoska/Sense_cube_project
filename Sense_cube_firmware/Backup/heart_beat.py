import neopixel
from machine import Pin
import time
import machine
import uasyncio as asyncio


top = neopixel.NeoPixel(Pin(19), 2)
start_br = 60
br = 255
pin = machine.Pin(25,machine.Pin.OUT)


async def light_beat():
    i = start_br
    while i < br:
        i += 1
        #print(i)
        top.fill((i,0,0))
        top.write()
        await asyncio.sleep(0.0019)
    await asyncio.sleep(0.0015)
    while i > start_br:
        i -= 1
        #print(i)
        top.fill((i,0,0))
        top.write()
        await asyncio.sleep(0.0019)

async def heart_beat():
    await light_beat()
    await asyncio.sleep(0.15)
    await light_beat()
    await asyncio.sleep(0.6)
    await light_beat()
    await asyncio.sleep(0.15)
    await light_beat()


async def vibro_beat():
    pin.value(1)
    await asyncio.sleep_ms(120)
    pin.value(0)

async def heart_vibro():
    await vibro_beat()
    await asyncio.sleep_ms(190)
    await vibro_beat()
    await asyncio.sleep(0.44)
    await vibro_beat()
    await asyncio.sleep_ms(190)
    await vibro_beat()
