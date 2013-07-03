#include <Encoder.h>
#include <LiquidCrystal.h>

LiquidCrystal lcd(12, 11, 5, 4, 3, 2);
Encoder knob(7, 8);

//Volume Level (0-255)
long intVolume = 20;

void setup() {
  Serial.begin(9600);
  lcd.begin(20, 4);
  lcd.setCursor(8,3);
  lcd.print("Vol ");
}

void loop() {
  volume();
}

void volume() {
  long newPosition = knob.read();
  if (newPosition > 255) {
    knob.write(255);
    newPosition = 255;
  }calc
  if (newPosition < 0) {
    knob.write(0);
    newPosition = 0;
  }
  
  if (newPosition != intVolume) {
    intVolume = newPosition;
    Serial.println("volume " + String(intVolume));
    
    lcd.setCursor(0,0);
    lcd.print(intVolume);
    
    int dispVolume = intVolume / 31;
    lcd.setCursor(12,3);
    for(int i=1; i<=8; i++) {
      if(i<=dispVolume) {
        lcd.print(char(255));
      } else {
        lcd.print(char(219));
      }
    } 
  }
}
