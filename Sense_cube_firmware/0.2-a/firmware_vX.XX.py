# TODO: save touch config to file and load
# TODO: refactor callback into class
# TODO: rewrite calibrate algoritm 


import json
import esp32
import neopixel
import uasyncio as asyncio
from machine import Pin, TouchPad, reset

from ftp import ftpserver
from mqtt_as import MQTTClient, config

from charging  import gl as gl_ch, charging_deamon, charge
from batt import get_bat
from calibrate_v2 import calibrate
from touch_v3 import config as tconfig, Button
from heart_beat import heart_beat as heart
from ftp_controller import enable_ftp, disable_ftp
from chrg_isconnected import chrg_isconnected as on_charge
from hsv_to_rgb import hsv_to_rgb, temp

MQTTClient.DEBUG = True
buton = TouchPad(Pin(33))
task = {}
top = neopixel.NeoPixel(Pin(19), 2)
report = "----------------\n" \
         "Date: {}\n" \
         "Time: {}\n" \
         "Charging: {}\n" \
         "CPU temp: {}\n" \
         "IMU / CHRG temp: {}\n" \
         "Batt level: {}\n" \
         "CPU freq: {}\n" \
         "----------------"




# ------------------ MQTT settings
def callback(topic, msg, retained):
    senscube.callback(topic, msg, retained)

async def conn_han(client):
    await client.subscribe('remote', 1)
    # await client.subscribe('result', 1)

async def main(client):
    await client.connect()
    print("connected")
    await client.publish('python/kpsska1387', "Cube 001 is start", qos = 1)
    senscube.sw_mode(False)
    
config['subs_cb'] = callback
config['connect_coro'] = conn_han
client = MQTTClient(config)
# ------------------



        
# ------------------   Touch Config  
async def ocb():
    #print("ocb")
    #senscube.cocb()
    await heart_anim(True)    
    
def lcb(revers):
    #print("lcb", revers)
    senscube.clcb(revers)
    print(task)
    
def dcb():
    #print("dcb")
    senscube.cdcb()
    senscube.sw_mode()
tconfig["cback"] = ocb
tconfig["lback"] = lcb
tconfig["dback"] = dcb
# ------------------   Touch Config  


async def mode1(): # Color wheel
    while True:
        for h in range(360):
                top.fill(hsv_to_rgb(h, 1, 1))
                top.write()
                await uasyncio.sleep_ms(50)

async def heart_anim(send_msg):
    if senscube.IsChargeMode:
        senscube.disable_charge_mode()
        await heart()
        if send_msg:
            await client.publish('result', 'heart', qos = 1)
        senscube.enable_charge_mode()
    else:
        await heart()
        if send_msg:
            await client.publish('result', 'heart', qos = 1)
        top.fill((0,0,0))
        top.write()


