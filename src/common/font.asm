gfx_potash:
INCBIN "gfx/common/potash.2bpp"

load_potash:
  call wait_for_vram_access

  ld de, gfx_potash
  ld hl, Tile_Data_0_Begin
  ld b, 255
  call memcpy_16

  ret
