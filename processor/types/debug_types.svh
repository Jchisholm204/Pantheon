/**
 * @file debug_types.sv
 * @author Jacob Chisholm (https://Jchisholm204.github.io)
 * @brief 
 * @version 0.1
 * @date Created: 2025-07-17
 * @modified Last Modified: 2025-07-17
 *
 * @copyright Copyright (c) 2025
 */

`timescale 1ns/100ps
package debug_types;

localparam logic [31:0] dmstatus_wmask = 32'h00000000;
localparam logic [31:0] dmcontrol_wmask = 32'hFFFFFFFF;
localparam logic [31:0] abstractcs_wmask = 32'h00000800;
localparam logic [31:0] command_wmask = 32'hFFFFFFFF;
localparam logic [31:0] sbcs_wmask = 32'h001F1000;

typedef struct packed {
    logic active;
    logic reset;
    logic clrresethalreq;
    logic setresethaltreq;
    logic clrkeepalive;
    logic setkeepalive;
    logic [9:0] heartselhi;
    logic [9:0] heartsello;
    logic hasel;
    logic ackunavail;
    logic ackhavereset;
    logic heartreset;
    logic resumereq;
    logic haltreq;
} dmcontrol_t;


typedef struct packed {
    logic [6:0] zero7;
    logic resetpending;
    logic stickyunavail;
    logic impebreak;
    logic [1:0] zero2;
    logic allhavereset;
    logic anyhavereset;
    logic allresumeack;
    logic anyresumeack;
    logic allnonexistent;
    logic anynonexistent;
    logic allunavail;
    logic anyunavail;
    logic allrunning;
    logic anyrunning;
    logic allhalted;
    logic anyhalted;
    logic authenticated;
    logic authbusy;
    logic hasresethaltreq;
    logic confstrptrvalid;
    logic [3:0] version;
} dmstatus_t;


typedef struct packed {
    logic [2:0] zero3;
    logic [4:0] progbufsize;
    logic [10:0] zero11;
    logic busy;
    logic relaxedpriv;
    logic [2:0] cmderr;
    logic [3:0] zero4;
    logic [3:0] datacount;
} abstractcs_t;

typedef struct packed {
    logic [7:0] cmdtype;
    logic [23:0] control;
} command_t;

typedef struct packed {
    logic [2:0] version;
    logic [5:0] zero6;
    logic busyerror;
    logic busy;
    logic readonaddr;
    logic [2:0] access;
    logic autoincrement;
    logic readondata;
    logic [2:0] error;
    logic [6:0] size;
    logic access128;
    logic access64;
    logic access32;
    logic access16;
    logic access8;
} sbcs_t;

typedef union packed {
    dmcontrol_t dmcontrol;
    dmstatus_t dmstatus;
    abstractcs_t abstractcs;
    command_t command;
    sbcs_t sbcs;
} debug_type_t;

endpackage

