import OPi.GPIO as GPIO
import threading
import time

GPIO.setboard(GPIO.PCPCPLUS)
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

class SoftPwm(threading.Thread):

  def __init__(self,gpioPin):

      self.baseTime = 1.0
      self.maxCycle = 100.0
      self.sliceTime = self.baseTime / self.maxCycle
      self.pin = gpioPin
      self.control = False

  def start(self, dutyCycle):
    
      self.dutyCycle = dutyCycle
      if self.control == False :
          self.control = True
          GPIO.setup(self.pin, GPIO.OUT)
          GPIO.setwarnings(False)
          self.thread = threading.Thread(None, self.run, None, (), {})
          self.thread.start()

  def run(self):
      while self.control == True:
          if self.dutyCycle > 0:
              GPIO.output(self.pin, GPIO.HIGH)
              time.sleep(self.dutyCycle * self.sliceTime)
      
          if self.dutyCycle < self.maxCycle:
              GPIO.output(self.pin, GPIO.LOW)
              time.sleep((self.maxCycle - self.dutyCycle) * self.sliceTime)

  def setDuty(self, dutyCycle):
   
      self.dutyCycle = dutyCycle

  def setFreq(self, frequency):
    
      self.baseTime = 1.0 / frequency
      self.sliceTime = self.baseTime / self.maxCycle

  def stop(self):
   
      self.control = False
      GPIO.output(self.pin, GPIO.LOW)

