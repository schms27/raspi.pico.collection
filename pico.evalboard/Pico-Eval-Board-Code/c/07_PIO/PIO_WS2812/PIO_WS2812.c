#include <stdio.h>
#include "pico/stdlib.h"
#include "hardware/pio.h"

#include "ws2812.pio.h"

const uint WS2812_PIN = 4;

static inline void put_pixel(uint32_t pixel_grb) {
    pio_sm_put_blocking(pio0, 0, pixel_grb << 8u);
}


int main()
{
    stdio_init_all();
    PIO pio = pio0;
    int sm = 0;
    uint offset = pio_add_program(pio, &ws2812_program);

    ws2812_program_init(pio, sm, offset, WS2812_PIN, 800000, true);   
    uint32_t RGB =0;
    uint8_t R,G,B;
    while(true)
    {
        for(uint8_t cnt =0;cnt<100;cnt++)
        {
            R=cnt;
            B=100-cnt;
            G=0;
            RGB=(R<<8)+(G<<16)+(B<<0);
            put_pixel(RGB);
            sleep_ms(20);
            
        }
        for(uint8_t cnt =0;cnt<100;cnt++)
        {
            G=cnt;
            R=100-cnt;
            B=0;
            RGB=(R<<8)+(G<<16)+(B<<0);
            put_pixel(RGB);
            sleep_ms(20);
        }
        for(uint8_t cnt =0;cnt<100;cnt++)
        {
            B=cnt;
            G=100-cnt;
            R=0;
            RGB=(R<<8)+(G<<16)+(B<<0);
            put_pixel(RGB);
            sleep_ms(20);
        }

    } 
    return 0;
}
