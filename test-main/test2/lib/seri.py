import serial
import threading
import time

class Seriport(threading.Thread):

  def __init__(self,portname,baudrate):

    self.baudrate = baudrate
    self.portname = portname
    self.seri = serial.Serial(port=self.portname,baudrate=self.baudrate,
        parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,timeout=0.2
    )
    self.control = False
    self.rxArrivedFlag = False
    self.rxData = ""

  def sendString(self,data):

    self.seri.write((data))

  def listenStart(self):

    self.control = True
    self.thread = threading.Thread(None, self.run, None, (), {})
    self.thread.start()

  def run(self):

    while self.control == True :
        if self.seri.inWaiting()  != 0 :
            len = self.seri.inWaiting()
            self.rxData = self.seri.read(len)
            self.rxArrivedFlag = True
        time.sleep(0.01)

  def getData(self):

    if self.rxArrivedFlag == True:
        self.rxArrivedFlag = False
        return 1
    else :
        return 0

