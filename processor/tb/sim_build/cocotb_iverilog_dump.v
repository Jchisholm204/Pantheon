module cocotb_iverilog_dump();
initial begin
    $dumpfile("sim_build/register_file.fst");
    $dumpvars(0, register_file);
    $dumpvars(0, register_file.registers[0]);
end
endmodule
