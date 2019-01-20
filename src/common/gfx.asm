Tile_Data_0_Begin EQU $8000
Tile_Data_0_End EQU $87FF
Tile_Data_1_Begin EQU $8800
Tile_Data_1_End EQU $8FFF
Tile_Data_2_Begin EQU $9000
Tile_Data_2_End EQU $97FF

Tile_Map_0_Begin EQU $9800
Tile_Map_0_End EQU $9BFF
Tile_Map_1_Begin EQU $9C00
Tile_Map_1_End EQU $9FFF

disable_lcd:
  ld a, $01 ; enable v-blank only
  ldh [REG_Interrupt_Enable], a

.loop:
  halt

  ;; TODO: Why doesn't this work?????
  ;; ld a, [$FF00+REG_Interrupt_Flag]
  ;; cp a, $01   ; v-blank set?

  ldh a, [REG_LCD_Y]
  cp LCD_Y_VBLANK+1
  jr nz, .loop

  xor a
  ldh [REG_Interrupt_Enable], a ; disable interrupts
  ldh [REG_LCD_Control], a ; turn off LCD
  ret

reset_palettes:
  ld a, %11100100
  ldh [REG_BG_Palette], a
  ldh [REG_OB_Palette_1], a
  ldh [REG_OB_Palette_2], a
  xor a
  ldh [REG_Scroll_X], a
  ldh [REG_Scroll_Y], a
  ret

turn_on_lcd:
  ld a, $80 ; enable LCD display
  set 4, a ; use Tile_Data_0 addr mode
  set 0, a ; turn on BG
  ldh [REG_LCD_Control], a
  ret

wait_for_vram_access:
  ; TODO: is there anything smarter than can be done here?
  ;       also what mode is this exactly again?
  ld hl, $FF00+REG_LCD_Status
.wait:
  bit 1, [hl]
  jr nz, .wait
  ret

clear_tile_map_0:
  call wait_for_vram_access

  ld hl, Tile_Map_0_Begin
  xor a
  ld b, (32*32)/16
  call memset_16

  ret


; input
;   DE = tile map start
;   BC = message
; output
;   BC = pointer to NUL at end of message
; clobbers
;   af, bc, de, hl
print_ascii:
.loop:
    ld a, [bc]  ; load char
    inc bc
    or a        ; test if NUL
    jr z, .exit

    ld [de], a  ; draw
    inc de

    jr .loop
.exit:
    ret

test_message:
  DB "Hello music, I love you!     ",0