class Device:
    def __init__(self):
        self._charge_f = False
        self._mode1_f = False
        self._reports_f = False
        self.cur_mode = 0
        self._touch_conf_nodock = 100
        self._touch_conf_ondock = 100
    
    # ------------------- config for touch
    def clcb(self, revers):
        print("lcb", revers)
    def cdcb(self):
        print("dcb")
        if self._charge_f:
            self.disable_charge_mode()
            self.enable_mode1()
            self._mode1_f = True
            self._charge_f = False
            return True
            
        if self._mode1_f:
            self.disable_mode1(self)
            self.enable_charge_mode(self)
            self._mode1_f = False
            self._charge_f = True
            return True
    # -------------------   
        
    def callback(self, topic, msg, retained):
        msg = msg.decode("utf-8")
        print(msg)
        if "on_chrg" == msg:
            if not self._charge_f:
                self.chrg_dem = event_loop.create_task(charging_deamon())
                self.chrg = event_loop.create_task((charge()))
                self._charge_f = True
            
        if "off_chrg" == msg:
            if self._charge_f:
                self.chrg_dem.cancel()
                self.chrg.cancel()
                top.fill((0,0,0))
                top.write()
                self._charge_f = False
        
        if "calibrate" == msg:
            if self._charge_f:
                self.chrg_dem.cancel()
                self.chrg.cancel()    
            event_loop.create_task(self.calibr())

        if "get_sens" == msg:
            print(self._touch_sens)
        
        if "start_rep" == msg:
            if not self._reports_f:
                self.reports = event_loop.create_task(self.reporting())
                self._reports_f = True
            
        if "stop_rep" == msg:
            if self._reports_f:
                self.reports.cancel()
                self._reports_f = False
                
        if "s_rep" == msg:
            event_loop.create_task(self.single_report())
            
        if "heart" == msg:
            event_loop.create_task(heart_anim(False))
                
        if "en_ftp" == msg:
            enable_ftp()
            print("resetting to ftp mode")
            reset()
        
        if "st" == msg:
            event_loop.create_task(self.sec_but_r())
            
        if "reset" == msg:
            reset()
    
        if "sw" == msg:
            self.sw_mode()
    
        if "1" == msg:
            self.cur_mode = 0
            self.sw_mode(self, False)    
    
        if "2" == msg:
            self.cur_mode = 1
            self.sw_mode(False)
            
        if "3" == msg:
            self.cur_mode = 2
            self.sw_mode(False)             
    
    
    def sw_mode(self, switch = True):
        if switch:
            if self.cur_mode < 2:
                self.cur_mode += 1
            else:
                self.cur_mode = 0
            print(self.cur_mode)
        
        if self.cur_mode == 0:
            print("mode 1")
            self.enable_mode1()
        
        if self.cur_mode == 1:
            print("mode 2")
            self.disable_mode1()
            self.enable_charge_mode()
            
        if self.cur_mode == 2:
            print("mode 3")
            self.disable_charge_mode()
    
    def disable_mode1(self):
        self.mode1.cancel()
    
    def enable_mode1(self):
        self.mode1 = event_loop.create_task(mode1())
    
    def disable_charge_mode(self):
        self.chrg_dem.cancel()
        self.chrg.cancel()
        top.fill((0,0,0))
        top.write()
            
    def enable_charge_mode(self):
        self.chrg_dem = event_loop.create_task(charging_deamon())
        self.chrg = event_loop.create_task((charge()))
        
        
    async def sec_but_r():
        await client.publish('report', "value: {}".format(buton.read()), qos = 1)
    
    async def calibr(self):
        print("start calibrating")
        touch = await calibrate()
        print("calibrating finished touch: ", touch)
        if touch[1]:
            self._touch_conf_ondock = touch[0]
            sensor.sens = touch[0]
        else:
            self._touch_conf_nodock = touch[0]
            
    async def update_on_dock(self):
        no_repeat_f = True
        while True:
            if on_charge() and no_repeat_f:
                sensor.sens = self._touch_conf_ondock
                no_repeat_f = False
                print("switch sensetivy to ONdock params")
                
            if not on_charge() and not no_repeat_f:
                sensor.sens = self._touch_conf_nodock
                no_repeat_f = True
                print("switch sensetivy to NOdock params")
            
            
                
            
            await asyncio.sleep_ms(60)
        
         
    async def reporting():
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
        
    async def single_report():
            tc = (esp32.raw_temperature()-32.0)/1.8
            date = (time.localtime()[0], time.localtime()[2], time.localtime()[1])
            tim = (time.localtime()[3], ":", time.localtime()[4])
            rep = report.format(date,
                        tim,
                        gl_ch.charging,
                        tc,
                        None,
                        get_bat(),
                        machine.freq())
            await client.publish('reports', rep, qos = 1)

    
    @property
    def IsChargeMode(self):
        return self._charge_f   

        
senscube = Device()
sensor = Button(33)

# Start firmware or ftpserver
with open('config.json', 'r') as jsonfile:
    config_file = json.load(jsonfile)
    if config_file["start_ftp"]:
        import network
        sta_if = network.WLAN(network.STA_IF)
        if not sta_if.isconnected():
            print('connecting to network...')
            sta_if.active(True)
            sta_if.connect("Beerloga", 'tm9044725501')
            while not sta_if.isconnected():
                pass
        print('network config:', sta_if.ifconfig())
        print("starting ftp server")
        ftpserver()
        print("server stopped")
        disable_ftp()
        reset()
    else:
        print("startup firmware")
        # Create main tasks
        event_loop = uasyncio.get_event_loop()
        task["MQTT"] = event_loop.create_task(main(client))
        task["Touch"] = event_loop.create_task(sensor.click())
        task["Dock_updater"] = event_loop.create_task(senscube.update_on_dock())
        event_loop.run_forever()









