# Generated Cmake Pico project file

cmake_minimum_required(VERSION 3.13)

set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)

# initalize pico_sdk from installed location
# (note this can come from environment, CMake cache etc)
#set(PICO_SDK_PATH "D:/Raspberry/Raspberry_pico/code/pico-sdk")

# Pull in Raspberry Pi Pico SDK (must be before project)
include(pico_sdk_import.cmake)

project(PIO_WS2812 C CXX ASM)

# Initialise the Raspberry Pi Pico SDK
pico_sdk_init()

# Add executable. Default name is the project name, version 0.1
add_executable(PIO_WS2812 PIO_WS2812.c )

# generate the header file into the source tree as it is included in the RP2040 datasheet
pico_generate_pio_header(PIO_WS2812 ${CMAKE_CURRENT_LIST_DIR}/WS2812.pio)

pico_set_program_name(PIO_WS2812 "PIO_WS2812")
pico_set_program_version(PIO_WS2812 "0.1")

pico_enable_stdio_uart(PIO_WS2812 1)
pico_enable_stdio_usb(PIO_WS2812 1)

# Add the standard library to the build
target_link_libraries(PIO_WS2812 pico_stdlib)

# Add any user requested libraries
target_link_libraries(PIO_WS2812
        hardware_pio
        )

pico_add_extra_outputs(PIO_WS2812)

