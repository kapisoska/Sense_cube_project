# import uasyncio
# import neopixel
# from machine import Pin

# event_loop = uasyncio.get_event_loop()
# led = neopixel.NeoPixel(Pin(19), 2)


def hsv_to_rgb(h, s, v):
    h = h / 360
    if s == 0.0:
        v *= 255
        return v, v, v
    i = int(h * 6.)  
    f = (h * 6.) - i
    p, q, t = int(255 * (v * (1. - s))), int(255 * (v * (1. - s * f))), int(255 * (v * (1. - s * (1. - f))))
    v *= 255
    i %= 6
    v = int(v)
    i = int(i)
    if i == 0:
        return v, t, p
    if i == 1:
        return q, v, p
    if i == 2:
        return p, v, t
    if i == 3:
        return p, q, v
    if i == 4:
        return t, p, v
    if i == 5:
        return v, p, q



"""
async def temp():
    while True:
        for h in range(360):
                led.fill(hsv_to_rgb(h, 1, 1))
                led.write()
                await uasyncio.sleep_ms(50)






event_loop.create_task(temp())
event_loop.run_forever()
"""


