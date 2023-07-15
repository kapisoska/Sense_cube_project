from machine import SoftI2C
from imu import MPU6050
from machine import Pin
from mqtt_as import MQTTClient, config
import uasyncio as asyncio
import machine
import neopixel
pin = machine.Pin(32, machine.Pin.OUT)
status = neopixel.NeoPixel(machine.Pin(27), 1)
top = neopixel.NeoPixel(machine.Pin(33), 2)
vibro = uasyncio.get_event_loop()


action1 = "b'vb'"
action2 = "b'lgvb'"
ledon = "b'ldon'"
ledoff = "b'ldoff'"


async def vibro():
    for i in range(3):
        print("act_vibro")
        pin.value(1)
        await uasyncio.sleep_ms(70)
        pin.value(0)
        await uasyncio.sleep_ms(70)


async def long_vibro():

    pin.value(1)
    await uasyncio.sleep(1)
    pin.value(0)

SERVER = 'broker.emqx.io'  # Change to suit e.g. 'iot.eclipse.org'


def callback(topic, msg, retained):
    print((topic, msg, retained))

    if str(msg) == action1:
        print("vibro")

        uasyncio.create_task(vibro())

    elif str(msg) == action2:
        print("long vibro")
        uasyncio.create_task(long_vibro())
    elif str(msg) == ledon:
        print("led on")
        status[0] = (250, 250, 250)
        status.write()
        # ----------------
        for i in range(2):
            top[i] = (0, 250, 0)
        top.write()

    elif str(msg) == ledoff:
        print("led off")
        status[0] = (0, 0, 0)
        status.write()
        # ----------------
        for i in range(2):
            top[i] = (0, 0, 0)
        top.write()


async def conn_han(client):
    await client.subscribe('python/kpsska1387', 1)


async def main(client):
    await client.connect()
    print("connected")
    await uasyncio.sleep_ms(200)
    status[0] = (0, 60, 0)
    status.write()
    await uasyncio.sleep(0.9)
    status[0] = (0, 0, 0)
    status.write()


config['subs_cb'] = callback
config['connect_coro'] = conn_han
config['server'] = SERVER
config['ssid'] = "Beerloga"
config['wifi_pw'] = "tm9044725501"
MQTTClient.DEBUG = False  # Optional: print diagnostic messages


client = MQTTClient(config)


i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
imu = MPU6050(i2c)
imu.accel_range = 2


async def pub():
    while True:
        # print(imu.accel.xyz)
        if (imu.accel.y) > 6 or (imu.accel.x) > 6 or (imu.accel.z) > 6:
            print("move")
            await client.publish('python/kpsska1387', "move, {}".format(imu.accel.xyz), qos=1)
        await uasyncio.sleep_ms(50)


event_loop = uasyncio.get_event_loop()
event_loop.create_task(pub())
event_loop.create_task(main(client))
event_loop.run_forever()

"""
try:
    asyncio.run(pub())
    asyncio.run(main(client))
finally:
    client.close()  # Prevent LmacRxBlk:1 errors
    """
