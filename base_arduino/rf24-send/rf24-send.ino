#include <SPI.h>                                               // Подключаем библиотеку для работы с шиной SPI.
#include <nRF24L01.h>                                          // Подключаем файл настроек из библиотеки RF24.
#include <RF24.h>                                              // Подключаем библиотеку для работы с nRF24L01+.
RF24     radio(9, 10);                                         // Создаём объект radio для работы с библиотекой RF24, указывая номера выводов модуля (CE, SS).
int      ackData;
int     ack1;
int     arr1[4];
// Объявляем массив для хранения и передачи данных (до 32 байт включительно).
   // стартовый байт отправки
#define SEND_START 55      
   // стоповый байт отправки
#define SEND_STOP 56     

const int analogInPin = A0;  // Analog input pin that the potentiometer is attached to
const int buttonPin = 2; // датчик освещения
const int PIN_RELAY = 6; // rele

int sensorValue = 0;        // value read from the pot
int buttonState = 0;        // value output to the PWM (analog out)
unsigned long millissenddata=0;                                    

void setup(){
  //
    Serial.begin(9600);
    pinMode(PIN_RELAY, OUTPUT); // Объявляем пин реле как выход
    radio.begin           ();                                  // Инициируем работу модуля nRF24L01+.
    radio.setChannel      (27);                                // Указываем канал передачи данных (от 0 до 125), 27 - значит передача данных осуществляется на частоте 2,427 ГГц.
    radio.setDataRate     (RF24_250KBPS);                        // Указываем скорость передачи данных (RF24_250KBPS, RF24_1MBPS, RF24_2MBPS), RF24_1MBPS - 1Мбит/сек.
    radio.setPALevel      (RF24_PA_LOW);                       // Указываем мощность передатчика (RF24_PA_MIN=-18dBm, RF24_PA_LOW=-12dBm, RF24_PA_HIGH=-6dBm, RF24_PA_MAX=0dBm).
    radio.enableAckPayload();
    radio.openWritingPipe (0xAABBCCDD11LL);                 // Открываем 0 трубу с адресом 0xAABBCCDD11, для приема и передачи данных.
    //radio.enableDynamicPayloads();

}                                                              //

                                                               
                                                               
void rele(int status){
  if (status == 1){
    digitalWrite(PIN_RELAY, HIGH); // Отключаем реле - посылаем высокий уровень сигнала
    Serial.println("rele on");
  }
  if (status == 0){
    digitalWrite(PIN_RELAY, LOW); // Включаем реле - посылаем низкий уровень сигнала
    Serial.println("rele off");
   }
}

void loop(){

  if(millis()-millissenddata>5000) {
         Serial.println("read sensor");

         // получение данных с датчика
         sensorValue = analogRead(analogInPin);
          // map it to the range of the analog out:
         buttonState = digitalRead(buttonPin);
         arr1[0] = SEND_START;  
         arr1[1] = sensorValue;                            
         arr1[2] = buttonState;
         arr1[3] = ack1;                            
         arr1[4] = SEND_STOP;  
         Serial.print("send");
         
         Serial.print(arr1[0]);
         Serial.print(" ");
         Serial.print(arr1[1]);
         Serial.print(" ");
         Serial.print(arr1[2]);
         Serial.print(" ");
         Serial.print(arr1[3]);
         Serial.print(" ");
         Serial.print(arr1[4]);
         Serial.println(" ");
         // отправляем данные
 
         
         if( radio.write(&arr1, sizeof(arr1)) ){                // Если указанное количество байт массива myData было доставлено приёмнику, то ...
            //  Данные передатчика были корректно приняты приёмником.  // Тут можно указать код который будет выполняться при получении данных приёмником.
            Serial.println("send OK");
          }
          else{
              Serial.println("send Error");
              // Иначе (если данные не доставлены) ...
              //  Данные передатчика не приняты или дошли с ошибкой CRC. // Тут можно указать код который будет выполняться если приёмника нет или он не получил данные.
          }                                                          //
         Serial.println(ackData);
         if( radio.isAckPayloadAvailable() ){                       // Если в буфере имеются принятые данные из пакета подтверждения приёма, то ...
        Serial.println(" AckPayloadAvailable");
        radio.read(&ackData, sizeof(ackData));                 // Читаем данные из буфера в массив ackData указывая сколько всего байт может поместиться в массив.
          if (ackData == 13){
          rele(0);
          }
          if (ackData == 12){
          rele(1);
          }
          Serial.println(ackData);
         }
         millissenddata=millis();

      }
}

                                                     
