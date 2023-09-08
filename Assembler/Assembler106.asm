// Tests whether the value at memory address 0 is equal to the value at memory address 1.
// The result will be stored in memory address 6, with 1 meaning true and 0 meaning false.
@0
D=M
@1
D=D-M
@EQ
D;JEQ
@6
M=0
@END
0;JMP
(EQ)
@6
M=1
(END)