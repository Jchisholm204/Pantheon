
ISA_SOURCES = [
    "rv32_isa.svh"
]

TYPES_SOURCES = [
    "types/reg_transport.svh",
    "types/pipeline_types.svh",
    "types/debug_types.svh"
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
        "../interfaces/WISHBONE_IF.sv"
]

PIPE_SOURCES = [
    "datapipe/IF.sv",
    "datapipe/ID.sv",
    "datapipe/EX.sv",
    "datapipe/ME.sv"
]

CTRL_SOURCES = [
    "control/BranchOutcome.sv",
    "control/HazardUnit.sv",
    "control/PC.sv",
    "control/decoder.sv",
]

INTERFACE_SOURCES = [
    "../interfaces/WISHBONE_IF.sv",
    "../interfaces/DBG_IF.sv"
]
