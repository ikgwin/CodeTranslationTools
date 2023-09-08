instruction_type = ['NULL','A_INSTRUCTION','C_INSTRUCTION','L_INSTRUCTION']

instruction_dest = ['NULL','M','D','MD','A','AM','AD','AMD']

instruction_jump = ['NULL','JGT','JEQ','JGE','JLT','JNE','JLE','JMP']

instruction_comp = ['NULL',
                    '0','1','-1',
                    'A','M','D',
                    '!A','!M','!D',
                    '-A','-M','-D',
                    'A+1','M+1','D+1',
                    'A-1','M-1','D-1',
                    'D+A','D+M',
                    'D-A','D-M','A-D','M-D',
                    'D&A','D&M',
                    'D|A','D|M']

class SymbolTable:
    def __init__(self):
        # initialises the symbol table with empty dictionary
        self.table = {'SP': 0, 'LCL': 1, 'ARG': 2, 'THIS': 3, 'THAT': 4, 
                      'R0': 0, 'R1': 1, 'R2': 2, 'R3': 3, 'R4': 4, 
                      'R5': 5, 'R6': 6, 'R7': 7, 'R8': 8, 'R9': 9, 
                      'R10': 10, 'R11': 11, 'R12': 12, 'R13': 13, 'R14': 14, 'R15': 15, 
                      'SCREEN': 16384, 'KBD': 24576}
        # initialises next variable address to 16
        self.next_variable_address = 16

    def addSymbol(self, symbol, value):
        # add a symbol and its value to the symbol table
        self.table[symbol] = value
        self.next_variable_address += 1

    def getSymbol(self, symbol):
        # returns value of a symbol in the symbol table or -1 if not found
        return self.table.get(symbol, -1)


