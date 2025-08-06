/**
 * @file debug.svh
 * @author Jacob Chisholm (https://Jchisholm204.github.io)
 * @brief 
 * @version 0.1
 * @date Created: 2025-07-17
 * @modified Last Modified: 2025-07-17
 *
 * @copyright Copyright (c) 2025
 */

`timescale 1ns/100ps
package debug;

typedef enum logic [7:0] {
    data0 = 8'h04,
    data1 = 8'h05,
    control = 8'h10,
    status = 8'h11,
    abstractics = 8'h16,
    command = 8'h17,
    progbuf0 = 8'h20,
    progbuf1 = 8'h21,
    sbcs = 8'h38,
    sbaddress = 8'h39,
    sbdata0 = 8'h3c
} dcsr_e;

typedef enum logic [2:0] {
    cerr_none = 3'd0,
    // Debug Unit is busy
    cerr_busy = 3'd1,
    // Command is not supported
    cerr_nosupport = 3'd2,
    // Exception occurred while executing a command
    cerr_exception = 3'd3,
    // The heart was not in the required state to execute the command
    cerr_haltresume = 3'd4,
    // Bus Error (Alignment, Size, Timeout)
    cerr_buserr = 3'd5,
    // Reserved
    cerr_reserved = 3'd6,
    // Command Failed for other reason
    cerr_other = 3'd7
} cmderr_e;

typedef enum logic [7:0] {
    // Command Type: Register Access Command
    ct_reg_access = 8'd0,
    // Command Type: Quick Access Command
    ct_quick_access = 8'd1,
    // Command Type: Memory Access Command
    ct_access_mem = 8'd2
} cmdtype_e;

typedef enum logic [2:0] {
    // Legacy (Before January 1, 2018)
    sbv_legacy = 3'd0,
    // Version 1.0
    sbv_1_0 = 3'd1
} sbversion_e;

typedef enum logic [2:0] {
    // No bus error
    sbe_none = 3'd0,
    // Bus timed out
    sbe_timeout = 3'd1,
    // A bad address was accessed
    sberr_address = 3'd2,
    // There was an alignment error
    sbe_alignment = 3'd3,
    // Access of unsupported size was requested
    sbe_size = 3'd4,
    // Other error
    sbe_other = 3'd7
} sberr_e;

typedef enum logic [2:0] {
    sba_8bit = 3'd0,
    sba_16bit = 3'd1,
    sba_32bit = 3'd2,
    sba_64bit = 3'd3,
    sba_128bit = 3'd4
} sbaccess_e;

typedef enum logic {
    hs_single = 1'b0,
    hs_multiple = 1'b1
} hasel_e;

typedef enum logic [3:0] {
    // Debug Module not present
    dmv_none = 4'd0,
    // Version 0.11 DM Specification
    dmv_0_11 = 4'd1,
    // Version 0.13 DM Specification
    dmv_0_13 = 4'd2,
    // Version 1.0 DM Specification
    dmv_1_00 = 4'd3,
    // Custom DM - Does not conform to any specification
    dmv_custom = 4'd15
} dmversion_e;

typedef struct packed {
    // R/W, reset signal for the debug module
    logic active;
    // R/W, platform reset signal (entire system)
    logic reset;
    // W1, Halt on reset (hasresethaltreq must be 1 if implimented)
    logic clrresethaltreq;
    logic setresethaltreq;
    // W1, Keep heart avaliable for debug module
    logic clrkeepalive;
    logic setkeepalive;
    // WARL, Heart select
    logic [9:0] heartselhi;
    logic [9:0] heartsello;
    // WARL, Allow multiple hearts to be selected at once
    hasel_e hasel;
    // W1, Clear unavail for all selected hearts
    logic ackunavail;
    // W1, Clears havereset for all selected hearts
    logic ackhavereset;
    // WARL, Reset all selected hearts (leave system)
    logic heartreset;
    // W1, resume all selected hearts
    // cannot be written to if haltreq is active
    logic resumereq;
    // WARZ, Halt all selected and running hearts
    logic haltreq;
} dmcontrol_t;


typedef struct packed {
    logic [6:0] zero7;
    // R, NDM (System) Reset is pending
    logic resetpending;
    // R, unavail bits are sticky
    logic stickyunavail;
    // R, Implicit ebreak is present at end of program buffer
    logic impebreak;
    logic [1:0] zero2;
    // R, Hearts have been reset
    logic allhavereset;
    logic anyhavereset;
    // R, Heart has resumed
    logic allresumeack;
    logic anyresumeack;
    // R, Currently selected heart does not exist
    logic allnonexistent;
    logic anynonexistent;
    // R, Hearts unavailable
    logic allunavail;
    logic anyunavail;
    // R, All of the selected hearts are running
    logic allrunning;
    // R, Any of the selected hearts are running
    logic anyrunning;
    // R, All of the hearts are halted
    logic allhalted;
    // R, Any of the selected hearts are halted
    logic anyhalted;
    // R, Authentication Check Passed/Failed
    logic authenticated;
    // R, Authentication module busy
    logic authbusy;
    // R, DM has the ability to halt the heart after reset
    logic hasresethaltreq;
    // R, confstrptr used for configuration?
    logic confstrptrvalid;
    // R, Debug Module Standard Version
    dmversion_e version;
} dmstatus_t;


typedef struct packed {
    logic [2:0] zero3;
    // R, Program Buffer Size (in 32 bit words)
    logic [4:0] progbufsize;
    logic [10:0] zero11;
    // R, Abstract command is executing
    logic busy;
    // WARL, Relaxed permission checks apply
    logic relaxedpriv;
    // RW1C, Command Error
    cmderr_e cmderr;
    logic [3:0] zero4;
    // R, Number of data registers implimented
    logic [3:0] datacount;
} abstractcs_t;

typedef struct packed {
    cmdtype_e cmdtype;
    logic zero1;
    logic [2:0] aarsize;
    logic aarpostincrement;
    logic transfer;
    logic write;
    logic [15:0] regno;
} command_access_reg_t;

typedef struct packed {
    cmdtype_e cmdtype;
    logic [23:0] zero24;
} command_quick_access_t;

typedef struct packed {
    cmdtype_e cmdtype;
    logic aamvirtual;
    logic [2:0] aamsize;
    logic aampostincrement;
    logic [1:0] zero2;
    logic write;
    logic [1:0] target_specific;
    logic [13:0] zero14;
} command_access_mem_t;

typedef union packed {
    command_access_reg_t acc_reg;
    command_quick_access_t qa;
    command_access_mem_t acc_mem;
} command_t;

typedef struct packed {
    // R, System Bus interface specification version
    sbversion_e version;
    logic [5:0] zero6;
    // R/W1C, Debugger attempts to start new operation while one is in progress
    logic busyerror;
    // R, System Bus Manager is busy
    logic busy;
    // RW, Writes to sbaddress0 trigger a system bus read
    logic readonaddr;
    // RW, System Bus Access Size
    sbaccess_e access;
    // RW, sbaddress is auto incremented
    logic autoincrement;
    // RW, Every read from sbdata0 triggers a sbus read
    logic readondata;
    // R/W1C Debug Module System Bus Manager Error
    sberr_e error;
    // R, Width of the system bus in bits
    logic [6:0] size;
    // R, 128 bit accesses are supported
    logic access128;
    // R, 64 bit accesses are supported
    logic access64;
    // R, 32 bit accesses are supported
    logic access32;
    // R, 16 bit accesses are supported
    logic access16;
    // R, 8 bit accesses are supported
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

