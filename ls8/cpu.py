"""CPU functionality."""

import sys

HLT =  0b00000001
LDI =  0b10000010
PRN =  0b01000111
MUL =  0b10100010
PUSH = 0b01000101
POP =  0b01000110


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

        self.sp = 7

        self.hash_table = {}
        self.hash_table[HLT] = self.handle_HLT
        self.hash_table[LDI] = self.handle_LDI
        self.hash_table[PRN] = self.handle_PRN
        self.hash_table[MUL] = self.handle_MUL
        self.hash_table[PUSH] = self.handle_PUSH
        self.hash_table[POP] = self.handle_POP



    def load(self, filename):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = []

        try:
            with open(filename) as f:
                for line in f:
                    comment_split = line.split('#')
                    maybe_binary_num = comment_split[0]

                    try:
                        x = int(maybe_binary_num, 2)
                        program.append(x)
                    except:
                        continue

        except FileNotFoundError:
            print('file not found')

        for instruction in program:
            self.ram[address] = instruction
            address += 1
        
 

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == 'MUL':
            self.reg[reg_a] *= self.reg[reg_b]
            self.pc += 3
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

        self.running = True

        while self.running:
            ir = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if ir in self.hash_table:
                self.hash_table[ir](operand_a, operand_b)
            else:
                print(f'invalid instruction {ir}')
                self.pc += 1
                pass


    def handle_HLT(self, args):
        self.running = False

    def handle_LDI(self, *args):
        self.reg[args[0]] = args[1]
        self.pc += 3

    def handle_PRN(self, *args):
        print(self.reg[args[0]])
        self.pc += 2

    def handle_MUL(self, *args):
        self.alu('MUL', args[0], args[1])
        self.pc += 3

    def handle_PUSH(self, *args):
        self.reg[self.sp] -= 1
        self.ram[self.reg[self.sp]] = self.reg[args[0]]
        self.pc += 2

    def handle_POP(self, *args):
        self.reg[args[0]] = self.ram[self.reg[self.sp]]
        self.reg[self.sp] += 1
        self.pc += 2

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, data):
        self.ram[address] = data
