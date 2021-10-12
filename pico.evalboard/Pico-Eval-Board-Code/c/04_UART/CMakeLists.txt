# Generated Cmake Pico project file

cmake_minimum_required(VERSION 3.13)

set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)

# initalize pico_sdk from installed location
# (note this can come from environment, CMake cache etc)
#set(PICO_SDK_PATH "D:/Raspberry/Raspberry_pico/code/pico-sdk")

# Pull in Raspberry Pi Pico SDK (must be before project)
include(pico_sdk_import.cmake)

project(04_UART C CXX ASM)

# Initialise the Raspberry Pi Pico SDK
pico_sdk_init()

# Add executable. Default name is the project name, version 0.1

add_executable(04_UART 04_UART.c )

pico_set_program_name(04_UART "04_UART")
pico_set_program_version(04_UART "0.1")

pico_enable_stdio_uart(04_UART 0)
pico_enable_stdio_usb(04_UART 1)

# Add the standard library to the build
target_link_libraries(04_UART pico_stdlib hardware_uart)

pico_add_extra_outputs(04_UART)

