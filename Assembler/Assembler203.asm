// Test program for symbol table with labels and variables
// This program calculates the factorial of 5

    @fact
    M=1
    @counter
    M=5
(LOOP)
    @fact
    D=M
    @counter
    D=D&A
    @fact
    M=D
    @counter
    MD=M-1
    @0
    D=M
    @LOOP
    D;JNE
    @END
    0;JMP