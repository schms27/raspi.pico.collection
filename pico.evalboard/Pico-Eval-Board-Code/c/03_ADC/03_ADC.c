#include <stdio.h>
#include "pico/stdlib.h"
#include "hardware/gpio.h"
#include "hardware/adc.h"

const uint LDR_PIN = 26;
const float conversion_factor = 3.3f / (1 << 12);
/******************************************************************************
function:	main
parameter: 
Info: ADC Example,measuring LDR(GP26) and chip temperature
******************************************************************************/
int main()
{
    stdio_init_all();
    printf("ADC Example,measuring LDR(GP26) and chip temperature\n");
    
    adc_init();
    // Make sure GPIO is high-impedance, no pullups etc
    adc_gpio_init(26);
    //Enable the onboard temperature sensor.
    adc_set_temp_sensor_enabled(true);
    while (true)
    {
        // Select ADC input 0 (GPIO26)
        adc_select_input(0); 
        uint adc_ldr_raw = adc_read();
        float adc_ldr_vol = adc_ldr_raw * conversion_factor;
        printf("LDR: \r\nRaw value: 0x%03x, voltage: %f V\r\n", adc_ldr_raw, adc_ldr_vol );
        // Select ADC input 4 (temperature sensor)
        adc_select_input(4); 
        uint adc_temp_raw = adc_read();
        float adc_temp_vol =adc_temp_raw * conversion_factor;
        double temperature = 27.0 - ((double)adc_temp_vol - 0.706)/0.001721;
        printf("Temperature: \r\nRaw value: 0x%03x, voltage: %f temperature:%f C\r\n\r\n", adc_temp_raw , adc_temp_vol ,temperature);
        sleep_ms(1000);
    }
    


    return 0;
}
