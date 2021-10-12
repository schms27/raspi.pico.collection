#include <stdio.h>
#include "pico/stdlib.h"
#include "hardware/pwm.h"
const uint LED_PIN = 25;
/******************************************************************************
function:	main
parameter: 
Info: Fade LED(GP25)
******************************************************************************/
int main()
{
    stdio_init_all();

    // Tell GPIO 25 they are allocated to the PWM
    gpio_set_function(LED_PIN, GPIO_FUNC_PWM);
    // Find out which PWM slice is connected to GPIO 25 (it's slice 4 channel)
    uint slice_num = pwm_gpio_to_slice_num(LED_PIN);
    // Set period of 4 cycles (0 to 3 inclusive)
    pwm_set_wrap(slice_num, 1000);


    bool value =0;
    while (true)
    {
        uint16_t N;
        for(N=0;N<1000;N++)
        {
            // Set channel B output high for N cycle before dropping
            pwm_set_chan_level(slice_num, PWM_CHAN_B, N);
            // Set the PWM running
            pwm_set_enabled(slice_num, true);
            sleep_ms(1);
        }
        for(N=1000;N>0;N--)
        {
            // Set channel B output high for N cycle before dropping
            pwm_set_chan_level(slice_num, PWM_CHAN_B, N);
            // Set the PWM running
            pwm_set_enabled(slice_num, true);
            sleep_ms(1);
        }
    }  
    return 0;
}
