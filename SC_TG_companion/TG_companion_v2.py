"""
list of MQTT commands:

on_chrg --- включить анимацию зарядки
off_chrg --- отключить анимацию зарядки
calibrate --- запустить калибровку тач панели
get_sens --- получить значение тач сенсора по serial порту
start_reports --- включить отправку отчетов каждую минуту
stop_reports --- отключить отправку отчетов каждую минуту
single_report --- отправить отчет один раз
heart --- принудительный запуск анимации сердца
enable_ftp --- перезагрузить устройство для перепрошивки
st --- получить значение тач сенсора по MQTT
reset --- restart device
"""

import random
import time
import paho.mqtt.publish as publish
import telebot
from telebot import types
import paho.mqtt.client as paho

from config import bot_key
bot = telebot.TeleBot(bot_key)  # SensCubeRemote_bot

broker = 'm5.wqtt.ru'
port = 5530
topic = "python/kpsska1387"
client_id = f'python-mqtt-{random.randint(0, 10000)}'
username = 'admin'
password = 'HnYyjwYA'
lis_of_msg = []


def list_to_del(ms_id, deleted_msg=None):
    if ms_id:
        lis_of_msg.append(ms_id)
    elif deleted_msg:
        lis_of_msg.remove(deleted_msg)
    else:
        return lis_of_msg


def on_message(client, userdata, message):
    time.sleep(1)

    rcv_msg = str(message.payload.decode("utf-8"))
    print("received message =", rcv_msg)
    if "move" in rcv_msg:
        res = bot.send_message(chat_id=240077398, text="Принята таблетка {}".format(remain))
        ms_id = res.message_id
        list_to_del(ms_id)
        print(res.message_id)
    if "report" in rcv_msg:
        res = bot.send_message(chat_id=240077398, text=rcv_msg)
        ms_id = res.message_id
        list_to_del(ms_id)
        print("Report received")
    if "mig" in rcv_msg:
        res = bot.send_message(chat_id=240077398, text="mig")
        ms_id = res.message_id
        list_to_del(ms_id)
        print(res.message_id)


client = paho.Client(client_id)
client.username_pw_set(username, password)
client.on_message = on_message
print("connecting to broker ", broker)
client.connect(broker, port)  # connect
client.loop_start()  # start loop to process received messages
print("subscribing ")
client.subscribe("python/kpsska1387")  # subscribe

# bot.delete_message(chat_id = 240077398, message_id = message.message_id)


crossIcon = u"\u274C"
crossIcon2 = U"\u2588"

keyboard_4_but = [
    [
        types.InlineKeyboardButton("ON charge", callback_data='on_chrg'),
        types.InlineKeyboardButton("OFF charge", callback_data='off_chrg'),

    ],
    [
        types.InlineKeyboardButton("Start reports", callback_data='start_reports'),
        types.InlineKeyboardButton("Stop reports", callback_data='stop_reports'),
    ],
    [
        types.InlineKeyboardButton("Single report", callback_data="single_report"),
    ],
    [
        types.InlineKeyboardButton("Calibrate", callback_data='calibrate'),
    ],
    [
        types.InlineKeyboardButton("Get touch", callback_data='st'),
    ],
    [
        types.InlineKeyboardButton("Heart", callback_data='heart'),
    ],
    [
        types.InlineKeyboardButton("Update Firmware", callback_data='enable_ftp'),
    ],
    [
        types.InlineKeyboardButton("RESET", callback_data='reset'),
    ],
]

kbrd = types.InlineKeyboardMarkup(keyboard_4_but)


@bot.message_handler(commands=["start"])
def inline(message):
    print("has started")
    bot.send_message(message.chat.id, "Menu:", reply_markup=kbrd)
    print(message.chat.id)


if client.on_message:
    print("lox")


def delete_log():
    if list_to_del(None):
        for msg in list_to_del(None):
            bot.delete_message(chat_id=240077398, message_id=msg)
            list_to_del(None, msg)
        if list_to_del(None):
            delete_log()
        else:
            pass


@bot.callback_query_handler(func=lambda c: True)
def inline(c):
    if c.data == 'on_chrg':
        print("on_chrg")
        client.publish("remote", "on_chrg")

    if c.data == 'off_chrg':
        print("off_chrg")
        client.publish("remote", "off_chrg")

    if c.data == 'calibrate':
        print("calibrate")
        client.publish("remote", "calibrate")

    if c.data == 'start_reports':
        print("start_reports")
        client.publish("remote", "start_reports")

    if c.data == 'stop_reports':
        print("stop_reports")
        client.publish("remote", "stop_reports")

    if c.data == 'single_report':
        print("single_report")
        client.publish("remote", "single_report")

    if c.data == 'heart':
        print("heart")
        client.publish("remote", "heart")

    if c.data == 'enable_ftp':
        print("enable_ftp")
        client.publish("remote", "enable_ftp")

    if c.data == 'st':
        print("st")
        client.publish("remote", "st")

    if c.data == 'reset':
        print("reset")
        client.publish("remote", "reset")


bot.polling(none_stop=True, interval=0)
