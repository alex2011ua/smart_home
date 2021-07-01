#include <SPI.h>                                               // Подключаем библиотеку для работы с шиной SPI.
#include <nRF24L01.h>                                          // Подключаем файл настроек из библиотеки RF24.
#include <RF24.h>                                              // Подключаем библиотеку для работы с nRF24L01+.
RF24     radio(7, 10);                                         // Создаём объект radio для работы с библиотекой RF24, указывая номера выводов модуля (CE, SS).
                                                               //
void setup(){                                                  //
    Serial.begin(9600);                                        // Инициируем передачу данных по шине UART в монитор последовательного порта на скорости 9600 бит/сек.
    radio.begin();           Serial.print("Connected "    );   // Инициируем работу модуля nRF24L01+ и выводим текст «Connected ».
    if(radio.isPVariant() ){ Serial.print("nRF24L01"      ); } // Если модуль поддерживается библиотекой RF24, то выводим текст «nRF24L01».
    else                   { Serial.print("unknown module"); } // Иначе, если модуль не поддерживается, то выводи текст «unknown module».
                             Serial.print("\r\n"          );   //
}                                                              //
                                                               //
void loop(){}                                                  //
