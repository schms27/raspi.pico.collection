# 查找当前目录下的所有源文件
# 并将名称保存到 DIR_audio_data_SRCS 变量
aux_source_directory(. DIR_audio_data_SRCS)
# 生成链接库
add_library(audio_data ${DIR_audio_data_SRCS})
target_link_libraries(audio_data PUBLIC  pico_stdlib hardware_spi hardware_i2c hardware_pwm hardware_adc hardware_pio hardware_dma)