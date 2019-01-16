ld_freq_lo: MACRO
  ld \1, ((DIV(MUL(2048.0, \2-64),\2.0)) & $FF)
  ENDM

ld_freq_hi: MACRO
  ld \1, (((DIV(MUL(2048.0, \2-64),\2.0)) & $FF00)>>8)
  ENDM

disable_sound:
  xor a
  ldh [REG_Sound_OnOff], a
  ret

enable_sound:
  ;enable sound system
  ld a, $80
  ldh [REG_Sound_OnOff], a

  ;max volume, both L & R
  ld a, %01110111
  ldh [REG_Sound_MasterVolume], a

  ;disable all channels
  xor a
  ldh [REG_Sound_Panning], a

  ret


start_tone:
  ;DISABLE CHANNEL 1
  ldh a, [REG_Sound_Panning]
  res 0, a ; S01 for Channel 1
  res 4, a ; S02 for Channel 1
  ldh [REG_Sound_Panning], a


  ;disable sweep
  ld a, $00
  ldh [REG_Sound1_Sweep], a

  ;50% wave pattern & max length
  ld a, %10111111
  ldh [REG_Sound1_LengthDuty], a

  ;max volume, medium down envelope
  ld a, %11110100
  ldh [REG_Sound1_VolumeEnvelope], a
  ret

end_tone:
  ;ENABLE CHANNEL 1
  ldh a, [REG_Sound_Panning]
  set 0, a ; S01 for Channel 1
  set 4, a ; S02 for Channel 1
  ldh [REG_Sound_Panning], a
  ret

;ugly i know
tone_macro: MACRO
  call start_tone
  ld_freq_lo a, \1
  ldh [REG_Sound1_FreqLow], a
  ld_freq_hi a, \1
  or $80 ;add the restart sound bit
  ldh [REG_Sound1_FreqHi], a
  call end_tone
  ret
  ENDM

play_a4_tone:
  tone_macro 110

play_b4_tone:
  tone_macro 123

play_cs5_tone:
  tone_macro 139

play_d5_tone:
  tone_macro 147

play_e5_tone:
  tone_macro 165

play_fs5_tone:
  tone_macro 185

play_gs5_tone:
  tone_macro 208

play_a5_tone:
  tone_macro 220
