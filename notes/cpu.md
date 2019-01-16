# HALT Mode

HALT mode will exit when the same bit of both **IF** and **IE** are set, regardless of the status of **IME**. The difference is that **IME** being enabled will cause the CPU to jump to the interrupt vector (and clear the **IF** flag), but with **IME** disabled the CPU will still continue executing, but **IF** won't be cleared.

# HRAM

From `$FF80` to `$FFFE`? Can only be allocated with **DS** of course, but is this range correct for even GBC? Might need to investigate. That range is 126 bytes.

# Calling convention

I suppose it might make sense to use some of HRAM as parameters to functions,
particularly there could be a standard set for leaf functions.
