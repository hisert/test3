from pyA20.gpio import gpio
from pyA20.gpio import port
import sys
import os
import time
import serial
import socket
import threading
sys.path.append('./mod')
sys.path.append('./lib')
from led_alive import *
from lcd import *
from seri import *
from tcp import *
from buzzer_pwm import *

def BUZZER_START():

    global my_buzzer
    my_buzzer = BuzzerPwm(port.PA10)
    my_buzzer = my_buzzer.tone_start(tone_open,1)

def LED_ALIVE():

    global my_led
    my_led = TooglePort(port.PA8,0.05,0.95)
    my_led.start()

def LCD():
    try:
        global LCD
        LCD = LcdI2C(0,0x20)
        LCD.init()
        LCD_SHOW_IP()
    except:
        pass

def LCD_SHOW_IP():

    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.connect(("8.8.8.8",80))
    hostname = socket.gethostname()
    ipaddress = s.getsockname()[0]
    LCD.writeString(ipaddress,LCD.getLine(1))
    LCD.writeString(hostname + " <3",LCD.getLine(2))

def SERIPORT2_DEBUG():

    global SERIPORT_DEBUG
    SERIPORT_DEBUG = Seriport('/dev/ttyS2',9600)
    SERIPORT_DEBUG.listenStart()

def SERIPORT1_TCP():
    global TCP_SERIPORT
    global SERIPORT_TCP
    SERIPORT_TCP = Seriport('/dev/ttyS1',9600)
    SERIPORT_TCP.listenStart()
    TCP_SERIPORT = Tcp("192.168.1.110",5000)
    TCP_SERIPORT.connect()
    TCP_SERIPORT.listenStart()

def BRIDGE_TCP_SERIAL_WHILE():

    if SERIPORT_TCP.getData() == 1 :
        TCP_SERIPORT.sendString(SERIPORT_TCP.rxData)
        PROCESS_RS485(SERIPORT_TCP.rxData)

    if TCP_SERIPORT.getData() == 1 :
        SERIPORT_TCP.sendString(TCP_SERIPORT.rxData)

def SERIPORT2_WHILE():

    if SERIPORT_DEBUG.getData() == 1 :
        SERIPORT_DEBUG.sendString(SERIPORT_DEBUG.rxData)

def PROCESS_RS485(data):
    if data == "<OPI SHUTDOWN>" :
        os.system("shutdown now")

def init():
    
    LCD()
    LED_ALIVE()
    SERIPORT2_DEBUG()
    SERIPORT1_TCP()
    BUZZER_START()
    time.sleep(2)

def loop():

    while(True):
        SERIPORT2_WHILE()
        BRIDGE_TCP_SERIAL_WHILE()

init()
loop()
