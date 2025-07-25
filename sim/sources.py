
ISA_SOURCES = [
    "processor/rv32_isa.svh"
]

TYPES_SOURCES = [
    "processor/types/reg_transport.svh",
    "processor/types/pipeline_types.svh",
    "processor/types/debug_types.svh"
]

ALU_SOURCES = [
    "processor/ALU/CLA.sv",
    "processor/ALU/BitWise.sv",
    "processor/ALU/DIV32.sv",
    "processor/ALU/MUL32.sv",
    "processor/ALU/SHIFT.sv",
    "processor/ALU/ALU.sv"
]

MEM_SOURCES = [
    "processor/memory/DMEM.sv",
    "processor/memory/IMEM.sv",
    "processor/memory/RAMBlock.sv",
    "processor/memory/ROMBlock.sv",
    "processor/memory/Register.sv",
    "processor/memory/RegisterFile.sv"
]

WISHBONE_SOURCES = [
        "processor/../interfaces/WISHBONE_IF.sv"
]

PIPE_SOURCES = [
    "processor/datapipe/IF.sv",
    "processor/datapipe/ID.sv",
    "processor/datapipe/EX.sv",
    "processor/datapipe/ME.sv"
]

CTRL_SOURCES = [
    "processor/control/BranchOutcome.sv",
    "processor/control/HazardUnit.sv",
    "processor/control/PC.sv",
    "processor/control/decoder.sv",
]

INTERFACE_SOURCES = [
    "processor/../interfaces/WISHBONE_IF.sv",
    "processor/../interfaces/DBG_IF.sv",
    "processor/../interfaces/BBUS_IF.sv"
]
