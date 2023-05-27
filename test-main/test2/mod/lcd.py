import smbus
import time

LCD_WIDTH = 16   # Maximum characters per line

LCD_CHR = 1 # Mode - Sending data
LCD_CMD = 0 # Mode - Sending command

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
LCD_LINE_3 = 0x94 # LCD RAM address for the 3rd line
LCD_LINE_4 = 0xD4 # LCD RAM address for the 4th line

LCD_BACKLIGHT  = 0x08  # On
#LCD_BACKLIGHT = 0x00  # Off

ENABLE = 0b00000100 # Enable bit

E_PULSE = 0.0005
E_DELAY = 0.0005

class LcdI2C():
  def __init__(self,busname,adress):

      self.bus = smbus.SMBus(busname)
      self.I2C_ADDR = adress

  def init(self):
      # Initialise display
      self.writeByte(0x33,LCD_CMD) # 110011 Initialise
      self.writeByte(0x32,LCD_CMD) # 110010 Initialise
      self.writeByte(0x06,LCD_CMD) # 000110 Cursor move direction
      self.writeByte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off
      self.writeByte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
      self.writeByte(0x01,LCD_CMD) # 000001 Clear display
      time.sleep(E_DELAY)

  def writeByte(self,bits, mode):

      bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
      bits_low = mode | ((bits<<4) & 0xF0) | LCD_BACKLIGHT
      self.bus.write_byte(self.I2C_ADDR, bits_high)
      self.lcd_toggle_enable(bits_high)
      self.bus.write_byte(self.I2C_ADDR, bits_low)
      self.lcd_toggle_enable(bits_low)

  def getLine(self,line):
      if line == 1:
          return LCD_LINE_1
      elif line == 2:
          return LCD_LINE_2
      elif line == 3:
          return LCD_LINE_3
      elif line == 4:
          return LCD_LINE_4

  def lcd_toggle_enable(self,bits):

      time.sleep(E_DELAY)
      self.bus.write_byte(self.I2C_ADDR, (bits | ENABLE))
      time.sleep(E_PULSE)
      self.bus.write_byte(self.I2C_ADDR,(bits & ~ENABLE))
      time.sleep(E_DELAY)

  def writeString(self,message,line):

      message = message.ljust(LCD_WIDTH," ")
      self.writeByte(line, LCD_CMD)
      for i in range(LCD_WIDTH):
          self.writeByte(ord(message[i]),LCD_CHR)


