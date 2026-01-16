/************************************************************************/
/*  MOD_LCD.C - Biblioteca de manipulação do módulo LCD com o hd44780   */
/*  Bilbioteca extraída do livro PIC programação em C                   */
/*  Autor: Fabio Pereira  | Adaptado por: Cadu Bastos                   */
/*                                                                      */
/************************************************************************/
/*
lcd_cursor_on()                        funções LCD
lcd_cursor_pisca()
lcd_cursor_off()
lcd_corre_esquerda()
lcd_corre_direita()
lcd_envia_nibble( byte dado )
lcd_read_byte()
lcd_ini()
lcd_pos_xy( byte x, byte y)
lcd_escreve( char c)                   \f  Clear display                            ////
                                       \n  Go to start of second line               ////
                                       \b  Move back one position                   ////

*/
// As definições a seguir são utilizadas para acesso aos pinos do display
// caso o pino RW não seja utilizado, comente a definição lcd_rw
#include <stdint.h>
#include <stdbool.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/gpio.h"

#ifndef lcd_16x2_pins
   #define lcd_en GPIO_NUM_22     // pino enable do LCD
   #define lcd_rs GPIO_NUM_21     // pino rs do LCD
   #define lcd_rw GPIO_NUM_11     // pino rw do LCD
   
   #define lcd_d4 GPIO_NUM_23     // pino de dados d4 do LCD
   #define lcd_d5 GPIO_NUM_19     // pino de dados d5 do LCD
   #define lcd_d6 GPIO_NUM_18     // pino de dados d6 do LCD
   #define lcd_d7 GPIO_NUM_5      // pino de dados d7 do LCD
#endif

#define lcd_type 2          // 0=5x7, 1=5x10, 2=2 linhas
#define lcd_seg_lin 0x40    // Endereço da segunda linha na RAM do LCD

// a constante abaixo define a sequência de inicialização do módulo LCD
const uint8_t INIT_LCD[4] = {0x20 | (lcd_type << 2), 0x0C, 1, 6};

/*   O 0x20 eh p configurar o tipo do display e tal.
   O Segundo numero configura o modo do cursor, sendo:
               -> 0x0F Cursor piscante
               -> 0x0E Cursor comum
               -> 0x0C Sem cursor
   O terceiro (1) limpa o display
   O Quarto volta com o cursor.
*/

uint8_t lcd_read_byte(){ // Read a byte from LCD (only with RW pin) 

   uint8_t data;
   // Setup input data pins
   gpio_set_direction(lcd_d4, GPIO_MODE_INPUT);
   gpio_set_direction(lcd_d5, GPIO_MODE_INPUT);
   gpio_set_direction(lcd_d6, GPIO_MODE_INPUT);
   gpio_set_direction(lcd_d7, GPIO_MODE_INPUT);

   // If defined RW pin, set RW pin.
   #ifdef lcd_rw
   gpio_set_level(lcd_rw, 1);
   #endif
   gpio_set_level(lcd_en, 1); // Enable display
   data = 0;   // Reset data 
   // lê os quatro bits mais significativos
   if (gpio_get_level(lcd_d7)) data |= (1 << 7);
   if (gpio_get_level(lcd_d6)) data |= (1 << 6);
   if (gpio_get_level(lcd_d5)) data |= (1 << 5);
   if (gpio_get_level(lcd_d4)) data |= (1 << 4);
   // dá um pulso na linha enable
   gpio_set_level(lcd_en, 0);
   gpio_set_level(lcd_en, 1);
   // lê os quatro bits menos significativos
   if (gpio_get_level(lcd_d7)) data |= (1 << 3);
   if (gpio_get_level(lcd_d6)) data |= (1 << 2);
   if (gpio_get_level(lcd_d5)) data |= (1 << 1);
   if (gpio_get_level(lcd_d4)) data |= (1 << 0);
   gpio_set_level(lcd_en, 0);   // desabilita o display
   // Setup output data pins
   gpio_set_direction(lcd_d4, GPIO_MODE_OUTPUT);
   gpio_set_direction(lcd_d5, GPIO_MODE_OUTPUT);
   gpio_set_direction(lcd_d6, GPIO_MODE_OUTPUT);
   gpio_set_direction(lcd_d7, GPIO_MODE_OUTPUT);
   return data;   // retorna o byte lido
}

