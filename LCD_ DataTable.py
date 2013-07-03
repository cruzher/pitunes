#!/usr/bin/python
#----------------------------------------------------------------
# Author: Chris Crumpacker                               
# Date: May 2013
#
# Testing a data table on an 20x4 LCD, 
# using a RaspberyPi and an MCP23017 I2C port expander
# 
# Using Adafruit_CharLCD code with the I2C and MCP230xx code as well
#----------------------------------------------------------------

from time import sleep
from Adafruit_CharLCDPlate4line import Adafruit_CharLCDPlate
from LCD_EoL_HandlingAnd4LineSupport import LCD_EoL_Handling

class LCD_DataTable(Adafruit_CharLCDPlate):
    # Limited to 4 characters, 
    # position is left or right, 
    # line is 1-4
    def updateHalfLabel(self, text, position, line):
        self.clearHalfDataSet(position,line)
        if position == "left":
            lcd.setCursor(0,line)
            eol.message(text[0:4]+':')        
        elif position == "right":
            lcd.setCursor(10,line)
            eol.message('|'+text[0:4]+':')
            
    # Limited to 4 characters, 
    # position is left or right, 
    # line is 1-4
    def updateHalfValue(self, text, position, line):
        if position == "left":
            lcd.setCursor(5,line)
            eol.message("    ")
            lcd.setCursor(5,line)
            eol.message(text[0:4])        
        elif position == "right":
            lcd.setCursor(16,line)
            eol.message("    ")
            lcd.setCursor(16,line)
            eol.message(text[0:4])
    
    # Writes up to a 9 character lable and value to a full line
    def updateWholeLineLabel(self, label, line):
        self.clearWholeLine(line)
        lcd.setCursor(0,line)
        eol.message(label[0:9] + ': ')
    
    # Writes up to a 9 character lable and value to a full line
    def updateWholeLineValue(self, value, line):
        lcd.setCursor(10,line)
        eol.message(value[0:10])
    
    #Clears an entire line
    def clearWholeLine(self, line):
        lcd.setCursor(0,line)
        eol.message(" " * columns)
    
    #Clears an entire line
    def clearWholeLineValue(self, line):
        lcd.setCursor(10,line)
        eol.message(" " * 10)
    
    # Clears just a half data set, label and value   
    def clearHalfDataSet(self, position,line):
        if position == "left":
            lcd.setCursor(0,line)
            eol.message(" " * 10)
        elif position == "right":
            lcd.setCursor(10,line)
            eol.message(" " * 10)
    
    # Clears just the value portion for a half data set
    def clearHalfValue(self, position,line):
        if position == "left":
            lcd.setCursor(5,line)
            eol.message("    ")      
        elif position == "right":
            lcd.setCursor(16,line)
            eol.message("    ")

#----------------------------------------------------------------
# Main program, just trowing bogus data "against the wall"
#----------------------------------------------------------------
if __name__ == '__main__':
    
    #lcd size reference
    columns = 20
    rows = 4
    
    eol = LCD_EoL_Handling()
    lcd = Adafruit_CharLCDPlate()
    dt = LCD_DataTable()
    
    lcd.begin(columns, rows)
    lcd.backlight(lcd.ON)
    lcd.clear()
    
    lcd.message("20x4 Table Testing")
    sleep(2)
    
    #Filling the table with bogus info
    lcd.clear()
    dt.updateHalfLabel("Temp","left",0)
    dt.updateHalfLabel("Mode","right",0)
    dt.updateHalfLabel("Targ","left",1)
    dt.updateHalfLabel("Fan","right",1)
    dt.updateHalfValue("Cool","right",0)
    dt.updateHalfValue("75.5","left",0)
    dt.updateHalfValue("Auto","right",1)
    dt.updateHalfValue("74.0","left",1)
    dt.updateWholeLineLabel("Tempurature",2)
    dt.updateWholeLineValue("Too Hot!!!",2)
    dt.updateWholeLineLabel("Humidity",3)
    dt.updateWholeLineValue("100%!!!",3)
        
    #Start testing updating and clearing parts
    
    # Clearing entire lines
    sleep(2)
    dt.clearWholeLine(0)
    sleep(1)
    dt.clearWholeLine(3)
    sleep(1)
    
    # Repopulating the lines just cleared
    dt.updateHalfLabel("Temp","left",0)
    dt.updateHalfValue("75.3","left",0)
    dt.updateHalfLabel("Mode","right",0)
    dt.updateHalfValue("Cool","right",0)
    dt.updateWholeLineLabel("Humidity",3)
    dt.updateWholeLineValue("100%!!!",3)
    sleep(2)
    
    # Clearing the entire Data set, both Label and Value
    dt.clearHalfDataSet("left",0)
    sleep(1)
    dt.clearHalfDataSet("right",0)
    sleep(1)
    dt.clearHalfDataSet("left",1)
    sleep(1)
    dt.clearHalfDataSet("right",1)
    sleep(2)
    
    # Repopulating the half labels and values just removed
    dt.updateHalfLabel("Temp","left",0)
    dt.updateHalfLabel("Mode","right",0)
    dt.updateHalfLabel("Targ","left",1)
    dt.updateHalfLabel("Fan","right",1)
    
    dt.updateHalfValue("75.5","left",0)
    dt.updateHalfValue("Cool","right",0)
    dt.updateHalfValue("74.0","left",1)
    dt.updateHalfValue("On","right",1)
    sleep(2)
    
    # Clearing the values in the half data sets
    dt.clearHalfValue("left",0)
    sleep(1)
    dt.clearHalfValue("right",0)
    sleep(1)
    dt.clearHalfValue("left",1)
    sleep(1)
    dt.clearHalfValue("right",1)
    sleep(2)
    
    # Repopulating half data set values
    dt.updateHalfValue("74.7","left",0)
    sleep(1)
    dt.updateHalfValue("Auto","right",0)
    sleep(1)
    dt.updateHalfValue("74.0","left",1)
    sleep(1)
    dt.updateHalfValue("On","right",1)
    sleep(2)
    
    # Clearing the value on a full line entry
    dt.clearWholeLineValue(2)
    dt.clearWholeLineValue(3)
    sleep(2)
    
    # Repopulating the values that was just removed
    dt.updateWholeLineValue("Still Hot",2)
    dt.updateWholeLineValue("90%",3)
