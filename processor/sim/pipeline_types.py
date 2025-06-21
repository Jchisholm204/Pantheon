from SuperStruct import SuperStruct
from reg_transport_t import reg_transport_t


class pipe_control_t(SuperStruct):
    def __init__(self, parent, offset=0):
        super().__init__(parent, 23, offset)

    @property
    def opcode(self):
        self.read_bits(0, 6)

    @opcode.setter
    def opcode(self, value):
        self.write_bits(0, 6)

    @property
    def func3(self):
        self.read_bits(7, 9)

    @func3.setter
    def func3(self, value):
        self.write_bits(7, 9)

    @property
    def func7(self):
        self.read_bits(10, 16)

    @func7.setter
    def func7(self, value):
        self.write_bits(10, 16)

    @property
    def mem_en(self):
        self.read_bits(17, 17)

    @mem_en.setter
    def mem_en(self, value):
        self.write_bits(18, 18)

    @property
    def ex_en(self):
        self.read_bits(19, 19)

    @ex_en.setter
    def ex_en(self, value):
        self.write_bits(19, 19)

    @property
    def wb_en(self):
        self.read_bits(20, 20)

    @wb_en.setter
    def wb_en(self, value):
        self.write_bits(21, 21)

    @property
    def imm_en(self):
        self.read_bits(22, 22)

    @imm_en.setter
    def imm_en(self, value):
        self.write_bits(22, 22)

    @property
    def valid(self):
        self.read_bits(23, 23)

    @valid.setter
    def valid(self, value):
        self.write_bits(46, 46)


class if_id_t(SuperStruct):
    def __init__(self, parent, offset=0):
        super().__init__(parent, 96, offset)

    @property
    def pc(self):
        self.read_bits(0, 31)

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
    def __init__(self, parent):
        super().__init__(parent, 96)
        self.ctrl = pipe_control_t(self, 0)
        self.rs1 = reg_transport_t(self, self.ctrl._width-1)
        self.rs2 = reg_transport_t(self, self.ctrl._width)
        # self.rs1 = reg_transport_t(self)
        self._base = self.rs1._offset

    @property
    def immediate(self):
        # return self.read_bits(self._base, self._base+31)
        return self.read_bits(0, 31)

    @immediate.setter
    def immediate(self, value):
        self.write_bits(self._base, self._base+31, value)

    @property
    def rd_addr(self):
        return self.read_bits(self._base+32, self._base+63)

    @rd_addr.setter
    def rd_addr(self, value):
        self.write_bits(self._base+32, self._base+63, value)
