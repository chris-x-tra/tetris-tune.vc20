;---
;
; 4 voices vc 20 tune player by chrissie ^ x-tra-designs 09.2025
;
; keys 1 - 4 disable voice
; keys 5 - 8 enable voice again
;
;---

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

        jsr init_sound

        sei             ; no interrupts!

mainloop

	; https://codebase64.org/doku.php?id=base:making_stable_raster_routines#making_stable_raster_routines_c64_and_vic-20
	ldx #$84
-	cpx $9004	; wait for raster line unten ausserhalb schirm
	bne -

        jsr play_sound
        jsr get_key_via

	jmp mainloop


        ; -----
        ; key
        ; -----

key1    !byte 0
key2    !byte 0
key3    !byte 0
key4    !byte 0

get_key_via

        lda #%01111111
        sta $9120
        lda $9121


        cmp #%11111110        ; key 2
        bne +
        ldy #$01
        sty key2

+       cmp #%11111101        ; key 4
        bne +
        ldy #$01
        sty key4

+       cmp #$fb             ; key 6
        bne +
        ldy #$00
        sty key2

+       cmp #$f7          ; key  8
        bne +
        ldy #$00
        sty key4
+
        ; ----
        lda #%11111110
        sta $9120      
        lda $9121

        cmp #$fe        ; key 1
        bne +
        ldy #$01
        sty key1

+        cmp #$fd        ; key 3
        bne +
        ldy #$01
        sty key3

+       cmp #$fb          ; key 5
        bne +
        ldy #$00
        sty key1

+       cmp #$f7          ; key  7
        bne +
        ldy #$00
        sty key3

+
        ; Anzeige
        lda key1
        ldy #6*22+5
        jsr hexout
        lda key2
        ldy #6*22+9
        jsr hexout
        lda key3
        ldy #6*22+13
        jsr hexout
        lda key4
        ldy #6*22+17
        jsr hexout
        rts

        ; -----
        ; init
        ; -----

tune_over       !byte 00,00,00,00
tune_channels   !byte 00,00,00,00

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

        lda #<voice4
        sta mod_voice4+1
        lda #>voice4
        sta mod_voice4+2

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

        ldx key1                ; stimme abschaltbar
        bne +
        sta VIC_CHANNEL1
+
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

        ldx key2                ; stimme abschaltbar
        bne +
        sta VIC_CHANNEL2
+        

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

        ldx key3                ; stimme abschaltbar
        bne +
        sta VIC_CHANNEL3
+
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

        ;
        ; play CHANNEL4
        lda durationChannel4
        cmp #$ff                ; $ff in duration = end of this channel lsit
        beq play4_end
        cmp #$00
        beq +
        dec durationChannel4
        jmp play4_end
+
        ; get next note and duration
        ldy #0
        jsr mod_voice4

        ldx key4                ; stimme abschaltbar
        bne +
        sta VIC_CHANNEL4
+
        sta tune_channels+3
        ldy #1
        jsr mod_voice4
        sta durationChannel4

        ; end of voic1 - never increment be silent
        ldy #1
        jsr mod_voice4
        cmp #$ff
        beq +

        clc
        lda mod_voice4+1
        adc #2
        sta mod_voice4+1
        bcc +
        inc mod_voice4+2
+
play4_end

        ; beim abschalten abnullen
        lda key1                ; stimme abschaltbar
        beq +
        lda #0
        sta VIC_CHANNEL1
+       
        lda key2                ; stimme abschaltbar
        beq +
        lda #0
        sta VIC_CHANNEL2
+
        lda key3                ; stimme abschaltbar
        beq +
        lda #0
        sta VIC_CHANNEL3
+
        lda key4                ; stimme abschaltbar
        beq +
        lda #0
        sta VIC_CHANNEL4
+

        ; ausgabe auf Bildschirm
        ; ausgabe noten
        ldy #0+2*22+5
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

        iny
        iny
        lda tune_channels+3
        jsr hexout 

        ;
        ldy #3*22+5
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

        iny
        iny
        lda durationChannel4
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
mod_voice4  lda voice4,y
        rts

