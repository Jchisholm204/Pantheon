# This file must mirror the pipeline_types.sv file
from cocotb.handle import ModifiableObject
from cocotb.binary import BinaryValue


class SuperStruct:
    def __init__(self, signal: ModifiableObject, width: int):
        """ Initialize the SuperStruct
        SuperStruct:
            Structure that manages signal storage for System Verilog Structs

        Args:
            signal: CoCoTB Signal representing the struct
            width: Total bit width of the struct
        """
        self._signal = signal
        # Write only Shadow copy of the CoCoTB simulation value
        self._recent = BinaryValue(None, width, False)
        self._width = width

    def write(self, value):
        """ Write out the whole struct to the simulation

        Args:
            value (): Struct Values to write out
        """
        self._recent = BinaryValue(value, self._width, False)
        self._signal.value = self._recent

    def read(self):
        """ Read from write only Shadow copy of CoCoTB

        Returns:
            The last written signal value
        """
        return self._recent


class if_id_t(SuperStruct):
    def __init__(self, signal: ModifiableObject):
        super().__init__(signal, 96)

    @property
    def pc(self):
        return self._signal.value[0:31]

    @pc.setter
    async def pc(self, value):
        old = int(self.read())
        old = old & 0x0000_0000_FFFF_FFFF_FFFF_FFFF
        new = old | (value & 0xFFFF_FFFF)
        self.write(new)

    @property
    def pc4(self):
        return self._signal.value[32:63]

    @pc4.setter
    async def pc4(self, value):
        old = int(self.read())
        old = old & 0xFFFF_FFFF_0000_0000_FFFF_FFFF
        new = old | ((value & 0xFFFF_FFFF) << 32)
        self.write(new)

    @property
    def instruction(self):
        return self._signal.value[64:95]

    @instruction.setter
    async def instruction(self, value):
        old = int(self.read())
        old = old & 0xFFFF_FFFF_FFFF_FFFF_0000_0000
        new = old | ((value & 0xFFFF_FFFF) << 64)
        self.write(new)


class reg_transport_t(SuperStruct):
    def __init__(self, signal: ModifiableObject):
        super().__init__(signal, 37)

    @property
    def value(self):
        return self._get()[0:31]
        # return self._signal.value[0:31]

    @value.setter
    def value(self, value):
        old = int(self.read())
        old &= ~0xFFFF_FFFF
        new = old | (value & 0xFFFF_FFFF)
        self.write(new)

    @property
    def addr(self):
        return self._signal.value[32:35]

    @addr.setter
    def addr(self, value):
        old = int(self.read())
        old &= ~(0x1F << 32)
        new = old | ((value & 0x1F) << 32)
        print(value)
        self.write(new)


def gets(val, typ, acc):
    """
    Retrieve a value from within an SV Struct

    Args:
        val (): Struct to Retrieve From
        typ (): Typename of the struct
        acc (): Name of the SV struct parameter

    Returns:
        The value within the struct (not an integer)
    """
    return val.value[typ[acc][0]:typ[acc][1]]
