# Build

* Structure for generating multiple ROMs
* Include testing framework
* Re-arrange files like `projects/instrument/src` & `common/src`?
* Should allow for having a `test` dir per project? idk

# Testing

* SameBoy tester.c hack for `.sav` was a success, but...
* Really I want to just be asking, read arbitrary addrs & check?
* What would be an easy way to specify that?
* Using `.sav` for a testing framework is nice until you want to test your saving code I suppose :P
* Actually I have a much better idea, I could use a byte or two of memory as a register to talk to SameBoy, and then single step it in the tester???
* Could read `.map` file for test_framework section info to control testing exec
* Writing a ctypes wrapper at the moment, to write the testing code in Python
* Imagine being able to check invariants every frame?

# Profiling

* SameBoy should be able to give us a cycle number?

# Code

* Shuffle out some sort of minimal initialization routines
* Same with hardware definition files
* Small test harness code (see `notes/testing.md`)
