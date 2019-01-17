enable_cart_ram:
  ld hl, $0000
  ld [hl], $0A
  ret

disable_cart_ram:
  ld hl, $0000
  ld [hl], $00
  ret
