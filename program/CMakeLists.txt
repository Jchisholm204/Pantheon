cmake_minimum_required(VERSION 3.21)

#set(CMAKE_TRY_COMPILE_TARGET_TYPE "STATIC_LIBRARY")
include(./gcc-riscv-none.cmake)
# set(CMAKE_SYSTEM_NAME Generic)
project(PANTHEON C ASM)

set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_C_EXTENSIONS ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Base directories
set(PROJECT_DIR ${CMAKE_CURRENT_SOURCE_DIR})

# Architecture flags for RV32IM
set(CPU_PARAMETERS
    -march=rv32im
    -mabi=ilp32
)

# Linker script and startup
# set(STARTUP_SCRIPT ${CMAKE_CURRENT_SOURCE_DIR}/vendor/startup_riscv.S)
set(MCU_LINKER_SCRIPT ${CMAKE_CURRENT_SOURCE_DIR}/pantheon.ld)

# Include directories
set(INCLUDE_DIRECTORIES
    ${PROJECT_DIR}/include
)

# Source files
file(GLOB_RECURSE PROJECT_SOURCES
    ${PROJECT_DIR}/src/*.c
    ${PROJECT_DIR}/src/*.s
)


# Create executable
add_executable(${PROJECT_NAME}
    ${PROJECT_SOURCES}
    # ${STARTUP_SCRIPT}
)

# Compile options
target_include_directories(${PROJECT_NAME} PRIVATE ${INCLUDE_DIRECTORIES})
target_compile_options(${PROJECT_NAME} PRIVATE
    ${CPU_PARAMETERS}
    -Wall
    -Wextra
    -Wpedantic
    -fno-common
    -fdata-sections
    -ffunction-sections
    -g
)

# Linker options
target_link_options(${PROJECT_NAME} PRIVATE
    -T${MCU_LINKER_SCRIPT}
    ${CPU_PARAMETERS}
    -Wl,--gc-sections
    -Wl,-Map=firmware.map
    -Wl,--print-memory-usage
    -nostartfiles
    -nostdlib
)

add_custom_command(TARGET ${PROJECT_NAME} POST_BUILD
    COMMAND ${CMAKE_OBJCOPY} -O ihex $<TARGET_FILE:${PROJECT_NAME}> ${PROJECT_NAME}.hex
    COMMENT "Generating HEX file"
)
add_custom_command(
  OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/start.s
  COMMAND ${CMAKE_C_COMPILER} -S ${CPU_PARAMETERS} -ffreestanding -nostartfiles
          ${CMAKE_CURRENT_SOURCE_DIR}/src/start.c -o ${CMAKE_CURRENT_BINARY_DIR}/start.s
  DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/src/start.c
  COMMENT "Generating assembly from start.c"
)

add_custom_target(asm_output ALL DEPENDS ${CMAKE_CURRENT_BINARY_DIR}/start.s)

