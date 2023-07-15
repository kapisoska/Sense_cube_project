"""
есть отслеживание двойного клика
есть отслеживание долгого нажатия с реверсом значений
нет отслаживания одинарного короткого нажатия 
"""

import machine
import neopixel
from machine import TouchPad, Pin
import uasyncio as asyncio
import time
from transmit import globl


gl = globl()
top = neopixel.NeoPixel(Pin(19), 2)
t = TouchPad(Pin(33))
# 690


async def long_click():
    count = 0
    i = 0
    flagg = True
    while True:
        if t.read() < 690 and flagg:
            await asyncio.sleep(1)
            if t.read() < 690:
                flagg = False
                while t.read() < 690 and i < 255:

                    i += 1
                    print(i)
                    top.fill((0,i,i))
                    top.write()
                    await asyncio.sleep_ms(5)
        if t.read() < 690 and not flagg:
            await asyncio.sleep(1)
            if t.read() < 690:
                flagg = True
                while t.read() < 690 and i > 0:

                    i -= 1
                    print(i)
                    top.fill((0,i,i))
                    top.write()
                    await asyncio.sleep_ms(5)





    await asyncio.sleep_ms(50)

# asyncio.run(long_click())






flag = True
def click():
    global flag
    if t.read() < 690 and flag:
        # print("send message")
        flag = False
        return True
    if t.read() > 690 and not flag:
        flag = True





async def detect_sc_click():
    time = 0

    while time < 250:
        # print(time)
        if click():
            # print("click 2")
            return True
        time += 1
        await asyncio.sleep_ms(1)
    return False


async def double_click():
    while True:
        if click():
            # print("send message")
            second = await detect_sc_click()
            # print(second)
            if second:
                print("double click")
                return True
            else:
                # print("not detected second click")
                return False


# asyncio.run(double_click())
# asyncio.run(detect_sc_click())
async def test():
    print("start func")

    count = 0
    count = 0
    i = 0
    flagg = True
    while True:
        db = await double_click()
        if db:
            count += 1
            print(count)






        if t.read() < 690 and flagg:
            await asyncio.sleep(1)
            if t.read() < 690:
                flagg = False
                while t.read() < 690 and i < 255:

                    i += 1
                    print(i)
                    top.fill((0,i,i))
                    top.write()
                    await asyncio.sleep_ms(5)

        if t.read() < 690 and not flagg:

            await asyncio.sleep(1)
            if t.read() < 690:
                flagg = True
                while t.read() < 690 and i > 0:

                    i -= 1
                    print(i)
                    top.fill((0,i,i))
                    top.write()
                    await asyncio.sleep_ms(5)







event_loop = uasyncio.get_event_loop()
#event_loop.create_task(single_click())
event_loop.create_task(test())
event_loop.run_forever()
