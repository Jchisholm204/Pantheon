from util.sources import Sources, SourceFiles
import string


def test_sources():
    all_included = SourceFiles()
    # Verify Types
    ts = Sources.TYPES()
    all_included += ts
    try:
        assert isinstance(ts, SourceFiles), \
            "Sources did not return SourceFiles instance"
    except AssertionError:
        assert isinstance(ts, list), \
            "Sources did not return SourceFiles or List instance"
    # Verify ISA
    ts = Sources.ISA()
    all_included += ts
    try:
        assert isinstance(ts, SourceFiles), \
            "Sources did not return SourceFiles instance"
    except AssertionError:
        assert isinstance(ts, list), \
            "Sources did not return SourceFiles or List instance"
    # Verify ALU
    ts = Sources.ALU()
    all_included += ts
    try:
        assert isinstance(ts, SourceFiles), \
            "Sources did not return SourceFiles instance"
    except AssertionError:
        assert isinstance(ts, list), \
            "Sources did not return SourceFiles or List instance"
    # Verify MEM
    ts = Sources.MEM()
    all_included += ts
    try:
        assert isinstance(ts, SourceFiles), \
            "Sources did not return SourceFiles instance"
    except AssertionError:
        assert isinstance(ts, list), \
            "Sources did not return SourceFiles or List instance"
    # Verify Interfaces
    ts = Sources.INTERFACES()
    all_included += ts
    try:
        assert isinstance(ts, SourceFiles), \
            "Sources did not return SourceFiles instance"
    except AssertionError:
        assert isinstance(ts, list), \
            "Sources did not return SourceFiles or List instance"
    # Verify Wishbone
    ts = Sources.WISHBONE()
    all_included += ts
    try:
        assert isinstance(ts, SourceFiles), \
            "Sources did not return SourceFiles instance"
    except AssertionError:
        assert isinstance(ts, list), \
            "Sources did not return SourceFiles or List instance"
    # Verify Pipe
    ts = Sources.PIPE()
    all_included += ts
    try:
        assert isinstance(ts, SourceFiles), \
            "Sources did not return SourceFiles instance"
    except AssertionError:
        assert isinstance(ts, list), \
            "Sources did not return SourceFiles or List instance"
    # Verify Control
    ts = Sources.CTRL()
    all_included += ts
    try:
        assert isinstance(ts, SourceFiles), \
            "Sources did not return SourceFiles instance"
    except AssertionError:
        assert isinstance(ts, list), \
            "Sources did not return SourceFiles or List instance"
    # Verify Processor
    proc_sources = Sources.PROC()
    try:
        assert isinstance(proc_sources, SourceFiles), \
            "Sources did not return SourceFiles instance"
    except AssertionError:
        assert isinstance(proc_sources, list), \
            "Sources did not return SourceFiles or List instance"
    # for psource in proc_sources:
    #     found = False
    #     duplicate = False
    #     for asource in all_included:
    #         if found is False and psource == asource:
    #             found = True
    #         elif found is True and psource == asource:
    #             duplicate = True
    #     assert found is True, f"{asource} not found"
    #     assert duplicate is False, f"{asource} has a duplicate"


if __name__ == "__main__":
    test_sources()
