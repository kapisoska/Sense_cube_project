"""
chrg_isconnected
Batt
charging



"""
from machine import Pin, ADC
import uasyncio as asyncio
import neopixel

from transmit import globl

top = neopixel.NeoPixel(Pin(19), 2)
gl = globl() 

batt = ADC(Pin(36))  # 36 пин для акб
batt.atten(ADC.ATTN_6DB)  # Full range: 2.0v
ADC.width(ADC.WIDTH_12BIT)  # Расширение 4095
chrg = ADC(Pin(32))  # 32 пин для зарядки
chrg.atten(ADC.ATTN_6DB)  # Full range: 2.0v
ADC.width(ADC.WIDTH_12BIT)  # Расширение 4095


def adc_to_voltage(unscaled):  # Функция перевода значения с АЦП в напряжение
    to_min = 0
    to_max = 2
    from_min = 0
    from_max = 4095
    return (to_max - to_min) * (unscaled - from_min) / (from_max - from_min) + to_min

def get_bat():
    adc_value = batt.read()  # Получение значения с АЦП
    x = adc_to_voltage(adc_value) * 2.92
    k = (-0.0241 * x) + 1.074  # Формула для вычисления коэфицента
    return adc_to_voltage(adc_value) * 2.92 * k

def chrg_isconnected():
    adc_value = chrg.read()  # Получение значения с АЦП
    x = adc_to_voltage(adc_value) * 2.92
    k = (-0.0241 * x) + 1.074  # Формула для вычисления коэфицента
    if (adc_to_voltage(adc_value) * 2.92 * k) > 2.0:
        return True
    else:
        return False

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
event_loop.create_task(charging_deamon())
event_loop.create_task(charge())
event_loop.run_forever()
"""







    