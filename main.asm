
main

;---
; setup stuff, screen
;---
	lda #CLRSCR
	jsr PRINT

	; color ram
	;lda #$06		; blue
	lda #$01		; white
	ldx #$00
-	sta colorram,x
	sta colorram+$100,x
	dex
	bne -

	lda #$5		; print color also white
	jsr PRINT

	lda #8		; screen black, border black
	sta bgcolor	

	; Video Chip Config
	; screen memory at $1000
	lda #$16
	sta $9002

	; character set at $1800
	lda #$ce
	sta $9005

;---
; main
;---
        ;VIDEO_EFFECT = 1

        jsr init_sound

mainloop

	; https://codebase64.org/doku.php?id=base:making_stable_raster_routines#making_stable_raster_routines_c64_and_vic-20
	ldx #$84
-	cpx $9004	; wait for raster line unten ausserhalb schirm
	bne -

        jsr play_sound


!ifdef VIDEO_EFFECT {
	jsr amazingVideoEffect
}



	jmp mainloop

        ; init

tune_over       !byte 00,00,00
tune_channels   !byte 00,00,00

init_sound

        ; initialize volume
        lda #$0f
        sta VIC_VOLUME
        lda #$00
        sta VIC_CHANNEL1
        sta VIC_CHANNEL2
        sta VIC_CHANNEL3
        sta VIC_CHANNEL4

        lda #$ff
        sta tune_over
        sta tune_over+1
        sta tune_over+2

        lda #$00
        sta durationChannel1
        sta durationChannel2
        sta durationChannel3

        ; init player
        lda #<voice1
        sta mod_voice1+1
        lda #>voice1
        sta mod_voice1+2

        lda #<voice2
        sta mod_voice2+1
        lda #>voice2
        sta mod_voice2+2

        lda #<voice3
        sta mod_voice3+1
        lda #>voice3
        sta mod_voice3+2

        rts

        ;
        ; play sound
        ;
play_sound
        pha
        tya
        pha

        ;
        ; play CHANNEL1
        lda durationChannel1
        cmp #$ff                ; $ff in duration = end of this channel track
        beq play1_end
        cmp #$00
        beq +
        dec durationChannel1
        jmp play1_end
+
        ; get next note and duration
        ldy #0
        jsr mod_voice1
        sta VIC_CHANNEL1
        sta tune_channels
        ldy #1
        jsr mod_voice1
        sta durationChannel1

        ; end of voic1 - never increment be silent
        ldy #1
        jsr mod_voice1
        cmp #$ff
        beq +

        clc
        lda mod_voice1+1
        adc #2
        sta mod_voice1+1
        bcc +
        inc mod_voice1+2

+
play1_end

        ;
        ; play CHANNEL2
        lda durationChannel2
        cmp #$ff                ; $ff in duration = end of this channel lsit
        beq play2_end
        cmp #$00
        beq +
        dec durationChannel2
        jmp play2_end
+
        ; get next note and duration
        ldy #0
        jsr mod_voice2
        sta VIC_CHANNEL2
        sta tune_channels+1
        ldy #1
        jsr mod_voice2
        sta durationChannel2

        ; end of voic1 - never increment be silent
        ldy #1
        jsr mod_voice2
        cmp #$ff
        beq +

        clc
        lda mod_voice2+1
        adc #2
        sta mod_voice2+1
        bcc +
        inc mod_voice2+2
+
play2_end

        ;
        ; play CHANNEL3
        lda durationChannel3
        cmp #$ff                ; $ff in duration = end of this channel lsit
        beq play3_end
        cmp #$00
        beq +
        dec durationChannel3
        jmp play3_end
+
        ; get next note and duration
        ldy #0
        jsr mod_voice3
        sta VIC_CHANNEL4        ; rauschen
        sta tune_channels+2
        ldy #1
        jsr mod_voice3
        sta durationChannel3

        ; end of voic1 - never increment be silent
        ldy #1
        jsr mod_voice3
        cmp #$ff
        beq +

        clc
        lda mod_voice3+1
        adc #2
        sta mod_voice3+1
        bcc +
        inc mod_voice3+2
+
play3_end

        ; ausgabe auf Bildschirm

        ; ausgabe noten
        ldy #0
        lda tune_channels+0
        jsr hexout

        iny
        iny
        lda tune_channels+1
        jsr hexout

        iny
        iny
        lda tune_channels+2
        jsr hexout 

        ;
        ldy #22
        lda durationChannel1
        jsr hexout

        iny
        iny
        lda durationChannel2
        jsr hexout

        iny
        iny
        lda durationChannel3
        jsr hexout 


play_end
        ; all three channels end = $ff in duration?
        lda durationChannel1
        cmp #$ff
        bne +
        lda durationChannel2
        cmp #$ff
        bne +
        lda durationChannel3
        cmp #$ff
        bne +

        ; re init
        jsr init_sound
+
play_return
        pla
        tay
        pla
        rts

mod_voice1  lda voice1,y
        rts
mod_voice2  lda voice2,y
        rts
mod_voice3  lda voice3,y
        rts

; ---
; ---
; ---
!ifdef VIDEO_EFFECT {
amazingVideoEffect
	ldy #16       ; perform amazing video effect
	lda $900f
	tax
	eor #$f7
	sta $900f
	stx $900f
	sta $900f
	stx $900f
	sta $900f
	stx $900f
	sta $900f
	stx $900f
	sta $900f
	stx $900f
	sta $900f
	stx $900f
	rts
	}

