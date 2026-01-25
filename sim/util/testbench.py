# Testbench superclass
import os
from cocotb.runner import get_runner
from pathlib import Path
import shutil
import inspect
from util.sources import Sources, SourceFiles


class TB:
    def __init__(self, test_module: str, hdl_toplevel: str, sim="verilator"):
        self.test_module = test_module
        self.hdl_toplevel = hdl_toplevel
        self.sim = os.getenv("SIM", sim)
        self.basepath = Sources.get_basepath()
        self.sources = []
        self.parameters = {}
        self.defines = {}

    def add_source(self, source: str):
        self.sources += [self.basepath / source]

    def add_sources(self, sources: [list, SourceFiles]):
        # if isinstance(sources, SourceFiles):
        #     for source in sources:
        #         self.sources += [source]
        # else:
        for source in sources:
            self.add_source(source)

    def add_param(self, key: str, value):
        self.parameters.update({key: value})

    def add_define(self, key: str, value):
        self.defines.update({key: value})

    def run_tests(self):
        os.environ["MAKEFLAGS"] = f'-j{os.cpu_count()}'
        if self.sim == "icarus":
            build_args = ["-DICARUS_TRACE_ARRAYS", "-DICARUS_FST"]
        else:
            build_args = ["--trace",
                          "-Wno-fatal",
                          "--trace-structs",
                          "--vpi",
                          # "--output-split", "8",
                          # "--threads", "8 "
                          # "--threads-dpi", "all "
                          "-I../include",
                          "-I../include/types",
                          "-I../include/interfaces"
                          ]
        runner = get_runner(self.sim)
        sim_build = os.path.join(os.getcwd(), "sim_build")
        waveform_path = os.path.join(os.getcwd(), "waveforms")
        if not os.path.exists(waveform_path):
            os.mkdir(waveform_path)
        # sim_build = f"{self.basepath}/build_{self.test_module}"
        print(runner.build(
            verilog_sources=self.sources,
            hdl_toplevel=self.hdl_toplevel,
            clean=True,
            waves=True,
            build_args=build_args,
            always=True,
            parameters=self.parameters,
            defines=self.defines,
            build_dir=sim_build
        ))
        print(runner.test(
            hdl_toplevel=self.hdl_toplevel,
            test_module=self.test_module,
            plusargs=["-fst", "--trace-structs", "--vpi"],
            waves=True,
        ))
        try:
            os.rename(os.path.join(sim_build, "dump.vcd"),
                      os.path.join(waveform_path, f"{self.hdl_toplevel}.vcd"))
            print(
                f"[+] Renamed Waveform dump.vcd -> waveforms/{self.hdl_toplevel}.vcd")
        except FileExistsError:
            print("[!] No dump.vcd file found")
