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
gl = globl()


report = "----------------\n" \
         "Date: {}\n" \
         "Time: {}\n" \
         "Charging: {}\n" \
         "CPU temp: {}\n" \
         "IMU / CHRG temp: {}\n" \
         "Batt level: {}\n" \
         "CPU freq: {}\n" \
         "----------------"

def callback(topic, msg, retained):
    # print((topic, msg, retained))
    print(msg.decode("utf-8"))
    message = [msg.decode("utf-8"), 1]
    gl.msg = message
    print(gl.msg)

async def as_callback():
    while True:
        callback = gl.msg
        flag = callback[1]
        msg = callback[0]
        if flag == 1:
            callback[1] = 0
            gl.msg = callback
            if "mig" in msg:
                await mig()
        await asyncio.sleep_ms(45)

async def conn_han(client):
    await client.subscribe('python/kpsska1387', 1)

config['subs_cb'] = callback
config['connect_coro'] = conn_han


async def main(client):
    await client.connect()
    print("connected")
    await uasyncio.sleep_ms(200)
    top.fill((0,60,0))
    top.write()
    await uasyncio.sleep(0.9)
    top.fill((0,0,0))
    top.write()

async def wait_con():
    try:
        await main(client)
    except Exception:
        machine.reset()
    print("cube connected start programm")
    event_loop.create_task(charging_deamon())
    event_loop.create_task(charge())
    event_loop.create_task(send_report())
    print("started")

async def send_report():
    while True:
        tc = (esp32.raw_temperature()-32.0)/1.8
        date = (time.localtime()[0], time.localtime()[2], time.localtime()[1])
        tim = (time.localtime()[3], ":", time.localtime()[4])
        rep = report.format(date, tim,
                    gl_ch.charging,
                    tc,
                    None,
                    get_bat(),
                    machine.freq())
        await client.publish('python/kpsska1387', rep, qos = 1)
        await asyncio.sleep(60)


time.sleep(5)
event_loop = uasyncio.get_event_loop()
event_loop.create_task(wait_con())
# event_loop.create_task(main(client))
event_loop.create_task(as_callback())
event_loop.run_forever()
