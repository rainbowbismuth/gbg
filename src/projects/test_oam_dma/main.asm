INCLUDE "header.asm"
INCLUDE "macros.asm"
INCLUDE "registers.asm"
INCLUDE "constants.asm"
INCLUDE "memory.asm"

main:
  ld sp, Work_RAM_End
  call disable_lcd
  call reset_gfx
  jp cause_deadlock ; tail call

vblank:
  reti
stat:
  reti
timer:
  reti
serial:
  reti
joypad:
  reti

cause_deadlock:
  di
  xor a
  ldh [REG_Interrupt_Enable], a
  ldh [REG_Interrupt_Flag], a
  halt ; instructions after this will never be executed.

INCLUDE "gfx.asm"
INCLUDE "font.asm"

SECTION "main.asm_wram", WRAM0,ALIGN[8]

OBJ_0_Y: DS 1
OBJ_0_X: DS 1
OBJ_0_Tile: DS 1
OBJ_0_Flag: DS 1

OBJ_1_Y: DS 1
OBJ_1_X: DS 1
OBJ_1_Tile: DS 1
OBJ_1_Flag: DS 1

OBJ_Rest DS (38*4)

SECTION "main.asm_rom0", ROM0

write_byte: MACRO
  ld a, \2
  ld [\1], a
  ENDM

load_objects_to_ram:
  write_byte OBJ_0_Y, 20
  write_byte OBJ_0_X, 25
  write_byte OBJ_0_Tile, "e"
  write_byte OBJ_0_Flag, 0
  write_byte OBJ_1_Y, 25
  write_byte OBJ_1_X, 27
  write_byte OBJ_1_Tile, "B"
  write_byte OBJ_1_Flag, (1 << 5)
  ld hl, OBJ_Rest
  ld b, 38*4
  ld a, 0
  jp memset ; tail call

turn_on_obj:
  ldh a, [REG_LCD_Control]
  set 1, a ; turn on OBJ
  ldh [REG_LCD_Control], a
  ret

reset_gfx:
  call reset_palettes
  call load_potash
  call clear_tile_map_0

  call install_oam_dma_code_to_hram
  call load_objects_to_ram

  ld a, (OBJ_0_Y / $100)
  call run_oam_dma

  call turn_on_lcd
  jp turn_on_obj ; tail call?
