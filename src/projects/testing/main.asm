INCLUDE "test_framework.asm"

test_main:
  call test_or_behaviour
  call test_cp_behaviour
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
