INCLUDE "header.asm"
INCLUDE "macros.asm"
INCLUDE "registers.asm"
INCLUDE "constants.asm"
INCLUDE "memory.asm"


main:
  ret
  
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


pico8_palette:
pico8_black:
  DB 0, 0, 0
pico8_dark_blue:
  DB 29, 43, 83
pico8_dark_purple:
  DB 126, 37, 83
pico8_dark_green:
  DB 0, 135, 81
pico8_brown:
  DB 171, 82, 54
pico8_dark_gray:
  DB 95, 87, 79
pico8_light_gray:
  DB 194, 195, 199
pico8_white:
  DB 255, 241, 232
pico8_red:
  DB 255, 0, 77
pico8_orange:
  DB 255, 163, 0
pico8_yellow:
  DB 255, 236, 39
pico8_green:
  DB 0, 228, 54
pico8_blue:
  DB 41, 173, 255
pico8_indigo:
  DB 131, 118, 156
pico8_pink:
  DB 255, 119, 168
pico8_peach:
  DB 255, 204, 170
