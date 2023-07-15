import neopixel
from machine import Pin
import time
import machine

top = neopixel.NeoPixel(Pin(19), 2)

def beat():
    top.fill((255,0,0))
    top.write()
    time.sleep(0.2)
    top.fill((80,0,0))
    top.write()
    
""" 
beat()
time.sleep(0.2)
beat()
time.sleep(0.6)
beat()
time.sleep(0.2)
beat()
"""

def sm_beat():
    i = 120
    while i < 255:
        print(i)
        top.fill((i,0,0))
        top.write()
        time.sleep_us(30)
        i += 1
    time.sleep(0.1)
    while i > 120:
        print(i)
        top.fill((i,0,0))
        top.write()
        time.sleep_us(30)
        i -= 1
      
    time.sleep(0.15)
    while i < 255:
        print(i)
        top.fill((i,0,0))
        top.write()
        time.sleep_us(30)
        i += 1
    time.sleep(0.1)
    while i > 120:
        print(i)
        top.fill((i,0,0))
        top.write()
        time.sleep_us(1000)
        i -= 1        


"""
sm_beat()
time.sleep(0.25)
sm_beat()
"""

pin = machine.Pin(25,machine.Pin.OUT)

def vibro_beat():
    pin.value(1)
    time.sleep_ms(120)
    pin.value(0)

    

def heart_vibro():
    vibro_beat()
    time.sleep_ms(150)
    vibro_beat()
    time.sleep(0.34)
    vibro_beat()
    time.sleep_ms(150)
    vibro_beat()

while True:
    heart_vibro() 
    time.sleep(3)











