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
