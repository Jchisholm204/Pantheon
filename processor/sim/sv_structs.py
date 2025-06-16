# This file must mirror the pipeline_types.sv file
from cocotb.handle import ModifiableObject
from cocotb.binary import BinaryValue


class if_id_t:
    def __init__(self, signal: ModifiableObject):
        self._signal = signal
        self._recent = BinaryValue(None, 96)

    @property
    def pc(self):
        return self._signal.value[0:31]

    @pc.setter
    async def pc(self, value):
        old = self._recent.integer
        old = old & 0x0000_0000_FFFF_FFFF_FFFF_FFFF
        new = old | (value & 0xFFFF_FFFF)
        self._signal.value

    @property
    def pc4(self):
        return self._signal.value[32:63]

    @pc4.setter
    async def pc4(self, value):
        old = self._signal.value
        old = old & 0xFFFF_FFFF_0000_0000_FFFF_FFFF
        new = old | ((value & 0xFFFF_FFFF) << 32)
        self._signal.value = new

    @property
    def instruction(self):
        return self._signal.value[64:95]

    @instruction.setter
    async def instruction(self, value):
        old = self._signal.value
        old = old & 0xFFFF_FFFF_FFFF_FFFF_0000_0000
        new = old | ((value & 0xFFFF_FFFF) << 64)
        self._signal.value = new


class reg_transport_t:
    def __init__(self, signal: ModifiableObject):
        self._signal = signal
        self._recent = BinaryValue(None, 37)

    def _get(self):
        return self._recent

    def _set(self, value):
        self._recent = BinaryValue(value, 37, False)
        self._signal.value = self._recent

    @property
    def value(self):
        return self._get()[0:31]
        # return self._signal.value[0:31]

    @value.setter
    def value(self, value):
        old = int(self._get())
        old &= ~0xFFFF_FFFF
        new = old | (value & 0xFFFF_FFFF)
        self._set(new)
        # self._signal.value = new

    @property
    def addr(self):
        return self._signal.value[32:35]

    @addr.setter
    def addr(self, value):
        old = int(self._get())
        # old = self._signal.value.integer
        old &= ~(0x1F << 32)
        new = old | ((value & 0x1F) << 32)
        print(value)
        self._set(new)
        # self._signal.value = new


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
