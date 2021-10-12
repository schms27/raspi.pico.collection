#include <stdio.h>
#include "pico/stdlib.h"

const uint LED_PIN = 25;
/******************************************************************************
function:	main
parameter: 
Info: blink LED(GP25)
******************************************************************************/
int main()
{
    stdio_init_all();
    gpio_init(LED_PIN);
    gpio_set_dir(LED_PIN,GPIO_OUT);
    bool value =0;
    while (true)
    {
        gpio_put(LED_PIN,value);
        sleep_ms(500);
        value =!value;
    }  
    return 0;
}
