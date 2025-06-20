from hex_creator import HexCreator
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
