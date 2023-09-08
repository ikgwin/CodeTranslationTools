"""
VMTranslator Module

Description:
This module translates VM commands into Hack assembly code. The VM language is a stack-based intermediate language that
serves as an intermediate representation between high-level object-based language and the Hack machine language.

The VMTranslator provides the following functionalities:
1. Arithmetic and logical operations: Performs basic arithmetic (add, sub) and logical operations (neg, eq, gt, lt, or).
2. Memory access commands: Manipulate the stack and the memory segments, including push and pop operations across different segments like constant, local, argument, this, that, pointer, temp, and static.
3. Program control commands: Generates code for functions, call, and return commands, allowing for the program's flow to change as per function calls and returns.
4. Branching commands: Generates assembly code to support VM branching commands like label, goto, and if-goto.

In addition to the class, standalone functions provide additional functionality for certain VM commands. If executed as
a standalone script, it reads VM commands from a file and writes the corresponding Hack assembly code to the standard
output.

Usage:
To use the VMTranslator as a standalone script, run it with the path to the VM file as an argument:
$ python VMTranslator.py path_to_vm_file.vm
"""

class VMTranslator:


    def vm_push(segment, offset):
        '''Generate Hack Assembly code for a VM push operation'''
        if segment == 'constant':
            # if the segment constant load the constant value into D
            # then push the value in D register to the stack and increment the stack pointer
            return '@{}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'.format(offset)
        else:
            # if segment is either local, arg , this or that
            if segment in ['local', 'argument', 'this', 'that']:
                # then get corresponding segment ptr 
                segPointer = {'local': 'LCL', 'argument': 'ARG', 'this': 'THIS', 'that': 'THAT'}.get(segment, segment)
                # geberate the assembly code to push the val at the address of (segment pointer + offset) onto stack
                asm_code = '@{}\nD=M\n@{}\nD=D+A\nA=D\nD=M\n'.format(segPointer, offset)

            # if segment is ptr
            elif segment == 'pointer':
                # then determien base address of the ptr segment (either address 3 or 4)
                base_addr = 3 if offset == 0 else 4
                # then generate assembly code to push the val at the base address onto stack
                asm_code = '@{}\nD=M\n'.format(base_addr)
                
            # if the segment is temop
            elif segment == 'temp':
                # determie base address of the temp segment (5 + offset)
                base_addr = 5 + offset
                # genrate assembly code to push value at the base address onto the stack
                asm_code = '@{}\nD=M\n'.format(base_addr)
            elif segment == 'static':
                # if the segment is static
                asm_code = '@static.{}\nD=M\n'.format(offset)
                
            # common code for all segments to push D register to the stack and increment the stack pointer
            asm_code += '@SP\nA=M\nM=D\n@SP\nM=M+1\n'
            return asm_code 

    def vm_pop(segment, offset):
        '''Generate Hack Assembly code for a VM pop operation'''
        if segment in ['local', 'argument', 'this', 'that']:
            # get base address for local arg, this, & that segs
            segPointer = {'local': 'LCL', 'argument': 'ARG', 'this': 'THIS', 'that': 'THAT'}.get(segment, segment)

            # load base address into D, add offset to get actual address, store actual address in R13
            # n then pop the top val; from stack into D & finally store it in the actual address
            asm_code = '@{}\nD=M\n@{}\nD=D+A\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n'.format(segPointer, offset)

        elif segment == 'pointer':
            # for ptr seg base address is either 3 (for this) or 4 (fort hat)
            base_addr = 3 if offset == 0 else 4
            # pop top val from the stack into D, then store it in the correct base address
            asm_code = '@SP\nAM=M-1\nD=M\n@{}\nM=D\n'.format(base_addr)

        elif segment == 'temp':
            # for temp seg, base address is 5 + offset
            base_addr = 5 + offset
            # pop the top val from stack into D, then store it in the correct base address
            asm_code = '@SP\nAM=M-1\nD=M\n@{}\nM=D\n'.format(base_addr)

        elif segment == 'static':
            # for static saeg, each variable is given a unique label prefixed with "static."
            # pop top val from the stack into D, then store it in the unique static variable address
            asm_code = '@SP\nAM=M-1\nD=M\n@static.{}\nM=D\n'.format(offset)

        # return the generated assembly code
        return asm_code

    def vm_add():
        '''Generate Hack Assembly code for a VM add operation'''
        # decerement stack pointer & load topmost val from the stack into D
        # go to the next topmost value in the stack and add the value in D to it
        return '@SP\nAM=M-1\nD=M\nA=A-1\nM=D+M\n'

    def vm_sub():
        '''Generate Hack Assembly code for a VM sub operation'''


        # decerement stack pointer & load topmost val from the stack into D
        # go to the next topmost value in the stack and subtract the value in D to it

        return '@SP\nAM=M-1\nD=M\nA=A-1\nM=M-D\n'

    def vm_neg():
        '''Generate Hack Assembly code for a VM neg operation'''
        # decerement stack pointer & load topmost val from the stack into D

        return '@SP\nA=M-1\nM=-M\n'

    def vm_eq():
        '''Generate Hack Assembly code for a VM eq operation'''
        return ""
    

