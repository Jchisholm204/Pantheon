# ARM GCC Toolchain
set(CMAKE_SYSTEM_NAME Generic)
set(CMAKE_SYSTEM_PROCESSOR riscv)

set(TOOLCHAIN_PREFIX riscv64-unknown-elf-)
## CFLAGS
set(CMAKE_CFLAGS
# "-fdata-sections -ffunction-sections -Wl,--gc-sections")
"")

set(CMAKE_C_COMPILER ${TOOLCHAIN_PREFIX}gcc ${CMAKE_CFLAGS} ${CMAKE_LDFLAGS})
set(CMAKE_CXX_COMPILER ${TOOLCHAIN_PREFIX}g++ ${CMAKE_CFLAGS} ${CMAKE_LDFLAGS})
set(CMAKE_ASM_COMPILER ${TOOLCHAIN_PREFIX}as)
set(CMAKE_OBJCOPY ${TOOLCHAIN_PREFIX}objcopy)
set(CMAKE_SIZE ${TOOLCHAIN_PREFIX}size)
set(CMAKE_OBJDUMP ${TOOLCHAIN_PREFIX}objdump)

set(CMAKE_EXECUTABLE_SUFFIX_ASM ".elf")
set(CMAKE_EXECUTABLE_SUFFIX_C ".elf")
set(CMAKE_EXECUTABLE_SUFFIX_CXX ".elf")

set(CMAKE_TRY_COMPILE_TARGET_TYPE STATIC_LIBRARY)
