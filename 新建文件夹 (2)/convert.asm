; BCD to 7-segment conversion program

start:

    ; Process the low digit
    LDA BCD
    ANI 0x0F
    MOV R0, A
    CALL convert_to_7seg
    STA lowDigit

    ; Process the high digit
    LDA BCD
    ANI 0xF0
    ROR A
    ROR A
    ROR A
    ROR A
    CALL convert_to_7seg
    STA highDigit

loop:
    JMP loop         ; Infinite loop to prevent program overflow execution data

; Digit to 7-segment code conversion
convert_to_7seg:
    MOV R1, A
    MOV DPTR, #segTable
    MOVC A, @A+DPTR
    RET

; Data section
BCD:         .data 1 0x18
lowDigit:    .data 1 0x00
highDigit:   .data 1 0x00

segTable:
    .db 0x40    ; 0
    .db 0x79    ; 1
    .db 0x24    ; 2
    .db 0x30    ; 3
    .db 0x19    ; 4
    .db 0x12    ; 5
    .db 0x02    ; 6
    .db 0x78    ; 7
    .db 0x00    ; 8
    .db 0x10    ; 9