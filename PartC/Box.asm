// Personalised capstone box for Abhinav Kumar (roll 2501350050).
// K = 50; start row = 50; height = 20 rows; width = 48 pixels = 3 words.
// The rectangle is black while any key is pressed, and is cleared on release.

(LOOP)
    @KBD
    D=M
    @SET_BLACK
    D;JNE
    @SET_CLEAR
    0;JMP

(SET_BLACK)
    @color
    M=-1
    @INITIALISE
    0;JMP

(SET_CLEAR)
    @color
    M=0

(INITIALISE)
    // SCREEN + (32 words per row * 50 rows) = SCREEN + 1600.
    @SCREEN
    D=A
    @1600
    D=D+A
    @address
    M=D

    @20
    D=A
    @rows
    M=D

(ROW_LOOP)
    @rows
    D=M
    @LOOP
    D;JEQ

    // First 16-pixel word of this row.
    @color
    D=M
    @address
    A=M
    M=D
    @address
    M=M+1

    // Second 16-pixel word of this row.
    @address
    A=M
    M=D
    @address
    M=M+1

    // Third 16-pixel word of this row: total width = 48 pixels.
    @address
    A=M
    M=D
    @address
    M=M+1

    // Advance from the next free word (base + 3) to next row (base + 32).
    @29
    D=A
    @address
    M=D+M

    @rows
    M=M-1
    @ROW_LOOP
    0;JMP
