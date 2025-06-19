# This file must mirror the pipeline_types.sv file
from cocotb.handle import ModifiableObject
from cocotb.binary import BinaryValue


class SuperStruct:
    def __init__(self, parent, width=0, offset=0):
        """ Initialize the SuperStruct
        SuperStruct:
            Structure that manages signal storage for System Verilog Structs

        Args:
            parent: The parent object of the SuperStruct
                (SuperStruct or CocoTB signal)
            width: Total bit width of the struct
            offset: Offset of this struct within the parent struct
        """
        self._parent = parent
        # Write only Shadow copy of the CoCoTB simulation value
        self._recent = BinaryValue(None, width, False)
        self._width = width
        self._offset = offset
        if not isinstance(parent, (ModifiableObject, SuperStruct)):
            raise TypeError("Parent must be CoCoTB Signal or SuperStruct")

    def write(self, value):
        """ Write out the whole struct to the simulation

        Args:
            value (): Struct Values to write out
        """
        if isinstance(self._parent, ModifiableObject):
            self._recent = BinaryValue(value, self._width, False)
            self._parent.value = self._recent
        elif isinstance(self._parent, SuperStruct):
            self._parent.write(value)
        else:
            pass

    def write_bits(self, low, high, value):
        """ Write out the whole struct to the simulation

        Args:
            low: low position
            high: high position
            value: Struct Values to write out
        """
        val = int(self._recent)
        width = high - low + 1
        mask = ((1 << width) - 1) << (low + self._offset)
        val = (val & ~mask) | ((value & (1 << width) - 1)) << (low + self._offset)
        self.write(val)

    def read(self):
        """ Read from write only Shadow copy of CoCoTB

        Returns:
            The last written signal value
        """
        if isinstance(self._parent, ModifiableObject):
            return self._parent.value
        elif isinstance(self._parent, SuperStruct):
            return self._parent.read()
        return None

    def read_bits(self, low, high):
        """ Read from write only Shadow copy of CoCoTB

        Returns:
            The last written signal value
        """
        return self.read()[low + self._offset:high + self._offset]
