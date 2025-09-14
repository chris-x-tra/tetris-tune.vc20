
; vc 20 with 8kb ram extension
; screen = $1000-$11ff
; 3.5 K ram = $1200 - $1fff
; 8 k ram   = $2000 - $3fff


; definitions

; kernel routines
PRINT = $ffd2	; kernal routine print ascii char
PLOT = $fff0	; kernal routine set cursor x/y x-reg column, y-reg row
GETIN = $ffe4	; get key
SETLFS   = $ffba
SETNAM   = $ffbd
OPEN     = $ffc0
CLOSE    = $ffc3
PRINT    = $ffd2
LOAD     = $ffd5
SAVE     = $ffd8
GETIN    = $ffe4
PLOT     = $fff0


; constants
CLRSCR = $93
HOME   = $13
SPACE  = $20
screenram = $1000
;screenram = $1c00
colorram = $9400
bgcolor=$900f

linelength = 22
screenheight = 23

basic = $1201                           ;basic start VIC20 + 8k


; zerpo page stuff
mapMemory = $4e
screenMemory = $50      ; 50,51

screenPointer = $62	; zero page pointer to a screen memory position of blocks
screenPointer2 = $64	; 2nd pointer to move data

; vic sound

VIC_CHANNEL1=36874
VIC_CHANNEL2=36875
VIC_CHANNEL3=36876
VIC_CHANNEL4=36877
VIC_VOLUME=36878

durationChannel1 = $68
durationChannel2 = $69
durationChannel3 = $6a
durationChannel4 = $6b

;


;---
; macro basic start sys
;---
!macro start_at .address {
  * = basic
  !byte $0c,$08,$00,$00,$9e
  !if .address >= 10000 { !byte 48 + ((.address / 10000) % 10) }
  !if .address >=  1000 { !byte 48 + ((.address /  1000) % 10) }
  !if .address >=   100 { !byte 48 + ((.address /   100) % 10) }
  !if .address >=    10 { !byte 48 + ((.address /    10) % 10) }
  !byte $30 + (.address % 10), $00, $00, $00
  * = .address
}

;---
; usage: +dbg 'A'
;---
!macro dbg .char {
	pha
	lda #.char
	jsr PRINT
	pla
}

; ---
; ---
; ---
; subroutine: print accu in hex on screen
; accu gets destroyed
prhex   pha             ; save a
        lsr             ; get high nibble
        lsr
        lsr
        lsr
        jsr +           ; print high nibble
        pla             ; get a back
+       and #15         ; get bottom four bits
        cmp #10
        bcc +           ; If 0-9, jump to print
        adc #6          ; Convert ':' to 'A'
+       adc #'0'
        jmp PRINT       ; Convert to character and print

; macro calls sub prhex but saves accu
!macro prhex {
        pha
        jsr prhex
        pla
}


; ---
; Delay via loop and nop
; ---
delay	ldx #$00
	dex
--	ldy #$00
-	dey
	nop
	nop
	bne -
	dex
	bne --
	rts
