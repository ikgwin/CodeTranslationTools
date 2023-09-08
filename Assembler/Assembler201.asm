// Test program for symbol table with labels
// This program calculates the sum of 1 to 10 using a loop

    // sum = 0
    @sum
    M=0
    //counter= 1
    @counter
    M=1
(LOOP)
    // add countr to sum
    @counter
    D=M
    @sum
    M=D+M
    // incr counter
    @counter
    MD=M+1
    // chec if counter is greater than 10
    @10
    D=M-D
    @END
    D;JLE
    // loop back to start if counter less than equal to 10
    @LOOP
    0;JMP
(END)
    @END
    0;JMP