# Generated Cmake Pico project file

cmake_minimum_required(VERSION 3.13)

set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)

# initalize pico_sdk from installed location
# (note this can come from environment, CMake cache etc)
#set(PICO_SDK_PATH "D:/Raspberry/Raspberry_pico/code/pico-sdk")

# Pull in Raspberry Pi Pico SDK (must be before project)
include(pico_sdk_import.cmake)

project(02_PWM C CXX ASM)

# Initialise the Raspberry Pi Pico SDK
pico_sdk_init()

# Add executable. Default name is the project name, version 0.1

add_executable(02_PWM 02_PWM.c )

pico_set_program_name(02_PWM "02_PWM")
pico_set_program_version(02_PWM "0.1")

pico_enable_stdio_uart(02_PWM 1)
pico_enable_stdio_usb(02_PWM 1)

# Add the standard library to the build
target_link_libraries(02_PWM pico_stdlib hardware_pwm)

pico_add_extra_outputs(02_PWM)

