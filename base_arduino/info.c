//#include <Bounce.h>

#define PIN_INPUT_1 2
#define PIN_INPUT_2 3
#define PIN_INPUT_3 4
#define PIN_INPUT_4 5

#define PIN_LED     6

#define PIN_INPUT_TEST 7  // test tuning mod, on 0

#define redPin      9  // Управление первым клапаном
#define greenPin    10  // Управление вторым клапаном
#define bluePin     11  // Управление вторым клапаном

#define time_to_push_1 500 //время задержки срабатывания кнопки
#define time_to_push_2 400//время задержки срабатывания кнопки

#define time_train 6000   //время движения поезда после срабатывания датчика

#define friqwensy_light 0.6   //скорость мигания желтого (float)
#define RED_MIG 10          //скорость мигания красного


unsigned long times;
unsigned long timesLast;
unsigned long times_led;
unsigned long timesLast_led;

#define time_on 1000 // time while led on
#define time_off 500 // time while led off
bool led_state = true;

int yark= 0;//
float mig=0;// яркость мигания
float lastMig; // предідущее значение для направления мигания
int state = 0;

int last_state = 0;
int local_var = 0;
int yellow_correct = 0;
int res_mig;
int sec_mig;
int last_button1 = 1;
int last_button2 = 1;

void setup() {
  timesLast=times = millis();
  // put your setup code here, to run once:
Serial.begin(9600);
  pinMode(redPin, OUTPUT);
  pinMode(greenPin, OUTPUT);
  pinMode(bluePin, OUTPUT);

  pinMode(PIN_INPUT_1, INPUT_PULLUP);
  digitalWrite(PIN_INPUT_1, HIGH);

  pinMode(PIN_INPUT_2, INPUT_PULLUP);
  digitalWrite(PIN_INPUT_2, HIGH);

  pinMode(PIN_INPUT_TEST, INPUT_PULLUP);
  digitalWrite(PIN_INPUT_TEST, HIGH);

  delay (100);
  int buttonState_1 = digitalRead(PIN_INPUT_1);
  Serial.println("setup:");
  int buttonState_2 = digitalRead(PIN_INPUT_2);
Serial.println(buttonState_1);
Serial.println(buttonState_2);

while (buttonState_1 == 0 or buttonState_2 == 0){
  Serial.println("start error");
  buttonState_1 = digitalRead(PIN_INPUT_1);
  buttonState_2 = digitalRead(PIN_INPUT_2);
  delay(25);

  analogWrite(greenPin, 0);
  if (mig>=lastMig)
 {lastMig=mig;
  mig=mig+10;
 }
 else
 {
  lastMig=mig;
  mig=mig-10;
  }
if (mig>255){
  mig = 255;
  lastMig=mig+1;
}
if (mig<50){
  mig = 50;
  lastMig=mig - 1;
}

if (mig > 180){ //частота мигания красного
  local_var = 255;
  yellow_correct = local_var - 70;
}
else{
  local_var = 0;
  yellow_correct = 0;

}
analogWrite(redPin, local_var);
analogWrite(greenPin, yellow_correct);

};
}

void loop() {
int test_button   = digitalRead(PIN_INPUT_TEST);
int buttonState_1 = digitalRead(PIN_INPUT_1);
int buttonState_2 = digitalRead(PIN_INPUT_2);
int buttonState_3 = digitalRead(PIN_INPUT_3);
int buttonState_4 = digitalRead(PIN_INPUT_4);
if (test_button   == 0 ){
  state = 4;
}
if(buttonState_1==0 and buttonState_2==0){
  state = 3;
}

if (buttonState_1 != last_button1){
  Serial.print("change button1 state :");
  Serial.println(buttonState_1);
  last_button1 = buttonState_1;
}
if (buttonState_2 != last_button2){
  Serial.print("change button2 state :");
  Serial.println(buttonState_2);
  last_button2 = buttonState_2;
}

times = millis();
times_led = millis();
delay (25);

switch(state){
  case 0: //wait mode горит желтый, ждем трамвая
  if (state != last_state){
    last_state =  state;
    Serial.print("State-");
  Serial.println(state);
  }
   if(buttonState_1 == 0){
    if(times - timesLast > time_to_push_1){
    Serial.println("buttonState_1 pressed 1");
    state = 1;
    }}
   else{
    timesLast = times;
   }

  if (mig>=lastMig)
 {lastMig=mig;
  mig=mig+friqwensy_light;
 }
 else
 {
  lastMig=mig;
  mig=mig-friqwensy_light;
  }

  if (mig>180){
    mig = 180;
    lastMig=mig + 1;
  }
if (mig<125){
  mig = 125;
  lastMig=mig - 1;
}
  res_mig = (int) mig;
  analogWrite(redPin, 255); // mig
  analogWrite(greenPin, res_mig); // mig
  break;


  case 1: // 1 датчик видит трамвай

    if (state != last_state){
    last_state =  state;
    Serial.print("State-");
  Serial.println(state);
  }
  if(buttonState_1 == 0){
    timesLast = millis();
   }
  else{
    int t = times-timesLast;
    Serial.println(t);
    if (t>time_train){
      state = 2;
    }
  }

  analogWrite(greenPin, 0);
  if (mig>=lastMig)
 {lastMig=mig;
  mig=mig+RED_MIG;
 }
 else
 {
  lastMig=mig;
  mig=mig-RED_MIG;
  }
if (mig>255){
  mig = 255;
  lastMig=mig+1;
}
if (mig<50){
  mig = 50;
  lastMig=mig - 1;
}

if (mig > 200){ //частота мигания красного
  local_var = 255;
}
else{
  local_var = 0;
}
analogWrite(redPin, local_var);
  break;


  case 2: // трамвай проехал 1 датчик  и на остановке
  analogWrite(redPin, 0);
  analogWrite(greenPin, 255);
  if(buttonState_2 == 0){
    if(times - timesLast > time_to_push_2){
      Serial.println("buttonState_1 pressed 1");
      state = 0;
    }
  }
  else{
    timesLast = times;
  }
  break;

  case 3:// Если оба датчика в режиме сработки горит салатовый
  if(buttonState_1!=0 and buttonState_2!=0){
    state = 0;
  }
  Serial.println(state);
  analogWrite(redPin, 255);
  analogWrite(greenPin, 255);
  break;

  case 4: // режим проверки датчиков. при срабатывании датчиков будет гореть соответствующие цвета.
  if (test_button   != 0 ){state = 0;}

  if(buttonState_1 == 0){analogWrite(redPin, 255);}
  else{analogWrite(redPin, 0);}

  if(buttonState_2 == 0){analogWrite(greenPin, 255); }
  else{analogWrite(greenPin, 0);}

  if(buttonState_3 == 0){analogWrite(redPin, 255);}
  else{analogWrite(redPin, 0);}

  if(buttonState_4 == 0){analogWrite(greenPin, 255); }
  else{analogWrite(greenPin, 0);}

}
  switch(led_state){
    case true:
          analogWrite(PIN_LED, 255);
    if(times_led-timesLast_led > time_on){
      timesLast_led = times_led;
      led_state = false;

    };
    break;
    case false:
      analogWrite(PIN_LED, 0);
      if (times_led-timesLast_led > time_off){
        timesLast_led = times;
        led_state = true;
      }
  }

}