add_a_to_hl: MACRO
  add a, l
  ld l, a
  jr nc, .notcarry\@
  inc h
.notcarry\@
  ENDM
