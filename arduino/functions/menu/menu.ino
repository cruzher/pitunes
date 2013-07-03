#include <LiquidCrystal.h>
#include <Wire.h>
#include <Adafruit_MCP23017.h>

Adafruit_MCP23017 mcp;
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

//CONFIG
int buttonsPin = A3;
//CONFIG END

boolean btnPressed = false;

//MENU/////////////////////
boolean menuActive = true;
String menuItems[6] = {"Start Volume", "Fader", "Balance", "Treble", "Bass", "Exit"};
int menuCounter = 0;
int menuTimeout = 2000;
int menuScreenPos = 1;
int menuScreenPosLast = 0;
int menuPos = 0;
int menuPosLast = 99;
int menuItemsIndex = 0;
///////////////////////////

void setup() {
  lcd.begin(20, 4);
  mcp.begin();
}

void loop() {
  if (menuActive == true) {
    menu();
  } else {
    
    if(button() == 5) {
      menuActive = true;
    }
  }
}

void menu() {
  if (menuActive == true) {
    boolean submenuselected = false;
    
    if (btnPressed == false) {
      switch (button()) {
        case 4:  //UP
          if(menuScreenPos>1) menuScreenPos--;
          if(menuPos>0) menuPos--;
          btnPressed = true;
          menuCounter = 0;
          break;
        case 6:  //DOWN
          if(menuScreenPos<3) menuScreenPos++;
          if(menuPos<5) menuPos++;
          btnPressed = true;
          menuCounter = 0;
          break;
        case 5:
          subMenu(menuPos);
          submenuselected = true;
          break;
      }
    } else if (button() == 0) {
      btnPressed = false;
    }
    
    
    if (submenuselected == false) {
      lcd.setCursor(8,0);
      lcd.print("MENU");
      
      if (menuPos != menuPosLast) {
        //Clear menu rows
        lcd.setCursor(2,1);
        lcd.print("                  ");
        lcd.setCursor(2,2);
        lcd.print("                  ");
        lcd.setCursor(2,3);
        lcd.print("                  ");
        
        if ((menuScreenPos == 3) and (menuPos>=3)) {
          menuItemsIndex = menuPos - 2;
        }
        if ((menuScreenPos == 1) and(menuPos<menuItemsIndex)) {
          menuItemsIndex = menuPos;
        }
        
        int i = menuItemsIndex;
        int j = i+2;
        int row = 1;
        for(i;i<=j;i++) {
          lcd.setCursor(2,row);
          lcd.print(menuItems[i]);
          row++;
        }
        menuPosLast = menuPos;
      }
      
      if (menuScreenPos != menuScreenPosLast) {
        lcd.setCursor(0,1);
        lcd.print(" ");
        lcd.setCursor(0,2);
        lcd.print(" ");
        lcd.setCursor(0,3);
        lcd.print(" ");
        lcd.setCursor(0,menuScreenPos);
        lcd.print(">");
        menuScreenPosLast = menuScreenPos;
      }
        
      if (menuCounter >= menuTimeout) {
        closeMenu();
      } else {
        menuCounter++;
      }
    }
  }
}

void subMenu(int menuid) {
  //Start Volume
  if (menuid == 0) {
    lcd.clear();
    lcd.setCursor(3,0);
    lcd.print("Start Volume");
  
  }
  if (menuid == 1) {
  
  }
  if (menuid == 2) {
  
  }
  if (menuid == 3) {
  
  }
  if (menuid == 4) {
  
  }
  if (menuid == 5) {
    closeMenu();
  }
}

void closeMenu() {
  menuActive = false;
  menuCounter = 0;
  menuScreenPosLast = 0;
  menuScreenPos = 1;
  menuPos = 0;
  menuPosLast = 99;
  lcd.clear();
  delay(500);
}

int button() {
  if(mcp.digitalRead(10) == HIGH) { return 1; }
  if(mcp.digitalRead(11) == HIGH) { return 2; }
  if(mcp.digitalRead(12) == HIGH) { return 3; }
  if(mcp.digitalRead(13) == HIGH) { return 4; }
  if(mcp.digitalRead(14) == HIGH) { return 5; }
  if(mcp.digitalRead(15) == HIGH) { return 6; }
  return 0;
}