class Assembler:

    def __init__(self):
        """
        Assembler constructor
        """

    def buildSymbolTable(self, instructions, symbolTable):
        """
        Assembler first pass; populates symbol table with label locations.

        @param instructions: A list of the assembly language instructions.
        @param symbolTable: The symbol table to populate.
        """
        # initializes the instruction address to 0
        instruction_address = 0
        for instruction in instructions:
            # determine he type of instruction
            instruction_type = self.parseInstructionType(instruction)
            # print("Instruction:", instruction)
            #print("Instruction Type:", instruction_type)
            if instruction_type == 'L_INSTRUCTION':
                # extract label from instruction
                label = self.parseSymbol(instruction)
                # add the label to symbol table if it doesnt exist already
                if symbolTable.getSymbol(label) == -1:
                    symbolTable.addSymbol(label, instruction_address)

                    # print("Label:", label)
                    # print("Instruction Address:", instruction_address)
                    # print("Symbol Table:", symbolTable.table)

            # increment the instruction address for nonlabel and non null instruction
            elif instruction_type != 'NULL':
                instruction_address += 1


    def generateMachineCode(self, instructions, symbolTable):
        """
        Assembler second pass; Translates a set of instructions to machine code.

        @param instructions: A list of the assembly language instructions to be converted to machine code.
        @param symbolTable: The symbol table to reference/update.
        @return: A String containing the generated machine code as strings of 16-bit binary instructions, 1-per-line.
        """
        # initialise empty list to store machine code instructions
        machine_code = []

        for instruction in instructions:
            # determine the type of instruction
            instruction_type = self.parseInstructionType(instruction)
            # print("Instruction:", instruction)
            # print("Instruction Type:", instruction_type)
            if instruction_type == 'A_INSTRUCTION':
                # extract symbol from the instruction
                symbol = self.parseSymbol(instruction)
                # print("A Instruction Symbol:", symbol)

                # if the symbol is not numeric look up or add it to symbol table
                if not symbol.isnumeric():
                    if symbolTable.getSymbol(symbol) == -1:
                        symbolTable.addSymbol(symbol, symbolTable.next_variable_address)
                    symbol = symbolTable.getSymbol(symbol)


                # print("A Instruction Symbol:", symbol)
                # appends the A instruction machine code t list
                machine_code.append('0{:015b}'.format(int(symbol)))
            elif instruction_type == 'C_INSTRUCTION':
                # parses and translates destination,computation, and jump fields of instruction
                dest = self.translateDest(self.parseInstructionDest(instruction))
                comp = self.translateComp(self.parseInstructionComp(instruction))
                jump = self.translateJump(self.parseInstructionJump(instruction))

                # appends the C instruction machine code to list

                # print("C Instruction Dest:", dest)
                # print("C Instruction Comp:", comp)
                # print("C Instruction Jump:", jump)

                machine_code.append('111{}{}{}'.format(comp, dest, jump))
        # returns machine code instructions as a separated string at newline


        return '\n'.join(machine_code).strip()
       

    def parseInstructionType(self, instruction):
        """
        Parses the type of the provided instruction

        @param instruction: The assembly language representation of an instruction.
        @return: The type of the instruction (A_INSTRUCTION, C_INSTRUCTION, L_INSTRUCTION, NULL)
        """
        instruction = instruction.strip() # stripp the whitespaces before processing the instruction


        if instruction.startswith('@'):
            # if start weith @ then its an A instructuion
            return 'A_INSTRUCTION'
        elif '=' in instruction or ';' in instruction:
            # if it has ; then its a C instruction
            return 'C_INSTRUCTION'
        elif instruction.startswith('(') and instruction.endswith(')'):
            # if it has brackets its a label
            return 'L_INSTRUCTION'
        else:
            return 'NULL'
    

    def parseInstructionDest(self, instruction):
        """
        Parses the destination of the provided C-instruction

        @param instruction: The assembly language representation of a C-instruction.
        @return: The destination of the instruction (see instruction_dest) 
        """
        instruction = instruction.strip() # stripp the whitespaces before processing the instruction
        if '=' in instruction:
            return instruction.split('=')[0]
        else:
            return 'NULL'
    

    def parseInstructionJump(self, instruction):
        """
        Parses the jump condition of the provided C-instruction

        @param instruction: The assembly language representation of a C-instruction.
        @return: The jump condition for the instruction (see instruction_jump)
        """
        instruction = instruction.strip() # stripp the whitespaces before processing the instruction
        if ';' in instruction:
            # if theres a ';' in the instruction split it by ';' and take second part (jump part)
            return instruction.split(';')[1]
        else:
            # if there's no ';'return null  (no jmp conditon)
            return 'NULL'
    

    def parseInstructionComp(self, instruction):
        """
        Parses the computation/op-code of the provided C-instruction

        @param instruction: The assembly language representation of a C-instruction.
        @return: The computation/op-code of the instruction (see instruction_comp)
        """
        instruction = instruction.strip() # stripp the whitespaces before processing the instruction
        if '=' in instruction:
            # if theres a '=' in the instruction split it by '=' and take second part (comp part)
            instruction = instruction.split('=')[1]
        if ';' in instruction:
            # if theres a ';' in the instruction split it by ';' and take first part (comp part)
            instruction = instruction.split(';')[0]
        return instruction
    
    def parseSymbol(self, instruction):
        """
        Parses the symbol of the provided A/L-instruction

        @param instruction: The assembly language representation of a A/L-instruction.
        @return: A string containing either a label name (L-instruction), 
                a variable name (A-instruction), or a constant integer value (A-instruction)
        """
        if instruction.startswith('@'):
            # if the instruction is an A instruction return symbol after the @
            return instruction[1:]
        elif instruction.startswith('(') and instruction.endswith(')'):
            # if the instruction is a l instruction (label), return the symbol between the '(' and ')'
            return instruction[1:-1]
        else:
            # for  other case return empty string
            return ''
    

    def translateDest(self, dest):
        """
        Generates the binary bits of the dest part of a C-instruction

        @param dest: The destination of the instruction
        @return: A String containing the 3 binary dest bits that correspond to the given dest value.
        """
        if dest == 'M':
            return '001'
        elif dest == 'D':
            return '010'
        elif dest == 'MD':
            return '011'
        elif dest == 'A':
            return '100'
        elif dest == 'AM':
            return '101'
        elif dest == 'AD':
            return '110'
        elif dest == 'AMD':
            return '111'
        else:
            return '000'
    

    def translateJump(self, jump):
        """
        Generates the binary bits of the jump part of a C-instruction

        @param jump: The jump condition for the instruction
        @return: A String containing the 3 binary jump bits that correspond to the given jump value.
        """
        if jump == 'JGT':
            return '001'
        elif jump == 'JEQ':
            return '010'
        elif jump == 'JGE':
            return '011'
        elif jump == 'JLT':
            return '100'
        elif jump == 'JNE':
            return '101'
        elif jump == 'JLE':
            return '110'
        elif jump == 'JMP':
            return '111'
        else:
            return '000'
    
    
    def translateComp(self, comp):
        """
        Generates the binary bits of the computation/op-code part of a C-instruction

        @param comp: The computation/op-code for the instruction
        @return: A String containing the 7 binary computation/op-code bits that correspond to the given comp value.
        """
        if comp == '0':
            return '0101010'
        elif comp == '1':
            return '0111111'
        elif comp == '-1':
            return '0111010'
        elif comp == 'D':
            return '0001100'
        elif comp == 'A':
            return '0110000'
        elif comp == '!D':
            return '0001101'
        elif comp == '!A':
            return '0110001'
        elif comp == '-D':
            return '0001111'
        elif comp == '-A':
            return '0110011'
        elif comp == 'D+1':
            return '0011111'
        elif comp == 'A+1':
            return '0110111'
        elif comp == 'D-1':
            return '0001110'
        elif comp == 'A-1':
            return '0110010'
        elif comp == 'D+A':
            return '0000010'
        elif comp == 'D-A':
            return '0010011'
        elif comp == 'A-D':
            return '0000111'
        elif comp == 'D&A':
            return '0000000'
        elif comp == 'D|A':
            return '0010101'
        elif comp == 'M':
            return '1110000'
        elif comp == '!M':
            return '1110001'
        elif comp == '-M':
            return '1110011'
        elif comp == 'M+1':
            return '1110111'
        elif comp == 'M-1':
            return '1110010'
        elif comp == 'D+M':
            return '1000010'
        elif comp == 'D-M':
            return '1010011'
        elif comp == 'M-D':
            return '1000111'
        elif comp == 'D&M':
            return '1000000'
        elif comp == 'D|M':
            return '1010101'
        else:
            return '0000000'
    
    
    def translateSymbol(self, symbol, symbolTable):
        """
        Generates the binary bits for an A-instruction, parsing the value, or looking up the symbol name.

        @param symbol: A string containing either a label name, a variable name, or a constant integer value
        @param symbolTable: The symbol table for looking up label/variable names
        @return: A String containing the 15 binary bits that correspond to the given sybmol.
        """
        try:
            # try to convert symbol to an integer (address)
            address = int(symbol)
        except ValueError:
            # if not an integer, check if in the symbol table
            if symbol not in symbolTable:
                # if not add it with the next variable adddress and incremnte next_variable_address
                symbolTable.addSymbol(symbol, symbolTable.next_variable_address)
                symbolTable.next_variable_address += 1
            # get address associated with the symbol
            address = symbolTable.getSymbol(symbol)


        # return  15 bit binary reprsentation of address
        # print(symbol)
        # print(symbolTable)
        # print(address)
        # print(symbolTable.next_variable_address)

        # return address
        return format(address, '015b')
    

# A quick-and-dirty parser when run as a standalone script.
if __name__ == "__main__":
    import sys
    if(len(sys.argv) > 1):
        instructions = []
        # Open file
        with open(sys.argv[1], "r") as a_file:
            # Read line-by-line, skip comments and empty line
            for line in a_file:
                if line[0] != '/' and line[0] != "\n":
                    instructions.append(line.strip())
        assembler = Assembler()
        symbolTable = SymbolTable()
            # print(instructions)
            # print(symbolTable)
        # First pass
        assembler.buildSymbolTable(instructions,symbolTable)
        # Second pass
        code = assembler.generateMachineCode(instructions,symbolTable)
        # Print output
        print(code)
