/* riscv_ram.ld - Linker script for running a program in RAM at 0x00000000 */

ENTRY(_start)

MEMORY
{
    RAM (rwx) : ORIGIN = 0x00000000, LENGTH = 64K
}

SECTIONS
{
    /* Code and read-only data */
    .text : {
        *(.text.entry)     /* Optional: place startup code first */
        *(.text*)          /* Main code */
        *(.rodata*)        /* Read-only data */
        *(.srodata*)       /* Small read-only data */
        KEEP(*(.init))
        KEEP(*(.fini))
    } > RAM

    /* Initialized data */
    .data : {
        *(.data*)
        *(.sdata*)
    } > RAM

    /* Uninitialized data */
    .bss : {
        __bss_start = .;
        *(.bss*)
        *(.sbss*)
        *(COMMON)
        __bss_end = .;
    } > RAM

    /* Stack */
    .stack (NOLOAD) : {
        . = ALIGN(8);
        _stack_top = .;
        . = . + 0x1000; /* 4KB stack */
        _stack_bottom = .;
    } > RAM

    /* Heap (optional, for malloc) */
    .heap (NOLOAD) : {
        _heap_start = .;
        . = . + 0x1000;
        _heap_end = .;
    } > RAM

    PROVIDE(_heap_start = _heap_start);
    PROVIDE(_heap_end = _heap_end);
    PROVIDE(_stack_top = _stack_top);
}

