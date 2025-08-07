--Wall
--timing
--trace-fst
--trace-structs
--x-assign unique
--x-initial unique
-Iinclude
-Iinclude/types
-Iinclude/interfaces
-Iinterfaces
-Isim/include

./processor/Processor.sv
./processor/control/PC.sv
./processor/control/control.sv
./processor/control/decoder.sv
./processor/control/HazardUnit.sv
./processor/control/DebugModule.sv
./processor/control/BranchOutcome.sv
./processor/debug/DCSRs.sv
./processor/debug/DebugModule.sv
