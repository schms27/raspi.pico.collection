/*****************************************************************************
* | File: Readme_EN. TXT
* | the Author:
* | Function: Help with use
* | Info:
* -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -
* | This version: V1.0
* | Date: 2021-04-20
* | Info: provide here USES a Chinese version of the document, for your quick use
******************************************************************************/
This file is to help you use this routine.
Here is a brief description of the use of this project:

1. Basic information:
This routine uses the corresponding module matching PICO for verification;

2. Pin connection:
Audio_data. h Pin connection You can view the audio_data.h in the \lib\audio_data directory, and again here:
PCM5101A     =>   	Pico
DIN		 26
BCK 		 27
LRCK	 	 BCK + 1

3. Basic use:
You need to execute:
    If the directory already exists, you can go directly. If there is no build directory, execute
         mkdir build
     Enter the build directory and type in the terminal:
         cd build
         export PICO_SDK_PATH=../../pico-sdk
     Where ../../pico-sdk is your installed SDK directory
     Execute cmake, automatically generate Makefile file, enter in the terminal:
         cmake ..
     Execute make to generate an executable file, and enter in the terminal:
         make
     Copy the compiled uf2 file to pico

4. Modification of Mode (Selected Reading) :
You can modify the macro definition of audio_data.h in the \lib\audio_data directory
PICO_AUDIO_FREQ 			This is a modification to the sampling frequency
PICO_AUDIO_COUNT		This is a change to the number of output channels
PICO_AUDIO_DATA_PIN 		This is a modification of the output data pin of the I2S protocol
PICO_AUDIO_CLOCK_PIN_BASE 	This is a modification of the output data clock pin of the I2S protocol (as well as the modification of the sampling clock pin of I2S to +1).
PICO_AUDIO_PIO 			This is a modification to the output PIO
PICO_AUDIO_SM 			This is a modification to the output state machine