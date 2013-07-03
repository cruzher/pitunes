
// include the library code:
#include <LiquidCrystal.h>
#include <Wire.h>
#include <Adafruit_MCP23017.h>
#include <Encoder.h>

Adafruit_MCP23017 mcp;
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);
Encoder stationKnob(7, 8);

//Config
int scrollTime = 100;
int requestTime = 200;

//Gloabal Variables
boolean btnPressed = false;
boolean radioPlaying = false;
int scrollLast = 0;
int scrollTimer = 0;
int currentStationId = 1;
int stationExec = 0;
long knobValue = -999;
String content = "";
String currentStation = "";
String newStation = "";
String currentSong = "";
String newSong = "";
String currentTime = "0000-00-00 00:00";
String newTime = "0000-00-00 00:00";

void setup() {
  lcd.begin(20, 4);
  mcp.begin();
  Serial.begin(9600);
  lcd.setCursor(0,0);
  lcd.print("0000-00-00 00:00");
  
  stationKnob.write(currentStationId * 4);
  
  mcp.pinMode(1, OUTPUT); //Raspberry pi
  mcp.pinMode(2, OUTPUT); //AMP
  mcp.pinMode(3, OUTPUT); //Display backlight
  mcp.digitalWrite(1, HIGH);
  mcp.digitalWrite(3, HIGH);
  delay(50000);
  mcp.digitalWrite(2, HIGH);
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
  
  
  if (btnPressed == false) {
    if (mcp.digitalRead(0) == HIGH) {
      btnPressed = true;
      if (radioPlaying == false) {
        Serial.println("play");
        radioPlaying = true;
      } else {
        Serial.println("stop");
        radioPlaying = false;
      }
    }
  } else if (mcp.digitalRead(0) == LOW) {
    btnPressed = false;
  }
  
  // CHANGE STATION
  //radioStation();  
  
  if (currentSong.length() > 20) {
    scrollRow(currentSong, 2);
  }
  
}
//######################################################################
//######################################################################

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
    
    lcd.print("                    ");
    lcd.setCursor(0, row);
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
