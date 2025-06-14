# Cocotb + Icarus Verilog
TOPLEVEL_LANG = verilog
# VERILOG_SOURCES = $(filter-out %cocotb_iverilog_dump.v, \
                    $(shell find ../ -name '*.v' -o -name '*.sv'))
# TOPLEVEL = DIV32
# MODULE = divisor # Name of the Python test without .py

# WAVES=3  # This tells cocotb to dump VCD automatically
SIM=icarus
#
# IVERILOG_FLAGS += -D ICARUS_TRACE_ARRAYS

# VERILOG_SOURCES ?=
# TOPLEVEL ?=
# MODULE ?=

include $(shell cocotb-config --makefiles)/Makefile.sim

