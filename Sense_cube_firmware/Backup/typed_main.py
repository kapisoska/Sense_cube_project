from charging import charging_deamon, charge
from charging import gl as gl_ch
from mqtt_as import MQTTClient, config
from batt import get_bat
import uasyncio as asyncio
from transmit import globl
from machine import Pin, TouchPad
import neopixel
import esp32


class Device:
    def __init__(self):
        self.client = None
    

    def callback(topic, msg, retained):
        print((topic, msg, retained))

    async def conn_han(client):
        await client.subscribe('foo_topic', 1)

    async def main(client):
        await client.connect()
        n = 0
        while True:
            await asyncio.sleep(5)
            print('publish', n)
            # If WiFi is down the following will pause for the duration.
            await client.publish('result', '{}'.format(n), qos = 1)
            n += 1

    config['subs_cb'] = callback
    config['connect_coro'] = conn_han

    MQTTClient.DEBUG = True  # Optional: print diagnostic messages
    self.client = MQTTClient(config)


    def start(self):
        asyncio.run(Device.main(self.client))


sens = Device()
Device.start()








    
    
    
    
    
    
    