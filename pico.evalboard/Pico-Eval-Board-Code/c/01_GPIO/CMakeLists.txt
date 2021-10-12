# Generated Cmake Pico project file

cmake_minimum_required(VERSION 3.13)

set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)

# initalize pico_sdk from installed location
# (note this can come from environment, CMake cache etc)
#set(PICO_SDK_PATH "D:/Raspberry/Raspberry_pico/code/pico-sdk")

# Pull in Raspberry Pi Pico SDK (must be before project)
include(pico_sdk_import.cmake)

project(GPIO C CXX ASM)

# Initialise the Raspberry Pi Pico SDK
pico_sdk_init()

# Add executable. Default name is the project name, version 0.1

add_executable(GPIO GPIO.c )

pico_set_program_name(GPIO "GPIO")
pico_set_program_version(GPIO "0.1")

pico_enable_stdio_uart(GPIO 1)
pico_enable_stdio_usb(GPIO 1)

# Add the standard library to the build
target_link_libraries(GPIO pico_stdlib)

pico_add_extra_outputs(GPIO)

