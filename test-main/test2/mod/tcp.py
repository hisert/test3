import time
import socket
import threading

class Tcp(threading.Thread):

  def __init__(self,ip,port):

      self.ip = ip
      self.port = port
      self.control = False
      self.rxArrivedFlag = False
      self.rxData = ""


  def connect(self):

      self.socket = socket.socket()
      self.connectState = False
      self.thread2 = threading.Thread(None, self.run2, None, (), {})
      self.thread2.start()

  def run2(self):
      while True :
          try :
              self.socket.connect((self.ip, self.port))
          except:
              time.sleep(1)
  
  def sendString(self,data):

      try :
          self.socket.send(data)
      except :
          self.connect()

  def listenStart(self):

      self.control = True
      self.thread = threading.Thread(None, self.run, None, (), {})
      self.thread.start()

  def listenStop(self):
   
      self.control = False

  def run(self):

      while self.control == True :
          try:
              tx = self.socket.recv(1024)
              if len(tx)== 0:
                  self.listenStop()
                  time.sleep(1)
                  self.socket.close();
                  time.sleep(1)
                  self.connect()
                  self.listenStart()
              elif tx != "":
                  self.rxData = tx
                  self.rxArrivedFlag = True
              else :
                  self.rxArrivedFlag = False
          except :
              pass
          time.sleep(0.1)

  def getData(self):

      if self.rxArrivedFlag == True:
          self.rxArrivedFlag = False
          return 1
      else :
          return 0



