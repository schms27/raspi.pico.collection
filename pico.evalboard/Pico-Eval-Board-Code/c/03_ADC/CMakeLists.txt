# Generated Cmake Pico project file

cmake_minimum_required(VERSION 3.13)

set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)

# initalize pico_sdk from installed location
# (note this can come from environment, CMake cache etc)
#set(PICO_SDK_PATH "D:/Raspberry/Raspberry_pico/code/pico-sdk")

# Pull in Raspberry Pi Pico SDK (must be before project)
include(pico_sdk_import.cmake)

project(03_ADC C CXX ASM)

# Initialise the Raspberry Pi Pico SDK
pico_sdk_init()

# Add executable. Default name is the project name, version 0.1

add_executable(03_ADC 03_ADC.c )

pico_set_program_name(03_ADC "03_ADC")
pico_set_program_version(03_ADC "0.1")

pico_enable_stdio_uart(03_ADC 1)
pico_enable_stdio_usb(03_ADC 1)

# Add the standard library to the build
target_link_libraries(03_ADC pico_stdlib hardware_adc)

pico_add_extra_outputs(03_ADC)

