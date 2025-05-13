; set up some numbers
        LDI R16, 60  ; X
        LDI R17, 90  ; Y
        LDI R18, 44  ; Z
        LDI R19, 100 ; 100

; do some math
        ADD R16, R17
        ADD R16, R19
        SUB R16, R18

; save the answer
        ST R16, Answer

; loop forever
loop: JMP loop

; memory stuff
Answer: .DATA 0
X:      .DATA 0
Y:      .DATA 0
Z:      .DATA 0