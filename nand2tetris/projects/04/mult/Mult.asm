// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.

	@sum
	M=0		// prepare sum variable

	@R1
	D=M
	@multiplier
	M=D		// copy R1 to multipler

(LOOP)
	@multiplier
	D=M
	@SAVE
	D;JLE		// leave loop if multiplier is 0 or less

	@R0
	D=M
	@sum
	M=M+D		// sum += R0

	@multiplier
	M=M-1		// mutliplier -= 1

	@LOOP
	0;JMP		// goto LOOP
(SAVE)
	@sum
	D=M
	@R2
	M=D

(END)
	@END
	0;JMP		// infinite loop



