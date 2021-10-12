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

// uint16_t a[7] = { 147 , 165 , 175 , 196 , 221 , 248 , 278 };
// uint16_t a[7] = { 294 , 330 , 350 , 393 , 441 , 495 , 556 };
// uint16_t a[7] = { 294 , 330 , 350 , 393 , 441 , 495 , 556 };

// uint16_t a[7] = { 131 , 147 , 165 , 175 , 196 , 220 , 247 };
// uint16_t a[7] = { 262 , 294 , 330 , 349 , 392 , 440 , 494 };
 uint16_t a[7] = { 524 , 988 , 660 , 698 , 784 , 880 , 988 };

int main() 
{  
	int32_t c = 0x7fff7fff;
	int32_t d = 0x00000000;
    pio_init(); 
    int32_t *samples;
	samples =(int32_t *)data_treating( sine_wave_table , 256 );
    while (true) 
    {	
		set_frequency(a[0]);
		for(int i = 0 ; i < a[0] * 2 ; i ++) 
			audio_out(samples);
			
		set_frequency(a[1]);
		for(int i = 0 ; i < a[1] * 2 ; i ++) 
			audio_out(samples);
			
		set_frequency(a[2]);
		for(int i = 0 ; i < a[2] * 2 ; i ++) 
			audio_out(samples);
			
		set_frequency(a[3]);
		for(int i = 0 ; i < a[3] * 2 ; i ++) 
			audio_out(samples);
			
		set_frequency(a[4]);
		for(int i = 0 ; i < a[4] * 2 ; i ++) 
			audio_out(samples);
			
		set_frequency(a[5]);
		for(int i = 0 ; i < a[5] * 2 ; i ++) 
			audio_out(samples);
			
		set_frequency(a[6]);
		for(int i = 0 ; i < a[6] * 2 ; i ++) 
			audio_out(samples); 
			
	/*	set_frequency(a[0]);
		for(int i = 0 ; i < a[0] * 256 ; i ++) 
		{
			if( i % 2 == 0)
				pio_sm_put_blocking(audio_format.pio, audio_format.sm, c);
			else
				pio_sm_put_blocking(audio_format.pio, audio_format.sm, d);
		}
			
		set_frequency(a[1]);
		for(int i = 0 ; i < a[1] * 256 ; i ++) 
		{
			c = ~c;
			pio_sm_put_blocking(audio_format.pio, audio_format.sm, c);
		}
			
		set_frequency(a[2]);
		for(int i = 0 ; i < a[2] * 256 ; i ++) 
		{
			c = ~c;
			pio_sm_put_blocking(audio_format.pio, audio_format.sm, c);
		}
			
		set_frequency(a[3]);
		for(int i = 0 ; i < a[3] * 256 ; i ++) 
		{
			c = ~c;
			pio_sm_put_blocking(audio_format.pio, audio_format.sm, c);
		}
			
		set_frequency(a[4]);
		for(int i = 0 ; i < a[4] * 256 ; i ++) 
		{
			c = ~c;
			pio_sm_put_blocking(audio_format.pio, audio_format.sm, c);
		}
			
		set_frequency(a[5]);
		for(int i = 0 ; i < a[5] * 256 ; i ++) 
		{
			c = ~c;
			pio_sm_put_blocking(audio_format.pio, audio_format.sm, c);
		}
			
		set_frequency(a[6]);
		for(int i = 0 ; i < a[6] * 256 ; i ++) 
		{
			c = ~c;
			pio_sm_put_blocking(audio_format.pio, audio_format.sm, c);
		}
*/
			
		
    }  
    return 0;
}
