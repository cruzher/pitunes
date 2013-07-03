########################################################################
#### OLD!!!!! This change had been rolled into the main plate sciprt ###
########################################################################

#----------------------------------------------------------------
# Author: Chris Crumpacker                               
# Date: May 2013
#
# Heavily modified version of the "message" function from Adafruit's 
# CharLCD code as written for the RaspberryPi LCD Plate. This handles 
# the end of row/line So that it is actually is cut off and does not 
# overflow into the buffer on the 16x2 displays and worse onto 
# line 3 on the 20x4 displays
# 
# All orginal functionality is retained with the addition of handling the
# \n's Cariage returns for all 4 lines on the 20x4
#
# When calling the message function you can add a "mode" variable to the end
# to describe how to handle strings over the length of the display.
#
# MODE:
# 0 or empty = Normal handling as it was from Adafruit
# 1 = Truncates the string right at the display's limit
# 2 = Truncates the string 3 short of the limit and adds an elipse
#
# Future plans will be to both handle proper cariage returns and to 
# cut at the spaces as to not leave partial words.
#
# Orginal was written by Adafruit Industries.  
# Under MIT license.
#
# "This is essentially a complete rewrite, but the calling syntax
# and constants are based on code from lrvick and LiquidCrystal.
# lrvic - https://github.com/lrvick/raspi-hd44780/blob/master/hd44780.py
# LiquidCrystal - https://github.com/arduino/Arduino/blob/master/libraries/LiquidCrystal/LiquidCrystal.cpp"
#----------------------------------------------------------------

from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate

lcd = Adafruit_CharLCDPlate()

class LCD_EoL_Handling(Adafruit_CharLCDPlate):
    
    def __init__(self, cols=20, rows=4):    # Defaulted to 20x4 displays
        self.numrows = rows
        self.numcols = cols                 # Added a var for the column count to act as the line length limit (say that 10x fast)
    
    
    def message(self, text, limitMode = 0):
        """ Send string to LCD. Newline wraps to next line"""
        lines = str(text).split('\n')       # Split at newline(s)
        for i, line in enumerate(lines):    # For each substring...
            if i == 1:                      # If newline(s),
                lcd.write(0xC0)             # set DDRAM address to 2nd line
            elif i == 2:
                lcd.write(0x94)
            elif i >= 3:
                lcd.write(0xD4)
            """Now depending on the limit mode set by the function call this will handle """
            lineLength = len(line)
            limit = self.numcols
            if limitMode == 0: 
                lcd.write(line, True)     
            elif lineLength >= limit and limitMode == 1:
                '''With the limit mode set to 1 the line is truncated 
                at the number of columns available on the display'''
                limitedLine = line[0:self.numcols]
                lcd.write(limitedLine, True)  
            elif lineLength >= limit and limitMode == 2:
                '''With the limit mode set to 2 the line is truncated 
                at the number of columns minus 3 to add in an elipse'''
                limitedLine = line[0:self.numcols-3]+'...'
                lcd.write(limitedLine, True)
            elif lineLength >= limit and limitMode == 3:
                '''Future todo, add in proper line after line cariage return'''
                print lines
            else:
                lcd.write(line, True)
                
#!/usr/bin/python

if __name__ == '__main__':
    from time import sleep

    numcolumns = 20
    numrows = 4
    
    eol = LCD_EoL_Handling(numcolumns, numrows)
    
    lcd.backlight(lcd.ON)
    lcd.begin(numcolumns, numrows)
    
    eol.message("CharLCD\nEnd of Line Handling\nWith Forced\nCarriage Returns")
    sleep(2)
    
    lcd.clear()
    eol.message("Short String")
    sleep(2)
    
    lcd.clear()
    eol.message("Longer string then can't fit in one line",0)
    sleep(2)
    
    lcd.clear()
    eol.message("Longer string then can't fit in one line",1)
    sleep(2)
    
    lcd.clear()
    eol.message("Longer string then can't fit in one line",2)
    sleep(2)
