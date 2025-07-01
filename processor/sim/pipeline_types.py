from SuperStruct import SuperStruct
from cocotb.handle import ModifiableObject
from reg_transport_t import reg_transport_t


class pipe_control_t(SuperStruct):
    def __init__(self, parent, offset=0):
        super().__init__(parent, 22, offset)

    @property
    def opcode(self):
        return self.read_bits(0, 6)

    @opcode.setter
    def opcode(self, value):
        self.write_bits(0, 6)

    @property
    def func3(self):
        return self.read_bits(7, 9)

    @func3.setter
    def func3(self, value):
        self.write_bits(7, 9, value)

    @property
    def func7(self):
        return self.read_bits(10, 16)

    @func7.setter
    def func7(self, value):
        self.write_bits(10, 16, value)

    @property
    def mem_en(self):
        return self.read_bits(17, 17)

    @mem_en.setter
    def mem_en(self, value):
        self.write_bits(17, 17, value)

    @property
    def ex_en(self):
        return self.read_bits(18, 18)

    @ex_en.setter
    def ex_en(self, value):
        self.write_bits(18, 18, value)

    @property
    def wb_en(self):
        return self.read_bits(19, 19)

    @wb_en.setter
    def wb_en(self, value):
        self.write_bits(19, 19, value)

    @property
    def imm_en(self):
        return self.read_bits(20, 20)

    @imm_en.setter
    def imm_en(self, value):
        self.write_bits(20, 20, value)

    @property
    def valid(self):
        return self.read_bits(21, 21)

    @valid.setter
    def valid(self, value):
        self.write_bits(21, 21, value)


class if_id_t(SuperStruct):
    def __init__(self, parent, offset=0):
        super().__init__(parent, 96, offset)

    @property
    def pc(self):
        return self.read_bits(0, 31)

    @pc.setter
    def pc(self, value):
        self.write_bits(0, 31, value)

    @property
    def pc4(self):
        self.read_bits(32, 63)

    @pc4.setter
    def pc4(self, value):
        self.write_bits(32, 63, value)

    @property
    def instruction(self):
        return self.read_bits(64, 95)

    @instruction.setter
    def instruction(self, value):
        self.write_bits(64, 95, value)


class id_ex_t(SuperStruct):
    def __init__(self, parent, input=False):
        super().__init__(parent, 133)
        if input:
            self.ctrl = pipe_control_t(self, 0)
            self.rs1 = reg_transport_t(self, self.ctrl._width)
            rs2_base = self.ctrl._width + self.rs1._width
            self.rs2 = reg_transport_t(self, rs2_base)
            self._base = rs2_base + self.rs2._width
        else:
            self.ctrl = pipe_control_t(self, 0)
            self.rs1 = reg_transport_t(self, self.ctrl._width)
            rs2_base = self.ctrl._width + self.rs1._width
            self.rs2 = reg_transport_t(self, rs2_base)
            self._base = rs2_base + self.rs2._width

    @property
    def immediate(self):
        return self.read_bits(self._base, self._base+31)
        # return self.read_bits(0, 31)

    @immediate.setter
    def immediate(self, value):
        self.write_bits(self._base, self._base+31, value)

    @property
    def rd_addr(self):
        return self.read_bits(self._base+32, self._base+36)

    @rd_addr.setter
    def rd_addr(self, value):
        self.write_bits(self._base+32, self._base+36, value)


class ex_mem_t(SuperStruct):
    def __init__(self, parent, input=False):
        super().__init__(parent, 133)
        if input:
            self.ctrl = pipe_control_t(self, 0)
            self.rs = reg_transport_t(self, self.ctrl._width)
            rd_base = self.ctrl._width + self.rs._width
            self.rd = reg_transport_t(self, rd_base)
        else:
            self.rd = reg_transport_t(self)
            self.rs = reg_transport_t(self, self.rd._width)
            self.ctrl = pipe_control_t(self, 0)


class mem_wb_t(SuperStruct):
    def __init__(self, parent):
        super().__init__(parent, 96)
        self.ctrl = pipe_control_t(self, 0)
        self.rd = reg_transport_t(self, self.ctrl._width)