def vm_eq():
    '''Generate Hack Assembly code for a VM eq operation'''
    label1 = "EQ_TRUE_{}".format(id(vm_eq))
    label2 = "EQ_END_{}".format(id(vm_eq))
    return ('@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\n@{}\nD;JEQ\n'
            '@SP\nA=M-1\nM=0\n@{}\n0;JMP\n'
            '({})\n@SP\nA=M-1\nM=-1\n'
            '({})\n').format(label1, label2, label1, label2)

def vm_gt():
    '''Generate Hack Assembly code for a VM gt operation'''
    label1 = "GT_TRUE_{}".format(id(vm_gt))
    label2 = "GT_END_{}".format(id(vm_gt))
    return ('@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\n@{}\nD;JGT\n'
            '@SP\nA=M-1\nM=0\n@{}\n0;JMP\n'
            '({})\n@SP\nA=M-1\nM=-1\n'
            '({})\n').format(label1, label2, label1, label2)

def vm_lt():
    '''Generate Hack Assembly code for a VM lt operation'''
    label1 = "LT_TRUE_{}".format(id(vm_lt))
    label2 = "LT_END_{}".format(id(vm_lt))
    return ('@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\n@{}\nD;JLT\n'
            '@SP\nA=M-1\nM=0\n@{}\n0;JMP\n'
            '({})\n@SP\nA=M-1\nM=-1\n'
            '({})\n').format(label1, label2, label1, label2)

def vm_or():
    '''Generate Hack Assembly code for a VM or operation'''
    return '@SP\nAM=M-1\nD=M\n@SP\nAM=M-1\nM=M|D\n@SP\nM=M+1\n'

def vm_function(function_name, n_vars):
    '''Generate Hack Assembly code for a VM function operation'''
    init_vars = ['@SP\nA=M\nM=0\n@SP\nM=M+1\n' for _ in range(n_vars)]
    return '({})\n{}'.format(function_name, ''.join(init_vars))

def vm_call(function_name, n_args):
    '''Generate Hack Assembly code for a VM call operation'''
    # This is a simplistic representation. A full vm_call would need to:
    # 1. Push return address.
    # 2. Push LCL, ARG, THIS, THAT.
    # 3. ARG = SP-n-5, LCL = SP.
    # 4. Transfer control to the called function.
    return '@{}\n0;JMP\n'.format(function_name)

def vm_return():
    '''Generate Hack Assembly code for a VM return operation'''
    # This is a simplistic representation. A full vm_return would need to:
    # 1. FRAME = LCL.
    # 2. RET = *(FRAME-5).
    # 3. *ARG = pop().
    # 4. SP = ARG+1.
    # 5. THAT = *(FRAME-1), etc. for THIS, ARG, LCL.
    # 6. goto RET.
    return '@LCL\nD=M\n@R13\nM=D\nD=D-1\nA=D\nD=M\n@R14\nM=D\n@SP\nAM=M-1\n@ARG\nA=M\nM=D\nD=A+1\n@SP\nM=D\n@R13\nAM=M-1\nD=M\n@THAT\nM=D\n@R13\nAM=M-1\nD=M\n@THIS\nM=D\n@R13\nAM=M-1\nD=M\n@ARG\nM=D\n@R13\nAM=M-1\nD=M\n@LCL\nM=D\n@R14\nA=M\n0;JMP\n'


# A quick-and-dirty parser when run as a standalone script.
if __name__ == "__main__":
    import sys
    if(len(sys.argv) > 1):
        with open(sys.argv[1], "r") as a_file:
            for line in a_file:
                tokens = line.strip().lower().split()
                if(len(tokens)==1):
                    if(tokens[0]=='add'):
                        print(VMTranslator.vm_add())
                    elif(tokens[0]=='sub'):
                        print(VMTranslator.vm_sub())
                    elif(tokens[0]=='neg'):
                        print(VMTranslator.vm_neg())
                    elif(tokens[0]=='eq'):
                        print(VMTranslator.vm_eq())
                    elif(tokens[0]=='gt'):
                        print(VMTranslator.vm_gt())
                    elif(tokens[0]=='lt'):
                        print(VMTranslator.vm_lt())
                    elif(tokens[0]=='and'):
                        print(VMTranslator.vm_and())
                    elif(tokens[0]=='or'):
                        print(VMTranslator.vm_or())
                    elif(tokens[0]=='not'):
                        print(VMTranslator.vm_not())
                    elif(tokens[0]=='return'):
                        print(VMTranslator.vm_return())
                elif(len(tokens)==2):
                    if(tokens[0]=='label'):
                        print(VMTranslator.vm_label(tokens[1]))
                    elif(tokens[0]=='goto'):
                        print(VMTranslator.vm_goto(tokens[1]))
                    elif(tokens[0]=='if-goto'):
                        print(VMTranslator.vm_if(tokens[1]))
                elif(len(tokens)==3):
                    if(tokens[0]=='push'):
                        print(VMTranslator.vm_push(tokens[1],int(tokens[2])))
                    elif(tokens[0]=='pop'):
                        print(VMTranslator.vm_pop(tokens[1],int(tokens[2])))
                    elif(tokens[0]=='function'):
                        print(VMTranslator.vm_function(tokens[1],int(tokens[2])))
                    elif(tokens[0]=='call'):
                        print(VMTranslator.vm_call(tokens[1],int(tokens[2])))

        