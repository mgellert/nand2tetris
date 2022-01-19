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

(START)

@KBD
D=M

@R0
M=0

@PUSHED
D;JEQ       // if button is pushed set R0 to -1 else keep 0

@R0
M=-1

(PUSHED)
@i
M=0         // start of loop reset i to 0

(LOOP)
@i
D=M

@8192       // loop 8192 times as that is the size of the screen (256*512/16)
M=A
D=M-D

@END
D;JEQ       // if end of loop jump

@i
D=M

@SCREEN
D=D+A       // calculate next position on screen to set

@temp
M=D         // save calculated position

@R0
D=M         // load the value that has to be filled in (0/-1)

@temp
A=M
M=D         // load the address to be filled in

@i
DM=M+1      // increment loop variable

@LOOP
D;JMP

(END)
@START
0;JMP