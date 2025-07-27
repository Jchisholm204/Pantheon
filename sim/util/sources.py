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
        if isinstance(path, str):
            path = Path(path)
        path = path.rglob(pattern)
        ls = []
        for x in path:
            ls.append(str(x))
        return ls

    @property
    def TYPES() -> []:
        basepath = Sources.get_path("include/types")
        return Sources.get_sourceFiles(basepath)

    ISA = [
        "processor/rv32_isa.svh"
    ]

    @property
    def ALU() -> SourceFiles:
        basepath = Sources.get_path("processor/ALU")
        return Sources.get_sourceFiles(basepath)

    @property
    def MEM() -> SourceFiles:
        basepath = Sources.get_path("processor/memory")
        return Sources.get_sourceFiles(basepath)

    @property
    def INTERFACES():
        basepath = Sources.get_path("include/interfaces")
        return Sources.get_sourceFiles(basepath)

    WISHBONE = [
            "processor/../interfaces/WISHBONE_IF.sv"
    ]

    @property
    def PIPE():
        basepath = Sources.get_path("processor/datapipe")
        return Sources.get_sourceFiles(basepath)

    @property
    def CTRL():
        basepath = Sources.get_path("processor/control")
        return Sources.get_sourceFiles(basepath)

    @property
    def PROC():
        basepath = Sources.get_path("processor")
        sl = Sources.get_sourceFiles(basepath)
        # sl += Sources.ALU
        # sl += Sources.PIPE
        # sl += Sources.INTERFACES
        # sl += Sources.MEM
        # sl += Sources.CTRL
        # sl += Sources.TYPES
        return sl
