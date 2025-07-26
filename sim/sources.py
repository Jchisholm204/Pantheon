import os
from pathlib import Path


class SourceFiles(list):
    pass


class Sources:
    def get_basepath():
        basepath = Path(__file__).resolve()
        # Remove the file name
        basepath = basepath.parent
        basestring = str(basepath)
        while not basestring.endswith("sim") and basestring != "/home":
            basepath = basepath.parent
            basestring = str(basepath)
        if basestring == "/home":
            assert "Path Resolution Failure"
        return basepath.parent

    def get_path(folder_name: str) -> Path:
        base = str(Sources.get_basepath())
        base += f"/{folder_name}"
        return Path(base)

    def get_sourceFiles(path: [Path, str], pattern="*") -> list:
        if path is str:
            path = Path(path)
        path = path.rglob(pattern)
        ls = SourceFiles()
        for x in path:
            ls.append(str(x))
        return ls

    def TYPES_SOURCES() -> SourceFiles:
        basepath = Sources.get_path("include/types")
        return Sources.get_sourceFiles(basepath)

    ISA_SOURCES = [
        "processor/rv32_isa.svh"
    ]

    def ALU_SOURCES() -> SourceFiles:
        basepath = Sources.get_path("processor/ALU")
        return Sources.get_sourceFiles(basepath)

    MEM_SOURCES = [
        "processor/memory/DMEM.sv",
        "processor/memory/IMEM.sv",
        "processor/memory/RAMBlock.sv",
        "processor/memory/ROMBlock.sv",
        "processor/memory/Register.sv",
        "processor/memory/RegisterFile.sv"
    ]

    WISHBONE_SOURCES = [
            "processor/../interfaces/WISHBONE_IF.sv"
    ]

    PIPE_SOURCES = [
        "processor/datapipe/IF.sv",
        "processor/datapipe/ID.sv",
        "processor/datapipe/EX.sv",
        "processor/datapipe/ME.sv"
]

    CTRL_SOURCES = [
        "processor/control/BranchOutcome.sv",
        "processor/control/HazardUnit.sv",
        "processor/control/PC.sv",
        "processor/control/decoder.sv",
    ]

    INTERFACE_SOURCES = [
        "processor/../interfaces/WISHBONE_IF.sv",
        "processor/../interfaces/DBG_IF.sv",
        "processor/../interfaces/BBUS_IF.sv"
    ]
