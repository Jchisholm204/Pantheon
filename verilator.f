--Wall
--timing
--trace-fst
--trace-structs
--x-assign unique
--x-initial unique
-Iprocessor
-Iprocessor/types
-Iinterfaces
-Isim/include

./processor/Processor.sv
./processor/control/PC.sv
./processor/control/control.sv
./processor/control/decoder.sv
./processor/control/HazardUnit.sv
./processor/control/DebugModule.sv
./processor/control/BranchOutcome.sv