void lcd_send_nibble(uint8_t data){ // Send a nibble of data to LCD
    
   uint8_t data_nibble = data & 0x0F; // Extract LSB from data
   // Set output pins to LCD according to data_nibble bit states
   gpio_set_level(lcd_d4, (data_nibble >> 0) & 1);
   gpio_set_level(lcd_d5, (data_nibble >> 1) & 1);
   gpio_set_level(lcd_d6, (data_nibble >> 2) & 1);
   gpio_set_level(lcd_d7, (data_nibble >> 3) & 1);
   // Pulse LCD enable pin
   gpio_set_level(lcd_en, 1);
   gpio_set_level(lcd_en, 0);
}

void lcd_send_byte(bool rs_pin, uint8_t data){ // Send a byte of data to LCD using send_nibble

   // Reset RS pin and wait to busy flag becomes to 0
   // while ( bit_test(lcd_le_byte(),7) ) ;
   // configura a linha rs dependendo do modo selecionado
  
   // delay de 100us !!!!!!
   // caso a linha rw esteja definida, coloca em 0
   #ifdef lcd_rw
   gpio_set_level(lcd_rw, 1);                // RW em leitura para ler busy
   gpio_set_level(lcd_rs, 0);
   while((lcd_read_byte() & 0x80) != 0);     // Wait until DB7 = 0 
   gpio_set_level(lcd_rw, 0);                // RW em escrita
   #endif
   gpio_set_level(lcd_rs, rs_pin);
   gpio_set_level(lcd_en, 0); 
   lcd_send_nibble(data >> 4);               // Send the first part of the byte
   lcd_send_nibble(data & 0x0f);             // Send the second part of the byte
}

void lcd_init(){ // LCD startup
   
   // Reset LCD pins
   gpio_reset_pin(lcd_d4);
   gpio_reset_pin(lcd_d5);
   gpio_reset_pin(lcd_d6);
   gpio_reset_pin(lcd_d7);
   gpio_reset_pin(lcd_rs);
   gpio_reset_pin(lcd_en);
   gpio_reset_pin(lcd_rw);

   // Set LCD pins to output
   gpio_set_direction(lcd_d4, GPIO_MODE_OUTPUT);
   gpio_set_direction(lcd_d5, GPIO_MODE_OUTPUT);
   gpio_set_direction(lcd_d6, GPIO_MODE_OUTPUT);
   gpio_set_direction(lcd_d7, GPIO_MODE_OUTPUT);
   gpio_set_direction(lcd_rs, GPIO_MODE_OUTPUT);
   gpio_set_direction(lcd_en, GPIO_MODE_OUTPUT);
   gpio_set_direction(lcd_rw, GPIO_MODE_OUTPUT);
   
   #ifdef lcd_rw
   gpio_set_level(lcd_rw, 0);
   #endif
   gpio_set_level(lcd_en, 1);
   //vTaskDelay(pdMS_TO_TICKS(15));
   // envia uma sequência de 3 vezes 0x03
   // e depois 0x02 para configurar o módulo
   // para modo de 4 bits
   for(uint8_t cont = 1; cont<=3; cont ++){
      lcd_send_nibble(0x03);
      //vTaskDelay(pdMS_TO_TICKS(5));
   }
   lcd_send_nibble(0x02);
   // Send LCD initialize string
   for(uint8_t cont = 0; cont<=3; cont++)
   lcd_send_byte(0, INIT_LCD[cont]);
}
/*
void lcd_printf(const char *str, ){

}
*/
void lcd_pos_xy(uint8_t x, uint8_t y){
   
   uint8_t addr;
   if(y!=1)
   addr = lcd_seg_lin;
   else{
      addr = 0;
      addr += x-1;
   }
   lcd_send_byte(0,0x80|addr);
}

void lcd_send_string(char *str){ // Send a string to LCD through lcd_send_byte
   
   while(*str){
      switch(*str){
         case '\f':                    // Clear display
            lcd_send_byte(0, 0x01);
            vTaskDelay(pdMS_TO_TICKS(4));
            break;
         case '\n':                    // Set cursor to the second line
            lcd_pos_xy(1, 0);
            break;
            case '\r': 
            lcd_pos_xy(1, 2);
            break;
         case '\b':
            lcd_send_byte(0, 0);       // Set cursor to the first line
            break;
         default:
            lcd_send_byte(1, *str);
            break;
      }
      str++;  
   }
}

void lcd_turn_off()
{
   lcd_send_byte(0, 0x01);
   vTaskDelay(pdMS_TO_TICKS(2));
}

void lcd_cursor_on()
{
   lcd_send_byte(0, 0x0E);
}

void lcd_cursor_off()
{
   lcd_send_byte(0, 0x0C);
}

void lcd_cursor_blink()
{
   lcd_send_byte(0, 0x0F);
}

void lcd_roll_left()
{
   lcd_send_byte(0, 0x18);
}

void lcd_roll_right()
{
   lcd_send_byte(0, 0x1C);
}

