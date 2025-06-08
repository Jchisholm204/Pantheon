
class HexCreator:
    def __init__(self, file_name="hexout.hex"):
        self.instructions = []
        self.fname = file_name
        self.data = []

    def add_Iins(self, opcode, rd, funct3, rs1, imm):
        instruction = 0
        instruction |= (opcode & 0x7F)              # bits 6:0
        instruction |= (rd & 0x1F) << 7             # bits 11:7
        instruction |= (funct3 & 0x7) << 12         # bits 14:12
        instruction |= (rs1 & 0x1F) << 15           # bits 19:15
        instruction |= (imm & 0xFFF) << 20          # bits 31:20
        self.instructions.append(instruction)

    def add_Rins(self, opcode, rd, funct3, rs1, rs2, funct7):
        instruction = 0
        instruction |= (opcode & 0x7F)              # bits 6:0
        instruction |= (rd & 0x1F) << 7             # bits 11:7
        instruction |= (funct3 & 0x7) << 12         # bits 14:12
        instruction |= (rs1 & 0x1F) << 15           # bits 19:15
        instruction |= (rs2 & 0x1F) << 20           # bits 24:20
        instruction |= (funct7 & 0x7F) << 25        # bits 31:25
        self.instructions.append(instruction)

    def add_Sins(self, opcode, funct3, rs1, rs2, imm):
        imm11_5 = (imm >> 5) & 0x7F
        imm4_0 = imm & 0x1F
        instruction = 0
        instruction |= (opcode & 0x7F)              # bits 6:0
        instruction |= (imm4_0) << 7                # bits 11:7
        instruction |= (funct3 & 0x7) << 12         # bits 14:12
        instruction |= (rs1 & 0x1F) << 15           # bits 19:15
        instruction |= (rs2 & 0x1F) << 20           # bits 24:20
        instruction |= (imm11_5) << 25              # bits 31:25
        self.instructions.append(instruction)

    def add_Bins(self, opcode, funct3, rs1, rs2, imm):
        # imm layout: imm[12|10:5|4:1|11]
        imm12   = (imm >> 12) & 0x1
        imm10_5 = (imm >> 5) & 0x3F
        imm4_1  = (imm >> 1) & 0xF
        imm11   = (imm >> 11) & 0x1
        instruction = 0
        instruction |= (opcode & 0x7F)              # bits 6:0
        instruction |= (imm4_1) << 8                # bits 11:8
        instruction |= (imm11) << 7                 # bit 7
        instruction |= (funct3 & 0x7) << 12         # bits 14:12
        instruction |= (rs1 & 0x1F) << 15           # bits 19:15
        instruction |= (rs2 & 0x1F) << 20           # bits 24:20
        instruction |= (imm10_5) << 25              # bits 30:25
        instruction |= (imm12) << 31                # bit 31
        self.instructions.append(instruction)

    def add_Uins(self, opcode, rd, imm):
        instruction = 0
        instruction |= (opcode & 0x7F)              # bits 6:0
        instruction |= (rd & 0x1F) << 7             # bits 11:7
        instruction |= (imm & 0xFFFFF000)           # bits 31:12 (upper 20 bits)
        self.instructions.append(instruction)

    def add_Jins(self, opcode, rd, imm):
        # imm layout: imm[20|10:1|11|19:12]
        imm20 = (imm >> 20) & 0x1
        imm10_1 = (imm >> 1) & 0x3FF
        imm11 = (imm >> 11) & 0x1
        imm19_12 = (imm >> 12) & 0xFF
        instruction = 0
        instruction |= (opcode & 0x7F)              # bits 6:0
        instruction |= (rd & 0x1F) << 7             # bits 11:7
        instruction |= (imm19_12) << 12             # bits 19:12
        instruction |= (imm11) << 20                # bit 20
        instruction |= (imm10_1) << 21              # bits 30:21
        instruction |= (imm20) << 31                # bit 31
        self.instructions.append(instruction)

    def add_data(self, address, data):
        self.data += [(address, data)]

    def get_ins(self):
        return self.instructions

    def get_data(self):
        return self.data

    def get_hex(byt):
        high = (byt & 0xF0) >> 4
        low = byt & 0x0F
        high_char = chr(65 + high - 10) if high >= 10 else chr(48 + high)
        low_char = chr(65 + low - 10) if low >= 10 else chr(48 + low)
        return f'{high_char}{low_char}'

    def export(self, fname=""):
        if fname == "":
            fname = self.fname
        with open(fname, "w") as file:
            file.write("@00000000\n")
            for ins in self.instructions:
                file.write(f'{HexCreator.get_hex(ins)} ')
                file.write(f'{HexCreator.get_hex(ins >> 8)} ')
                file.write(f'{HexCreator.get_hex(ins >> 16)} ')
                file.write(f'{HexCreator.get_hex(ins >> 24)} ')
            file.write("\n")
            for (addr, dat) in self.data:
                file.write(f'@{self.get_hex(addr)}')
                file.write(f'{self.get_hex(addr >> 8)}')
                file.write(f'{self.get_hex(addr >> 16)}')
                file.write(f'{self.get_hex(addr >> 24)}\n')
                file.write(f'{self.get_hex(dat)}')
                file.write(f'{self.get_hex(dat >> 8)}')
                file.write(f'{self.get_hex(dat >> 16)}')
                file.write(f'{self.get_hex(dat >> 24)}\n')
