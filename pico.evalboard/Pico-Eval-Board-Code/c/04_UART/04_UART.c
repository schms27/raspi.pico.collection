#include <stdio.h>
#include "hardware/uart.h"
#include "pico/stdlib.h"

#define UART_ID uart0
#define BAUD_RATE 115200

// We are using pins 0 and 1, but see the GPIO function select table in the
// datasheet for information on which other pins can be used.
#define UART_TX_PIN 0
#define UART_RX_PIN 1

const uint LED_PIN = 25;

/******************************************************************************
function:	main
parameter: 
Info: UART Example,
******************************************************************************/

int main()
{
    stdio_init_all();

    gpio_init(LED_PIN);
    gpio_set_dir(LED_PIN,GPIO_OUT);

    // Set up our UART with the required speed.
    uart_init(UART_ID, BAUD_RATE);

    // Set the TX and RX pins by using the function select on the GPIO
    // Set datasheet for more information on function select
    gpio_set_function(UART_TX_PIN, GPIO_FUNC_UART);
    gpio_set_function(UART_RX_PIN, GPIO_FUNC_UART);

    // Send out a string, with CR/LF conversions
    uart_puts(UART_ID, "Waveshare Uart Test!\r\n");
    while(true)
    {
        while(uart_is_readable(UART_ID))
        {
            uint8_t ch = uart_getc(UART_ID);
            if (ch == '0')
            {
                gpio_put(LED_PIN,0);
                uart_puts(UART_ID,"LED OFF\r\n");
            }
            else if (ch == '1')
            {
                gpio_put(LED_PIN,1);
                uart_puts(UART_ID,"LED ON\r\n");
            }
            else
            {
                uart_puts(UART_ID,"Please enter character 0 or 1 to switch the LED on and off\r\n");
            }
        }
    }

    return 0;
}
