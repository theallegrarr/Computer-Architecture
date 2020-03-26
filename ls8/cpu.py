"""CPU functionality."""

import sys

MUL = 0b10100010
SP = 7
class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.program_counter = 0

        # instruction register records running instructions
        self.instruction_register = [0]*16
        # ram
        self.ram = [0]*256
        # register
        self.reg = dict()
        self.halt = False
        self.reg[SP] = 0xf4

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]
        program = []
        try:
            filename = sys.argv[1]
        except:
            print('Please add an ls8 file path')
        print(filename)
        with open(filename) as f:
            for line in f:
                comment_split = line.split("#")
                # extract our number
                num = comment_split[0].strip() # trim whitespace
                if num == '':
                    continue # ignore blank lines

                # convert our binary string to a number
                x = int(num, 2)
                self.ram_write(address, x)
                address += 1


    def alu(self, op, reg_a, reg_b):
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def operation(self, identifier):
        if identifier == 0b00000001:
            return "HLT"
        elif identifier == 0b10000010:
            return "LDI"
        elif identifier == 0b01000111:
            return "PRN"
        elif identifier == 0b10100000:
            return "ADD"
        elif identifier == 0b10100010:
            return "MUL"
        elif identifier == 0b01000101:
            return "PUSH"
        elif identifier == 0b01000110:
            return "POP"
        return None

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.program_counter,
            #self.fl,
            #self.ie,
            self.ram_read(self.program_counter),
            self.ram_read(self.program_counter + 1),
            self.ram_read(self.program_counter + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

    def HLT(self):
        self.halt = True
    
    def run(self):
        """Run the CPU."""
        inc_size=0;
        while not self.halt:
            instruction = self.ram_read(self.program_counter)
            
            # self.instruction_register[self.program_counter] = instruction
            # get operation name
            operation = self.operation(instruction)
            instruct_a = self.ram_read(self.program_counter + 1)
            instruct_b = self.ram_read(self.program_counter + 2)
            # print(operation)
            
            if operation == 'HLT':
                self.HLT()

            # if operation is LDI
            if operation == 'LDI':
                # get the two arguments, registry and value
                self.reg[instruct_a] = instruct_b
                inc_size = 3

            # if operation is PRN
            if operation == 'PRN':
                reg_index = instruct_a
                num = self.ram_read(reg_index)
                print(num)
                inc_size = 2
            
            if operation == 'ADD':
                self.alu("ADD", instruct_a, instruct_b)
                inc_size = 3

            if operation == 'MUL':
                self.alu("MUL", instruct_a, instruct_b)
                inc_size = 3

            if operation == 'PUSH':
                value = self.reg[instruct_a]
                # PUSH
                self.reg[SP] -= 1
                self.ram_write(value, self.reg[SP])
                inc_size = 2

            if operation == 'POP':
                value = self.ram[self.reg[SP]]
                # POP
                self.reg[instruct_a] = value
                self.reg[SP] += 1
                inc_size = 2

            self.program_counter += inc_size
            
    def ram_write(self, address, value):
        self.ram[address] = value
        return self.ram[address]
    
    def ram_read(self, address):
        return self.ram[address]

    def LDI(self, register, value):
        self.instruction_register[int(register)] = value
        self.program_counter += 1
        return self.instruction_register[int(register)]

    def PRN(self, register):
        print(int(self.instruction_register[int(register)]))
        self.program_counter += 1
        return True