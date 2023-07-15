from charging import charging_deamon, charge
from charging import gl as gl_ch
from mqtt_as import MQTTClient, config
from batt import get_bat
import uasyncio as asyncio
from transmit import globl
from machine import Pin, TouchPad
import neopixel
import esp32


MQTTClient.DEBUG = True  # Optional: print diagnostic messages
client = MQTTClient(config)
top = neopixel.NeoPixel(Pin(19), 2)



def callback(topic, msg, retained):
    print(topic, msg.decode("utf-8"))

async def conn_han(client):
    await client.subscribe('python/kpsska1387', 1)

config['subs_cb'] = callback
config['connect_coro'] = conn_han


async def main(client):
    try:
        await client.connect()
    except Exception:
        machine.reset()
        
    print("connected")
    await uasyncio.sleep_ms(200)
    top.fill((0,60,0))
    top.write()
    await uasyncio.sleep(0.9)
    top.fill((0,0,0))
    top.write()
    print("cube connected start programm")
    #event_loop.create_task(charging_deamon())
    #event_loop.create_task(charge())
    print("started")









time.sleep(1)

event_loop = uasyncio.get_event_loop()
event_loop.create_task(main(client))

event_loop.run_forever()

