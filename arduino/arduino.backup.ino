
// include the library code:
#include <LiquidCrystal.h>
#include <Wire.h>
#include <Adafruit_MCP23017.h>

Adafruit_MCP23017 mcp;
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

//Config
int buttonsPin = A3;
int scrollTime = 70;
int requestTime = 200;

//Gloabal Variables
boolean btnPressed = false;
boolean radioPlaying = false;
int scrollLast = 0;
int scrollTimer = 0;
String content = "";
String currentStation = "";
String newStation = "";
String currentSong = "";
String newSong = "";
String currentTime = "0000-00-00 00:00";
String newTime = "0000-00-00 00:00";
String source = "Radio";

void setup() {
  lcd.begin(20, 4);
  mcp.begin();
  Serial.begin(9600);
  lcd.setCursor(0,0);
  lcd.print("0000-00-00 00:00");
}

//######################################################################
//######################################################################
void loop() {
  delay(5);
  char character;
  if (Serial.available() > 0) {
    character = Serial.read();
    content.concat(character);
  }
  if (content != "" and Serial.available() == 0) { readSerialData(); }
  
  if (source == "Radio") {
    radio();
  } else if (source == "Aux") {
  } else if (source == "Bluetooth") {
  }
}
//######################################################################
//######################################################################

void radio() {
  if (btnPressed == false) {
    switch (button()) {
      case 5:
        btnPressed = true;
        Serial.println("play 1");
        break;
      case 6:
        btnPressed = true;
        Serial.println("play 2");
        break;
      case 7:
        btnPressed = true;
        Serial.println("play 3");
        break;
      case 1:
        btnPressed = true;
        Serial.println("stop");
        break;
      case 2:
        btnPressed = true;
        Serial.println("shutdown");
        break;
    }
    
  } else if (button() == 0) {
    btnPressed = false;
  }
  
  if (currentSong.length() > 20) {
    scrollRow(currentSong, 2);
  }
}

void scrollRow(String str, int row) {
  if (scrollTimer > scrollTime) {
    str = str + " # " + str;
    lcd.setCursor(0, row);
    int from = scrollLast;
    int to = 0;
    if (from + 20 <= str.length()) {
      to = from + 20;
    } else {
      to = str.length();
    }
    
    lcd.print(str.substring(from, to));
    
    if (scrollLast > str.length() / 2) {
      scrollLast = 0;
    } else {
      scrollLast++;  
    }
    
    scrollTimer = 0;
  } else {
    scrollTimer++;
  }
}

int button() {
  if(mcp.digitalRead(0) == HIGH) { return 1; }
  if(mcp.digitalRead(1) == HIGH) { return 2; }
  if(mcp.digitalRead(2) == HIGH) { return 3; }
  if(mcp.digitalRead(3) == HIGH) { return 4; }
  if(mcp.digitalRead(4) == HIGH) { return 5; }
  if(mcp.digitalRead(5) == HIGH) { return 6; }
  if(mcp.digitalRead(6) == HIGH) { return 7; }
  if(mcp.digitalRead(7) == HIGH) { return 8; }
  return 0;
}

void readSerialData() {
  String id = content.substring(0,2);
  String str = content.substring(2);
  if(id == "00") {
    //message("Raspberry pi running");
    Serial.println("hello");
  };
      
  if ((id == "01") and (str != currentStation)) {
    lcd.setCursor(0,1);
    lcd.print("                    ");
    lcd.setCursor(0,1);
    lcd.print(str.substring(0,20));
    currentStation = str;
  }
  if ((id == "02") and (str != currentSong)) {
    lcd.setCursor(0,2);
    lcd.print("                    ");
    lcd.setCursor(0,2);
    lcd.print(str.substring(0,20));
    scrollLast = 0;
    currentSong = str;
  }
  if ((id == "03") and (str != currentTime)) {
    lcd.setCursor(0,0);
    lcd.print(str);
    currentTime = str;
  }
  content = "";
}
