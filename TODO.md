# Project

* I'm using a modified version of `sameboy_tester`, I should include that in this repo, and put my modification on github

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

# Code

* Shuffle out some sort of minimal initialization routines
* Same with hardware definition files
* Small test harness code (see `notes/testing.md`)
* Start code for instrument in it's own location
