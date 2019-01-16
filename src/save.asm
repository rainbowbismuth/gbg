enable_cart_ram:
  ld a, $0A
  ld [$0000], a
  ret

disable_cart_ram:
  xor a
  ld [$0000], a
  ret
