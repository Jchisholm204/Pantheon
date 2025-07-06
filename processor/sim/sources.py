
ISA_SOURCES = [
    "rv32_isa.sv"
]

TYPES_SOURCES = [
    "types/reg_transport.sv",
    "types/pipeline_types.sv"
]

ALU_SOURCES = [
    "ALU/CLA.sv",
    "ALU/BitWise.sv",
    "ALU/DIV32.sv",
    "ALU/MUL32.sv",
    "ALU/SHIFT.sv",
    "ALU/ALU.sv"
]

MEM_SOURCES = [
    "memory/DMEM.sv",
    "memory/IMEM.sv",
    "memory/RAMBlock.sv",
    "memory/ROMBlock.sv",
    "memory/Register.sv",
    "memory/RegisterFile.sv"
]

WISHBONE_SOURCES = [
        "../wishbone/WISHBONE_IF.sv"
]
