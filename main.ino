#include <Wire.h>
// https://github.com/Chris--A/Keypad
#include <Keypad.h>
#include <Servo.h>
#include "pitches.h"

// 設定 4 x 4 鍵盤
const byte numRows = 4;
const byte numCols = 4;
byte rowPins[numRows] = {9, 8, 7, 6};
byte colPins[numCols] = {5, 4, 3, 2};

char keymap[numRows][numCols] = {
  {'1', '2', '3', 'A'},
  {'4', '5', '6', 'B'},
  {'7', '8', '9', 'C'},
  {'*', '0', '#', 'D'}
};
Keypad kpd = Keypad(makeKeymap(keymap), rowPins, colPins, numRows, numCols);

// 建立 SERVO 物件
Servo servoA2;
Servo servoA1;

// 蜂鳴器
int melody[] = {
  NOTE_C4, NOTE_G3, NOTE_G3, NOTE_A3, NOTE_G3, 0, NOTE_B3, NOTE_C4
};
int noteDurations[] = {
  4, 8, 8, 4, 4, 4, 4, 4
};


// 初始設定
void setup() {
  Serial.begin(9600);
  // 按鈕
  pinMode(A3, INPUT);
  // 蜂鳴器
  pinMode(A0, OUTPUT);
  // 馬達
  pinMode(A2, OUTPUT);
  servoA2.attach(A2);
  servoA2.write(0);
  // 馬達好像壞掉
  //  pinMode(A1, OUTPUT);
  //  servoA1.attach(A1);
  //  servoA1.write(90);
}

// 輸入時間的函式
char key;
int r[3];
void setTime() {
  int i = 0;

  while (1) {
    key = kpd.getKey();
    char j;

    if (key != NO_KEY) {
      Serial.println(key);
      r[i] = key - 48;
      i++;
    }
    if (key == 'D') {
      key = 0;
      break;
    }
  }
}

// 重複執行部分
String seconds;
long int secs;
long int j;
long int pos = 0;
void loop() {
  Serial.println(A3);

  // 按下開始按鈕
  if (digitalRead(A3) == 1) {
    setTime();
    // 用串列監視器輸出輸入的時間
    for (int i = 0; i < 3; i++) {
      Serial.print(r[i]);
      Serial.println();
    }
    seconds = String(r[0]) + String(r[1]) + String(r[2]);
    secs = seconds.toInt();
    Serial.print("secs:");
    Serial.print(secs);
    Serial.println();
    // 蜂鳴器
    tone(A0, NOTE_B3, 1000);
    delay(1000);
    for (pos = 0; pos <= 45; pos += 1) {
      servoA2.write(pos);
      delay(15);
    }
    delay(1000);
    for (pos = 90; pos >= 0; pos -= 1) {
      servoA1.write(pos);
      delay(15);
    }
    // 倒數計時
    for (long int j = secs; j >= 0; j --) {
      Serial.println(j);
      // 再按一次按紐終止計時
      if (digitalRead(A3) == 1) {
        break;
      }

      // 時間到
      if (j == 0) {
        // 馬達
        for (pos = 45; pos >= 0; pos -= 1) {
          servoA2.write(pos);
          delay(15);
        }
        delay(1000);
        for (pos = 0; pos <= 90; pos += 1) {
          servoA1.write(pos);
          delay(15);
        }
        // 蜂鳴器
        for (int thisNote = 0; thisNote < 8; thisNote++) {
          int noteDuration = 1000 / noteDurations[thisNote];
          tone(A0, melody[thisNote], noteDuration);
          int pauseBetweenNotes = noteDuration * 1.30;
          delay(pauseBetweenNotes);
          
          noTone(A0);  // 停止播放
        }
      }
      delay(1000);
    }
  }
}
