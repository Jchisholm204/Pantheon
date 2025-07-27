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

    def get_sourceFiles(path: [Path, str], pattern="*") -> SourceFiles:
        if isinstance(path, str):
            path = Path(path)
        path = path.rglob(pattern)
        ls = SourceFiles()
        for x in path:
            ls.append(str(x))
        return ls

    def TYPES() -> SourceFiles:
        basepath = Sources.get_path("include/types")
        return Sources.get_sourceFiles(basepath)

    def ISA() -> list:
        return ["processor/rv32_isa.svh"]

    def ALU() -> SourceFiles:
        basepath = Sources.get_path("processor/ALU")
        return Sources.get_sourceFiles(basepath)

    def MEM() -> SourceFiles:
        basepath = Sources.get_path("processor/memory")
        return Sources.get_sourceFiles(basepath)

    def INTERFACES() -> SourceFiles:
        basepath = Sources.get_path("include/interfaces")
        return Sources.get_sourceFiles(basepath)

    def WISHBONE() -> SourceFiles:
        return ["include/interfaces/WISHBONE_IF.sv"]

    def PIPE() -> SourceFiles:
        basepath = Sources.get_path("processor/datapipe")
        return Sources.get_sourceFiles(basepath)

    def CTRL() -> SourceFiles:
        basepath = Sources.get_path("processor/control")
        return Sources.get_sourceFiles(basepath)

    def PROC() -> SourceFiles:
        basepath = Sources.get_path("processor")
        sl = Sources.get_sourceFiles(basepath, "*.sv")
        sl += Sources.get_sourceFiles(basepath, "*.svh")
        return sl
