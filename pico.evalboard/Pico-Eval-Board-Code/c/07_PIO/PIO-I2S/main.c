/*****************************************************************************
* |	This version:   V1.0
* | Date        :   2021-04-20
* | Info        :   
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documnetation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to  whom the Software is
# furished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS OR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
******************************************************************************/

#include "audio_pio.h"
#include <stdio.h>

int main() 
{  

    pio_init(); 
    int32_t *samples = (int32_t *)data_treating( sine_wave_table , 256 );
	int32_t *samples1 = NULL ;
    while (true) 
    {	
		for(int i = 20 ; i<100 ; i=i+20)
		{
			sleep_ms(1000);
			samples1 = (int32_t *)Volume_32((int16_t *)samples,256,i);
			Happy_birthday_out(samples1);
			free_32(samples1);
		}
    }  
    return 0;
}
