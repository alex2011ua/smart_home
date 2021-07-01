   #include <SPI.h>
   #include <nRF24L01.h>                                        
   #include <RF24.h>
   // Создаём объект
   RF24 m24l01(7, 8);                 
   // Массив для отправки данных
const int analogInPin = A0;  // Analog input pin that the potentiometer is attached to
const int buttonPin = 2; // Analog output pin that the LED is attached to

int sensorValue = 0;        // value read from the pot
int buttonState = 0;        // value output to the PWM (analog out)
   byte arr1[4];                                   

   // идентификатор канала

   #define ID 0xF0F0F0F0E2LL

   // стартовый байт отправки

   #define SEND_START 55      

   // стоповый байт отправки

   #define SEND_STOP 56        

   unsigned long millissenddata=0;    


   void setup(){

       Serial.begin(9600);
       m24l01.begin();

       m24l01.setPALevel(RF24_PA_LOW);

       m24l01.setDataRate(RF24_250KBPS);

       m24l01.setChannel(0x55);

       m24l01.openWritingPipe(ID);


       snr.begin();     

   }



   void loop() {
     // read the analog in value:
 

      // отправка данных

      if(millis()-millissenddata>10000) {

         // получение данных с датчика

          sensorValue = analogRead(analogInPin);
          // map it to the range of the analog out:
  
          buttonState = digitalRead(buttonPin);
         arr1[0] = SEND_START;  

         arr1[1] = sensorValue;                            

         arr1[2] = buttonState;                            

         arr1[3] = SEND_STOP;  

         Serial.println("send");

         // отправляем данные

         m24l01.write(&arr1, sizeof(arr1));  

         delay(100);

         millissenddata=millis();

      }

   }
