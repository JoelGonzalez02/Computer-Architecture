"""CPU functionality."""

import sys

HLT =  0b00000001
LDI =  0b10000010
PRN =  0b01000111


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""

        # 256 bytes of memory
        self.ram = [0] * 256

        # 8 general-purpose registers + a stack pointer
        self.reg = [0] * 7 + [0xF4]

        #program counter
        self.pc = 0

        self.running = False


    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        self.self.running = True

        while running:
            command_to_execute = program[self.pc]

            if command_to_execute == LDI:
                value_to_save = program[self.pc + 1]
                register_to_save_in = program[self.pc + 2]
                self.reg[register_to_save_in] = value_to_save
                self.pc += 3
            elif command_to_execute == PRN:
                register_to_print = program[self.pc + 1]
                print(f'{self.reg[register_to_print]}')
                self.pc += 2
            elif command_to_execute == HLT:
                self.running = False
            else:
                print(f'Unknown command {command_to_execute')
                sys.exit(1)

                



    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, data):
        self.ram[address] = data
