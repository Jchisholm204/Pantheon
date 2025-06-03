# Testbench superclass
import os
from cocotb.runner import get_runner
from pathlib import Path


class TB:
    def __init__(self, test_module: str, hdl_toplevel: str, sim="verilator"):
        self.test_module = test_module
        self.hdl_toplevel = hdl_toplevel
        self.sim = os.getenv("SIM", sim)
        self.basepath = Path(__file__).resolve().parent.parent
        self.sources = []
        self.parameters = {}

    def add_source(self, source: str):
        self.sources += [self.basepath / source]

    def add_param(self, key: str, value):
        self.parameters.update({key: value})

    def run_tests(self):
        if self.sim == "icarus":
            build_args = ["-DICARUS_TRACE_ARRAYS", "-DICARUS_FST"]
        else:
            build_args = ["--trace", "-Wno-fatal"]
        runner = get_runner(self.sim)
        print(runner.build(
            verilog_sources=self.sources,
            hdl_toplevel=self.hdl_toplevel,
            clean=False,
            waves=True,
            build_args=build_args,
            always=True,
            parameters=self.parameters
        ))
        print(runner.test(
            hdl_toplevel=self.hdl_toplevel,
            test_module=self.test_module,
            plusargs=["-fst"],
            waves=True,
        ))
