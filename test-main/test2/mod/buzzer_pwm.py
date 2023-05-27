import sys
import time
import threading
sys.path.append('./lib')
from soft_pwm import *

waittime = 0.1
tone_open = [
[300,waittime],
[400,waittime],
[500,waittime],
[600,waittime],
[700,waittime],
[800,waittime],
[900,waittime],
[1000,waittime],
[1100,waittime],
[1200,waittime],
[1300,waittime],
[1400,waittime],
[1500,waittime],
]
tone_close = [
[1500,waittime],
[1400,waittime],
[1300,waittime],
[1200,waittime],
[1100,waittime],
[1000,waittime],
[900,waittime],
[800,waittime],
[700,waittime],
[600,waittime],
[500,waittime],
[400,waittime],
[300,waittime],
]

class BuzzerPwm(threading.Thread):

  def __init__(self,pin):

      self.pwm = SoftPwm(pin)
      self.pwm.setFreq(1)
      self.control = False
      self.data = []
      self.data_old = []
      self.repeat = 0

  def tone_start(self,data_list,repeat):
      if self.control == False :
          self.repeat = repeat -1
          self.data = data_list.copy()
          self.data_old = data_list.copy()
          self.control = True
          self.pwm.setFreq(1)
          self.pwm.start(1)
          self.thread = threading.Thread(None, self.run, None, (), {})
          self.thread.start()

  def stop(self):

      self.control = False

  def run(self):

      while self.control == True :
          if len(self.data) != 0 :
              self.pwm.setFreq(self.data[0][0])
              time.sleep(self.data[0][1])             
              self.data.pop(0)
          else :
              if self.repeat != 0 :
                  self.repeat = self.repeat - 1
                  self.data = self.data_old.copy()
              else :
                  self.stop()
                  self.pwm.stop()
                  self.pwm.setFreq(1)
                  self.pwm.setDuty(1)
                  break
      