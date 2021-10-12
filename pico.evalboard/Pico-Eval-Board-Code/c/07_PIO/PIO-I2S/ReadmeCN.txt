/*****************************************************************************
* | File      	:   Readme_CN.txt
* | Author      :   
* | Function    :   Help with use
* | Info        :
*----------------
* |	This version:   V1.0
* | Date        :   2021-04-20
* | Info        :   在这里提供一个中文版本的使用文档，以便你的快速使用
******************************************************************************/
这个文件是帮助您使用本例程。
在这里简略的描述本工程的使用：

1.基本信息：
本例程使用相对应的模块搭配Pico进行了验证;

2.管脚连接：
管脚连接您可以在\lib\audio_data目录下查看audio_data.h中查看，这里也再重述一次：
PCM5101A    =>    Pico
DIN		26
BCK 		27
LRCK		BCK + 1


3.基本使用：
你需要执行：
    如果目录已经存在，则可以直接进入。 如果没有目录，执行:
         mkdir build
    进入目录，并添加SDK:
         cd build
         export PICO_SDK_PATH=../../pico-sdk
     其中 ../../pico-sdk 是你的SDK的目录。
     执行cmake，自动生成Makefile文件:
         cmake ..
     执行make生成可执行文件，然后在终端中输入：
         make
     编译好的uf2文件复制到pico中即可

4.模式修改（选读）：
您可以在\lib\audio_data目录下对audio_data.h的宏定义进行修改
PICO_AUDIO_FREQ 			这是对采样频率进行修改
PICO_AUDIO_COUNT		这是对输出通道数进行修改
PICO_AUDIO_DATA_PIN		这是对 I2S 协议的输出数据引脚进行修改
PICO_AUDIO_CLOCK_PIN_BASE	这是对 I2S 协议的输出数据时钟引脚进行修改 （同时修改的还有 I2S 的采样时钟引脚 为改引脚 +1）
PICO_AUDIO_PIO 			这是对输出的PIO进行修改
PICO_AUDIO_SM 			这是对输出的状态机进行修改

