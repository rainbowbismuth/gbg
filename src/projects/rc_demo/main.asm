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
  ldh a, [$FB]
  inc a
  ldh [$FB], a
  srl a
  srl a
  ldh [$FA], a
  reti

stat:
  ldh a, [REG_LCD_Y]
  cp a, LCD_Y_VBLANK-1
  jr c, .continue
  jr .return
.continue:
  ldh a, [$FA]
  inc a
  ldh [$FA], a
  and a, $1F

  ld hl, offsets
  add_a_to_hl
  ld a, [hl]
  ld b, a

  ld a, START_X-15
  add a, b
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
  DB 0, 1, 2, 3
  DB 4, 6, 8, 10
  DB 12, 14, 16, 18
  DB 20, 23, 25, 26
  DB 26, 25, 23, 20
  DB 18, 16, 14, 12
  DB 10, 8, 6, 4
  DB 3, 2, 1, 0

  DB 0, -1, -2, -3
  DB -4, -6, -8, -10
  DB -12, -14, -16, -18
  DB -20, -23, -25, -26
  DB -26, -25, -23, -20
  DB -18, -16, -14, -12
  DB -10, -8, -6, -4
  DB -3, -2, -1, 0


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
