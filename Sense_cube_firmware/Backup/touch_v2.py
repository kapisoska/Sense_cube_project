"""
по идее полностью асинхронный
есть:
1. одинарное нажатие
2. двойное
3. долгое 
"""


import machine
import neopixel
from machine import TouchPad, Pin
import uasyncio as asyncio
import time
from transmit import globl
from hsv_to_rgb import hsv_to_rgb

gl = globl()
top = neopixel.NeoPixel(Pin(19), 2)
gl.change_color = True
gl.color = 0
gl.brightness = 1.0
t = TouchPad(Pin(33))
# 690


def double_click_callback():
    gl.change_color = not gl.change_color
    print("bool reversed")

def single_click_callback():
    print("single callback")

count = 0
revers = False
def long_click_callback():
    global count
    global revers
    if revers:
        print("long callback:  ", gl.brightness)
        if gl.brightness > 0.0:
            gl.brightness -= 0.01
            if not gl.change_color:
                top.fill(hsv_to_rgb(gl.color, 1, gl.brightness))
                top.write()


    else:
        print("long callback:  ", gl.brightness)
        if gl.brightness < 1.0:
            gl.brightness += 0.01
            if not gl.change_color:
                top.fill(hsv_to_rgb(gl.color, 1, gl.brightness))
                top.write()



flagg = True
def o_click():
    global flagg
    if t.read() < 690 and flagg:
        flagg = False
        return True
    if t.read() > 690 and not flagg:
        flagg = True


async def detect_sc_click():
    time = 0
    while time < 250:
        if o_click():
            return True
        time += 1
        await asyncio.sleep_ms(1)
    return False


flag = True
async def click():
    global flag
    global revers
    while True:
        if o_click() and flag:
            flag = False
            second = await detect_sc_click()
            if second:
                double_click_callback()
                print("double click")
            else:
                if t.read() < 690:
                    await asyncio.sleep_ms(300)
                    if t.read() < 690:
                        while t.read() < 690:
                            long_click_callback()
                            # print("long click")
                            await asyncio.sleep_ms(55)
                        revers = not revers
                else:
                    single_click_callback()
                    print("one short click")
        if t.read() > 690 and not flag:
            flag = True
        await asyncio.sleep_ms(70)
#---------------------------------------------------------------


async def change_col():
    while True:
        if gl.change_color:
            if gl.color < 360:
                gl.color += 1
                top.fill(hsv_to_rgb(gl.color, 1, gl.brightness))
                top.write()
                await uasyncio.sleep_ms(20)
            else:
                gl.color = 0
            await uasyncio.sleep_ms(40)
        else:
            await uasyncio.sleep_ms(30)



event_loop = uasyncio.get_event_loop()
event_loop.create_task(change_col())
event_loop.create_task(click())
event_loop.run_forever()
