from cocotb.handle import ModifiableObject
from SuperStruct import SuperStruct


class reg_transport_t(SuperStruct):
    def __init__(self, parent, offset=0):
        super().__init__(parent, 37, offset)

    @property
    def value(self):
        return self.read_bits(0, 31)

    @value.setter
    def value(self, value):
        self.write_bits(0, 31, value)

    @property
    def addr(self):
        return self.read_bits(32, 35)

    @addr.setter
    def addr(self, value):
        self.write_bits(32, 36, value)
