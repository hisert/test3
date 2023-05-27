from pyA20.gpio import gpio
from pyA20.gpio import port
import threading
import time

gpio.init()

class TooglePort(threading.Thread):

  def __init__(self,pin,opTime,clTime):

    self.pin = pin
    self.openTime = opTime
    self.closeTime = clTime
    self.control = False

  def start(self):

    gpio.setcfg(self.pin, gpio.OUTPUT)
    self.control = True
    self.thread = threading.Thread(None, self.run, None, (), {})
    self.thread.start()

  def stop(self):

    self.control = False

  def changeTiming(self,opTime,clTime):
    
    self.openTime = opTime
    self.closeTime = clTime

  def run(self):

    while self.control == True :
      gpio.output(self.pin, gpio.HIGH)
      time.sleep(self.openTime)
      gpio.output(self.pin,gpio.LOW)
      time.sleep(self.closeTime)