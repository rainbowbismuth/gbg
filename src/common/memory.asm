; HL = Destination
; B = Number of bytes to write
; A = The byte to write
memset:
  ld [hl+], a
  dec b
  jr nz, memset
  ret

; HL = Destination
; BC = Number of bytes to write
; A = The byte to write
; clobbers D
memset_bc:
  ld d, a
.loop:
  ld a, d
  ld [hl+], a
  dec bc
  ld a, b
  or c
  jp nz, .loop
  ret


; HL = Destination
; BC = Number of zero bytes to write
; clobbers A
memzero:
  xor a
  ld [hl+], a
  dec bc
  ld a, b
  or c
  jr nz, memzero
  ret


; HL = Destination
; B = Number of 16 bytes blocks to write
; A = The byte to write
memset_16:
  ; TODO: Check for b = 0?
.loop:
REPT 16
  ld [hl+], a
ENDR
  dec b
  jr nz, .loop
.exit:
  ret

; HL = Destination
; DE = Source
; B = Number of bytes to copy
memcpy:
  ld a, [de]
  inc de
  ld [hl+], a
  dec b
  jr nz, memcpy
  ret

; HL = Destination
; DE = Source
; BC = Number of bytes to copy
memcpy_bc:
  ld a, [de]
  inc de
  ld [hl+], a
  dec bc
  ld a, b
  or c
  jr nz, memcpy_bc
  ret

; HL = Destination
; DE = Source
; B = Number of 16 byte blocks top copy
memcpy_16:
REPT 16
  ld a, [de]
  inc de
  ld [hl+], a
ENDR
  dec b
  jr nz, memcpy_16
  ret
