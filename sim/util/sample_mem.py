from util.hex_creator import HexCreator
from rv32_isa import *


def mem_sample_add(fname="testROM.hex"):
    """
    Sample Add test:
        Loads 5 into r1 using addi
        Computes r2 = r1 + r1

    Args:
        fname (): Test ROM filename to use

    Returns:
        ROM handle from HexCreator
    """
    rom = HexCreator(fname)
    rom.add_Iins(OpAluI, 1, OpF3ADD, 0, 0x5)
    rom.add_Rins(OpAluR, 2, OpF3ADD, 1, 1, OpF7ADD)
    return rom


def mem_sample_alu(fname="testROM.hex"):
    rom = HexCreator(fname)
    rom.add_Rins(OpAluR, 1, OpF3OR, 2, 3, OpF7OR)
    rom.add_Rins(OpAluR, 1, OpF3AND, 12, 13, OpF7AND)
    rom.add_Rins(OpAluR, 1, OpF3SLL, 30, 17, OpF7SLL)
    return rom


def mem_sample_mem(fname="testROM.hex"):
    rom = HexCreator(fname)
    rom.add_Sins(OpStore, OpF3SW, 2, 3, 20)
    rom.add_Iins(OpLoad, 4, OpF3LW, 5, 0x64)
    return rom
