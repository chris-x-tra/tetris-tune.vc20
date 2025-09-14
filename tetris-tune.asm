!cpu 6502
;!to "tetris-tune.prg", cbm

;---
; $1201  is basic start 8k
;---

; schaun, was von hand rein passt
* = $1220

!source "var_const.asm"


;---
; load charset at 1800
;---
	*=$1800
	!bin "charset.bin"

;---
; Start: Basic SYS cmd and  Main
;---
	+start_at $2000

!source "main.asm"

!source "tune.asm"
