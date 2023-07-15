"""
Полностью асинхронный
Реализация однократного, двойного, долгого касания
для каждого действия можно установить асинхронный callback
"""
from machine import TouchPad, Pin
import uasyncio as asyncio

config = {
    "cback": lambda *_: None,
    "lback": lambda *_: None,
    "dback": lambda *_: None,
}




class Button:
    def __init__(self, pin):
        self.but = TouchPad(Pin(pin))
        self._t_conf = 590
        self._flagg = True
        self._flag = True
        self._revers = False
        self._cback = config["cback"]
        self._lback = config["lback"]
        self._dback = config["dback"]

    def o_click(self):
        if self.but.read() < self._t_conf and self._flagg:
            self._flagg = False
            return True
        if self.but.read() > self._t_conf and not self._flagg:
            self._flagg = True


    async def detect_sc_click(self):
        time = 0
        while time < 250:
            if Button.o_click(self):
                return True
            time += 1
            await asyncio.sleep_ms(1)
        return False


    async def click(self):
        while True:
            if Button.o_click(self) and self._flag:
                self._flag = False
                second = await Button.detect_sc_click(self)
                if second:
                    self._dback() # double cb
                    print("double click")
                else:
                    if self.but.read() < self._t_conf:
                        await asyncio.sleep_ms(300)
                        if self.but.read() < self._t_conf:
                            while self.but.read() < self._t_conf:
                                self._lback(self._revers) # long cb
                                print("long click", self._revers)
                                await asyncio.sleep_ms(55)
                            self._revers = not self._revers
                    else:
                        self._cback() # one short cb
                        print("one short click")
            if self.but.read() > self._t_conf and not self._flag:
                self._flag = True
            await asyncio.sleep_ms(70)


#sensor = Button(33)

#event_loop = uasyncio.get_event_loop()
#event_loop.create_task(sensor.click())
#event_loop.run_forever()
