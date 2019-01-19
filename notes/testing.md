# Automated testing

I have a couple of ideas here.. I think my first one is simply because able to
run a cart, and have it write testing results to the *.sav* file, which should be
very easy to automatically check.

`sameboy_tester` also happens to write out a screenshot of the last frame. So
it might be possible to do comparisons here for graphics. The source code for
the test is pretty straightforward, so it might be possible to extend it with
additional checks.

It also has a built-in early exit on a deadlock which it logs. So it might be
useful to use that.

# Python

So now that I'm writing a Python API for SameBoy, I have some additional ideas..

* The testing framework needs to know how to build ROMs, *or* the testing main function in the cart should jump to a location we can write ourselves from python. Since we generate a symbol map we should be able to look up every symbol that starts with 'unittest' perhaps, and then reset the gameboy over and over again. Still need to add the halt detection, then I could do a 'run-until-deadlock or X cycles' like function.

* It would be good if I could easily jump in with the debugger too.
