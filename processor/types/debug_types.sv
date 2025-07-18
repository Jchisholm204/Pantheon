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

typedef struct packed {
    logic active;
    logic reset;
    logic clrresethalreq;
    logic setresethaltreq;
    logic clrkeepalive;
    logic setkeepalive;
    logic heartselhi;
    logic heartsello;
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
    logic cmderr;
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
    logic access;
    logic autoincrement;
    logic readondata;
    logic error;
    logic size;
    logic access128;
    logic access64;
    logic access32;
    logic access16;
    logic access8;
} sbcs_t;

endpackage

