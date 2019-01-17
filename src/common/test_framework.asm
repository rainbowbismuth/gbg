INCLUDE "header.asm"
INCLUDE "macros.asm"
INCLUDE "registers.asm"
INCLUDE "constants.asm"
INCLUDE "save.asm"

; TODO: Rewrite usin section / "DS"
TEST_Header_FA EQU (Cartridge_RAM_Begin+0)
TEST_Header_CE EQU (Cartridge_RAM_Begin+1)
TEST_Planned EQU (Cartridge_RAM_Begin+2)
TEST_Ran EQU (Cartridge_RAM_Begin+3)
TEST_Results EQU (Cartridge_RAM_Begin+4)

main:
  ld sp, Work_RAM_End
  call write_test_header
  call test_main
  jp cause_deadlock

; TODO: Think of a way for test code to use
;  interrupts? idk how much sense that even
;  makes for these kind of 'unit test' tests
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

; TODO: Rewrite these using stack/push/pop
;  just to maximize ease of use.
;  testing code won't need the performance.
write_test_header:
  call enable_cart_ram
  ld a, $FA
  ld [TEST_Header_FA], a
  ld a, $CE
  ld [TEST_Header_CE], a
  xor a
  ld [TEST_Planned], a
  ld [TEST_Ran], a
  call disable_cart_ram
  ret

plan_tests:
  call enable_cart_ram
  ld b, a
  ld a, [TEST_Planned]
  add b
  ld [TEST_Planned], a
  jp disable_cart_ram ;tail-call

test_write_b:
  call enable_cart_ram
  ld a, [TEST_Ran]
  ld hl, TEST_Results
  add_a_to_hl
  ld [hl], b

  ld a, [TEST_Ran]
  inc a
  ld [TEST_Ran], a

  jp disable_cart_ram ;tail-call

test_report_success:
  ld a, 1
  ld b, a
  jp test_write_b ;tail-call
  ret

test_report_failure:
  xor a
  ld b, a
  jp test_write_b ;tail-call

cause_deadlock:
  di
  xor a
  ldh [REG_Interrupt_Enable], a
  ldh [REG_Interrupt_Flag], a
  halt ; instructions after this will never be executed.

; This is the 'public API' if you will.
test_plan: MACRO
  ld a, \1
  call plan_tests
  ENDM

test_assert: MACRO
  jr \1, .success\@
  call test_report_failure
  jr .next\@
.success\@:
  call test_report_success
.next\@:
  ENDM
