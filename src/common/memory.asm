; Does using this kind of PUSHS format make sense?

PUSHS
SECTION "memory.asm_rom0",ROM0

; TODO: Start using BC as counter
; 	dec bc
;	  ld a, b
;	  or c
;	  jr nz, .ByteFill


; HL = Destination
; B = Number of bytes to write
; A = The byte to write
memset:
  ; TODO: Check for b = 0?
.loop:
  ld [hl+], a
  dec b
  jr nz, .loop
.exit:
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
  ; TODO: Check for b = 0?
.loop:
  ld a, [de]
  inc de
  ld [hl+], a
  dec b
  jr nz, .loop
.exit:
  ret

; HL = Destination
; DE = Source
; B = Number of 16 byte blocks top copy
memcpy_16:
  ; TODO: Check for b = 0?
.loop:
REPT 16
  ld a, [de]
  inc de
  ld [hl+], a
ENDR
  dec b
  jr nz, .loop
.exit:
  ret

POPS
