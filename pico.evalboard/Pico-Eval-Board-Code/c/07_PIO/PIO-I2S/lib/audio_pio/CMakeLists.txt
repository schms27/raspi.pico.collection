# 查找当前目录下的所有源文件
# 并将名称保存到 DIR_audio_pio_SRCS 变量
aux_source_directory(. DIR_audio_pio_SRCS)

include_directories(../audio_data)

# 生成链接库
add_library(audio_pio ${DIR_audio_pioSRCS})
target_link_libraries(audio_pio PUBLIC audio_data  pico_stdlib hardware_spi hardware_i2c hardware_pwm hardware_adc hardware_pio hardware_dma)