INCLUDE "test_framework.asm"

test_main:
  test_plan 3

  xor a
  or a
  test_assert z

  ld a, 1
  or a
  test_assert nz

  ld a, 1
  cp 1
  test_assert z

  ret
