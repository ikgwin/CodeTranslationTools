// Tests jump instructions by checking if the value at memory address 0 is greater than the value at memory address 1.
// The result will be stored in memory address 2, with 1 meaning true and 0 meaning false.
@0
D=M
@1
D=D-M
@GT
D;JGT
@2
M=0
@END
0;JMP
(GT)
@2
M=1
(END)