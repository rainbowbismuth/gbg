INCLUDE "header.asm"
INCLUDE "macros.asm"
INCLUDE "registers.asm"
INCLUDE "constants.asm"
INCLUDE "memory.asm"

assert: MACRO
  jr \1, .next\@
  jp cause_deadlock
.next\@:
  ENDM

main:
  ld sp, Work_RAM_End


  xor a
  or a
  assert z


  call disable_lcd
  call enable_sound
  call reset_gfx

  call enable_cart_ram

  ; write to cart ram cause why not
  ld a, $BA
  ld [Cartridge_RAM_Begin],a
  ld a, $BE
  ld [Cartridge_RAM_Begin+1],a

  call disable_cart_ram

  ld a, 7
  ld [Work_RAM_Begin], a

.loop:
  call enable_joypad
  halt

  ; this is silly because we just looping no matter what
  ld a, [Work_RAM_Begin]
  dec a
  ld [Work_RAM_Begin], a
  jr nz, .loop
  ld a, 7
  ld [Work_RAM_Begin], a


  call read_joypad_dpad
  bit 0, a
  jp z, .play_a4
  bit 1, a
  jp z, .play_b4
  bit 2, a
  jp z, .play_cs5
  bit 3, a
  jp z, .play_d5

  call read_joypad_buttons
  bit 0, a
  jp z, .play_e5
  bit 1, a
  jp z, .play_fs5
  bit 2, a
  jp z, .play_gs5
  bit 3, a
  jp z, .play_a5

  jp .loop

.play_a4
  call play_a4_tone
  jp .loop

.play_b4
  call play_b4_tone
  jp .loop

.play_cs5
  call play_cs5_tone
  jp .loop

.play_d5
  call play_d5_tone
  jp .loop

.play_e5
  call play_e5_tone
  jp .loop

.play_fs5
  call play_fs5_tone
  jp .loop

.play_gs5
  call play_gs5_tone
  jp .loop

.play_a5
  call play_a5_tone
  jp .loop



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



read_joypad_dpad:
  xor a
  ldh [REG_Joypad], a ; reset joypad

  set 5, a ; select direction keys
  ldh [REG_Joypad], a
  REPT 5
  ldh a, [REG_Joypad] ; repeat bc bouncing
  ENDR
  and $0F ; keep low nibble only
  ret

read_joypad_buttons:
  xor a
  ldh [REG_Joypad], a ; reset joypad

  set 4, a ; select button keys
  ldh [REG_Joypad], a
  REPT 5
  ldh a, [REG_Joypad] ; repeat bc bouncing
  ENDR
  and $0F ; keep low nibble only
  ret


; This is dumb, shouldn't even be trying to use
; the joystick interrupt tbh
enable_joypad:
  ld a, [REG_Interrupt_Enable]
  set 4, a
  set 0, a ; v-blank???
  ldh [REG_Interrupt_Enable], a
  reti

cause_deadlock:
  di
  xor a
  ldh [REG_Interrupt_Enable], a
  ldh [REG_Interrupt_Flag], a
  halt ; instructions after this will never be executed.

INCLUDE "save.asm"
INCLUDE "sound.asm"
INCLUDE "gfx.asm"
INCLUDE "font.asm"
