AS = riscv64-unknown-elf-as
LD = riscv64-unknown-elf-ld
OBJCOPY = riscv64-unknown-elf-objcopy

SRC = test.s
OUT = test
HEX = $(OUT).hex

all: $(HEX)

$(OUT).o: $(SRC)
	$(AS) -o $@ $<

$(OUT).elf: $(OUT).o
	$(LD) -o $@ $< -Ttext=0x0 --entry=_start

$(HEX): $(OUT).elf
	$(OBJCOPY) -O verilog $< $@

clean:
	rm -f $(OUT).o $(OUT).elf $(HEX)

