// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, the
// program clears the screen, i.e. writes "white" in every pixel.


(INIT)
    @SCREEN
    D=A
    @i
    M=D
    @fill
    M=0

    @KBD
    D=M
    @SET_BLACK
    D; JGT
    @SET_WHITE
    D; JEQ

(SET_BLACK)
    @fill
    M=-1
    @DRAW_SCREEN
    0; JMP

(SET_WHITE)
    @fill
    M=0
    @DRAW_SCREEN
    0; JMP

(DRAW_SCREEN)
    @KBD
    D=A
    @i
    D=D-M
    @INIT
    D; JEQ

    @fill
    D=M
    @i
    A=M
    M=D
    @i
    M=M+1

    @DRAW_SCREEN
    0; JMP
