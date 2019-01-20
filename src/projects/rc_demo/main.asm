INCLUDE "header.asm"
INCLUDE "macros.asm"
INCLUDE "registers.asm"
INCLUDE "constants.asm"
INCLUDE "memory.asm"

START_X EQU 195
START_Y EQU 210

main:
  call disable_lcd
  call reset_palettes
  call clear_tile_map_0
  call load_rc_logo_into_tiledata
  call load_rc_logo_into_tilemap

  call turn_on_lcd

  ld a, START_X
  ldh [REG_Scroll_X], a
  ld a, START_Y
  ldh [REG_Scroll_Y], a

  ldh a, [REG_Interrupt_Enable]
  set 0, a
  set 1, a
  ldh [REG_Interrupt_Enable], a

  ldh a, [REG_LCD_Status]
  set 3, a
  ldh [REG_LCD_Status], a

  ld a, $FF
  ldh [REG_LCD_Y_Compare], a

  ei
  nop

.loop:
  halt
  jr .loop

  call cause_deadlock

vblank:
  ;ldh a, [REG_Scroll_Y]
  ;inc a
  ;ldh [REG_Scroll_Y], a
  ;ldh a, [REG_Scroll_X]
  ;inc a
  ;ldh [REG_Scroll_X], a
  reti

stat:
;  reti
  ldh a, [REG_LCD_Y]
  cp a, LCD_Y_VBLANK-1
  jr c, .continue
  jr .return
.continue:
  ldh a, [$FA]
  inc a
  ldh [$FA], a
  and a, %00001111

  ;ld b, a
  ;ldh a, [$FB]
  ;and a, $0F
  ;add a, b

  ld hl, offsets
  add_a_to_hl
  ld a, [hl]
  ld b, a

  ld a, START_X-18
  ;ld c, a

  ;ldh a, [REG_Scroll_X]
  add a, b
  ;add a, c
  ldh [REG_Scroll_X], a
.return:
  reti

timer:
  reti

serial:
  reti

joypad:
  reti

offsets:
  DB 0, 1, 3, 9         ; 4
  DB 16, 32, 40, 42     ; 8
  DB 42, 40, 32, 16     ; 12
  DB 9, 3, 1, 0         ; 16
  DB 0, -1, -3, -9      ; 20
  DB -16, -32, -40, -42 ; 24
  DB -42, -40, -32, -16 ; 28
  DB -9, -3, -1, 0      ; 32


INCLUDE "gfx.asm"

load_rc_logo_into_tilemap:
  ld a, 1
  ld de, 32-5
  ld hl, Tile_Map_0_Begin
  REPT 6

  ld [hl+], a
  inc a
  ld [hl+], a
  inc a
  ld [hl+], a
  inc a
  ld [hl+], a
  inc a
  ld [hl+], a
  inc a

  add hl, de
  ;inc h
  ; sla l
  ;ld b, a
  ;ld a, l,
  ;add a, 16
  ;ld l, a
  ;ld a, b
  ENDR
  ret

load_rc_logo_into_tiledata:
  call wait_for_vram_access
  ld de, gfx_rc_logo
  ld hl, Tile_Data_0_Begin + 16
  ld b, 255
  call memcpy_16
  ret

cause_deadlock:
  di
  xor a
  ldh [REG_Interrupt_Enable], a
  ldh [REG_Interrupt_Flag], a
  halt ; instructions after this will never be executed.

gfx_rc_logo:
INCBIN "gfx/rc_demo/rc_logo.2bpp"
