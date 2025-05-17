# Cocotb + Icarus Verilog
TOPLEVEL_LANG = verilog
VERILOG_SOURCES = $(filter-out %cocotb_iverilog_dump.v, \
                    $(shell find ../ -name '*.v' -o -name '*.sv'))
TOPLEVEL = register_file
MODULE = register_file  # Name of the Python test without .py

WAVES=1  # This tells cocotb to dump VCD automatically
SIM=icarus

IVERILOG_FLAGS += -D ICARUS_TRACE_ARRAYS

include $(shell cocotb-config --makefiles)/Makefile.sim

