/**
 * @file DBG_IF.sv
 * @author Jacob Chisholm (https://Jchisholm204.github.io)
 * @brief SV Processor Debug Interface
 * @version 0.1
 * @date Created: 2025-07-15
 * @modified Last Modified: 2025-07-15
 *
 * @copyright Copyright (c) 2025
 */
interface DBG_IF();
    logic enter_debug;
    logic req_halt;
    logic req_resume;
    logic step;

    logic halted;
    logic running;
    logic stalled;

    logic dm_access_valid;
    logic dm_write;
    logic [6:0] dm_addr;
    logic [31:0] dm_wdata;
    logic [31:0] dm_rdata;

    modport processor (
        input enter_debug, req_halt, req_resume, step,
        output halted, running, stalled,
        input dm_write, dm_addr, dm_wdata,
        output dm_rdata, dm_access_valid
    );

    modport debug_module (
        input halted, running, stalled,
        output enter_debug, req_halt, req_resume, step,
        input dm_rdata, dm_access_valid,
        output dm_write, dm_addr, dm_wdata
    );

endinterface

