# Simulation

All simulations are written in Python using CoCoTB.
All verification simulations must follow the format `test_*.py`

## Organization
- `incl`
    - `SuperStruct` base class
    - System Verilog struct definitions (in Python)
- `util`
    - Basic RISC-V assembler - written in Python (`HexCreator`)
    - Number Representation/Manipulation
    - Sources Lists
    - Test Bench runner
- `wrappers`
    - System Verilog wrappers for modules that can not be directly interacted with from Python

## Wrapper Modules
Most simulations use Python wrapper modules to interact with the System Verilog modules.
Additionally, struct wrappers are used to interface with System Verilog structures.
See below for an example:

```python
class Processor():
    def __init__(self, dut):
        self.dut = dut
        self.iClk: ModifiableObject = self.dut.iClk
        self.nRst: ModifiableObject = self.dut.nRst
        self.dbg_nRst: ModifiableObject = self.dut.DBG_nRst
        self.dbg_halt: ModifiableObject = self.dut.DBG_halt
        self.dbg_exec: ModifiableObject = self.dut.DBG_exec
        self.dbg_req_init: ModifiableObject = self.dut.DBG_req_init
        self.dbg_regWrite: ModifiableObject = self.dut.DBG_regWrite
        self.dbg_ins: ModifiableObject = self.dut.DBG_ins
        # Use Struct Wrapper for SV Struct
        self.dbg_rd = reg_transport_t(self.dut.DBG_rd)
        self.dbg_rs = reg_transport_t(self.dut.DBG_rs)
        self.rf: NonHierarchyIndexableObject = self.dut.rf.reg_outs
        self._setup = False

    async def enter_dbg(self):
        if self._setup is False:
            await self.setup()
        self.dbg_req_init.value = 1
        await RisingEdge(self.iClk)
        self.dbg_halt.value = 1
        self.dbg_nRst.value = 0
        await RisingEdge(self.iClk)
        self.dbg_nRst.value = 1

    async def rst(self, enable=True):
        self.nRst.value = 0
        await RisingEdge(self.iClk)
        if enable is True:
            self.nRst.value = 1
            await RisingEdge(self.iClk)
```

## Struct Wrappers
All System Verilog structure wrappers use `SuperStruct` as a base class.
Struct wrappers are used due to CoCoTB/Verilator flattening structures into a single signal.
To unflatten the signal, and support other features, wrappers are placed around `SuperStruct`, which interacts with the CoCoTB signal.

### `SuperStruct`
The `SuperStruct` class was created as an interface to unflatten CoCoTB signals.
It supports interacting directly with CoCoTB signals (`ModifiableObject`) or with other `SuperStruct` instances.
This allows nested structures to be represented in Python.

Note that this is achieved by recursively calling the parent's write function until the parent is of type `ModifiableObject`.
Therefore, if the parent instance passed to a `SuperStruct` is not another `SuperStruct` or a `ModifiableObject`, calls to write will raise a `TypeError`.

### Usage
The `SuperStruct` must be initialized with a parent object, signal width, and internal offset (for nested structures).
Only the `read_bits` and `write_bits` functions should be called. `write` and `read` should not be used directly as they do not function as one might expect.
See below for an example:

```python
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
        return self.read_bits(32, 36)

    @addr.setter
    def addr(self, value):
        self.write_bits(32, 36, value)
```

Using `@property` and `@property.setter` allows the signals to be accessed as shown below:

```python
@cocotb.test
async def sample_test(dut):
    rt = reg_transport_t(dut.reg_transport)
    rt.value = 5
    rt.addr = 12
    await Timer(10, 'ns')
    assert rt.addr = 12, "Addr Fail"
```

The above struct is a python wrapper for the following System Verilog struct.

```systemverilog
typedef struct packed {
    logic [RegWidth-1:0] value;
    logic [RegAddrWidth-1:0] addr;
} reg_transport_t;
```

## Test Bench Runner Module
The Test Bench Runner, or TB, is a wrapper method around CoCoTB that allows for compilation options, runtime options, and base paths to be synced across all simulations/tests.
It can be used to add sources, starting from the Pantheon base directory, set parameters, and add defines.

The `TB` module is initialized by providing the name of the python module and top level System Verilog module used for the test.

```python
def test_sample_runner():
    tb = testbench.TB("test_sample", "Sample")
    # Add Sources
    tb.add_source("sample/Sample.sv")
    # Run the tests
    tb.run_tests()
```

## Sample Instruction Generator
The Sample Instruction Generator, `HexCreator`, is a basic RISC-V assembler written in Python that can generate hex files loadable into a simulation through `$readmemh`.
It can be used as follows:

```python
@cocotb.test
async def mem_test():
    hc = HexCreator()
    hc.addIins(opcode=OpAluI, rd=0x3, func3=OpF3Add, rs1=0x0, imm=0x22)
    hc.add_data(address=0x55, data=0xA7)
    hc.export(fname="simulationROM.hex")
```

