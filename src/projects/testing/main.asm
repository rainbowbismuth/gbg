INCLUDE "test_framework.asm"
INCLUDE "memory.asm"

test_main:
  call test_or_behaviour
  call test_cp_behaviour
  call test_dec16_behaviour
  call test_memset_bc
  call test_memzero
  call test_memcpy_bc
  ret

test_or_behaviour:
  test_plan 2

  xor a
  or a
  test_assert_true z

  ld a, 1
  or a
  test_assert_true nz
  ret

test_cp_behaviour:
  test_plan 3

  ld a, 1
  cp 2
  test_assert_true nz

  ld a, 1
  cp 2
  test_assert_false z

  ld a, 1
  cp 2
  test_assert_true c
  ret

test_dec16_behaviour:
  test_plan 1

  ld bc, 1
  dec bc
  test_assert_false z
  ret

test_memset_bc:
  test_plan 1

  ld hl, memset_test_ram
  ld bc, memset_test_ram.end - memset_test_ram
  ld a, 3
  call memset_bc

  ld hl, memset_test_ram
  ld bc, memset_test_ram.end - memset_test_ram
  call sum_byte_range

  cp 3*5
  test_assert_true z
  ret

test_memzero:
  test_plan 1

  ld hl, memzero_test_ram
  ld bc, memzero_test_ram.end - memzero_test_ram
  call memzero

  ld hl, memzero_test_ram
  ld bc, memzero_test_ram.end - memzero_test_ram
  call sum_byte_range

  or a
  test_assert_true z
  ret

test_memcpy_bc:
  test_plan 1

  ld hl, memcpy_bc_test_ram
  ld de, memcpy_bc_test_data
  ld bc, memcpy_bc_test_data.end - memcpy_bc_test_data
  call memcpy_bc

  ld hl, memcpy_bc_test_ram
  ld bc, memcpy_bc_test_data.end - memcpy_bc_test_data
  call sum_byte_range

  cp a, 1+2+3+4+5+100
  test_assert_true z
  ret


; HL = source
; BC = number of bytes
; outputs total in A
; clobbers d
sum_byte_range:
  xor a
  ld d, a
.loop:
  ld a, d
  add a, [hl]
  ld d, a
  inc hl
  dec bc
  ld a, b
  or c
  jp nz, .loop
  ld a, d
  ret

SECTION "Test ROM", ROM0
memcpy_bc_test_data:
DB 1,2,3,4,5,100
.end:

SECTION "Test RAM", WRAM0
memset_test_ram:
DS 5
.end:

memzero_test_ram:
DS $200
.end:

memcpy_bc_test_ram:
DS (memcpy_bc_test_data.end - memcpy_bc_test_data)
