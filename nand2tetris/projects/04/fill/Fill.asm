// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

	@colored
	M=0			// screen is white at the beginning

(LOOP_PRESS)
	@24576
	D=M
	@KEY_PRESSED
	D;JGT			// if key pressed, goto KEY_PRESSED
				// else
	@colored
	D=M
	@CHANGE_COLOR
	D;JGT			// if screen black, CHANGE_COLOR (WHITEN)
				// else
	@LOOP_PRESS
	0;JMP
	
(KEY_PRESSED)
	@colored
	D=M
	@CHANGE_COLOR
	D;JEQ			// if screen white, BLACKEN
				// else
	@LOOP_PRESS
	0;JMP			// jump to LOOP_PRESS
	

(CHANGE_COLOR)

	@8192
	D=A
	@count
	M=D			// set count to 8K (number of pixels)

	@16384
	D=A
	@current_row
	M=D			// set current row to first pixel

	@colored
	D=M
	@BLACKEN
	D;JEQ			// if screen white, BLACKEN
				// else
	@WHITEN
	0;JMP			// WHITEN
	
(WHITEN)			// turn whole screen white

	@count
	D=M
	@WHITEN_LEAVE
	D;JEQ			// goto WHITEN_LEAVE if count == 0

	@current_row
	A=M
	M=0			// set pixel to 0

	@count
	M=M-1			// count -= 1

	@current_row
	M=M+1			// current_row += 1

	@WHITEN
	0;JMP

(WHITEN_LEAVE)
	@colored
	M=0
	@LOOP_PRESS
	0;JMP			// jump to LOOP_PRESS


(BLACKEN)			// turn whole screen black

	@count
	D=M
	@BLACKEN_LEAVE
	D;JEQ			// goto BLACKEN_LEAVE if count == 0

	@current_row
	A=M
	M=-1			// set pixel to -1 (all 1s)

	@count
	M=M-1			// count -= 1

	@current_row
	M=M+1			// current_row += 1

	@BLACKEN
	0;JMP

(BLACKEN_LEAVE)
	@colored
	M=1
	@LOOP_PRESS
	0;JMP			// jump to LOOP_PRESS
