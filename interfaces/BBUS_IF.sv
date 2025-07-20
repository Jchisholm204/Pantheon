/**
 * @file BBUS_IF.sv
 * @author Jacob Chisholm (https://Jchisholm204.github.io)
 * @brief BBUS - Basic Bus
 * @version 0.1
 * @date Created: 2025-07-19
 * @modified Last Modified: 2025-07-19
 *
 * @copyright Copyright (c) 2025
 */

interface BBUS_IF #(
    parameter int ADDR_WIDTH=32,
    parameter int DATA_WIDTH=32
)( /* No Signals (Clock Optional) */ );

logic read_en, write_en;
logic read_ack, write_ack;
logic [ADDR_WIDTH-1:0] addr;
logic [DATA_WIDTH-1:0] rdata, wdata;

modport master (
    input read_ack, write_ack,
    input rdata,
    output read_en, write_en,
    output addr, wdata
);

modport slave (
    input read_en, write_en,
    input addr, wdata,
    output read_ack, write_ack,
    output rdata
);

endinterface
