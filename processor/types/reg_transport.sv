/**
 * @file reg_transport.sv
 * @author Jacob Chisholm (https://Jchisholm204.github.io)
 * @brief Register Transport Structure
 * @version 0.1
 * @date Created: 2025-06-14
 * @modified Last Modified: 2025-06-14
 *
 * @copyright Copyright (c) 2025
 */

`timescale 1ns/100ps
import rv32_isa::RegWidth;
import rv32_isa::RegAddrWidth;

package reg_transport;

typedef struct packed {
    logic [RegWidth-1:0] value;
    logic [RegAddrWidth-1:0] addr;
} reg_transport_t;

endpackage
