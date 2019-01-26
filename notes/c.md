# sdcc

I tried this a little bit (didn't save any of the code), and it worked fine, and it could even generate RGBDS assembly, so the output was easy to read, but there was just not a lot of options for the code generation, and I couldn't get it to generate anything really reasonable..

# my own cc?

I'm inspired by this paper I read a long time ago called [PICOBIT](http://www.iro.umontreal.ca/~feeley/papers/StAmourFeeleyIFL09.pdf), which is a Scheme for micro-controllers. The main idea that was new to me at the time was using a language like C, but having a special compiler that enforced a restriction of no-recursion, not even mutual recursion. When you combine that property with whole program optimization you have a complete, static, acyclic call tree, and no longer need to use a stack to store arguments or local variables. Not only that but you can essentially do register allocation on every variable in the program.

I think if you were to write a C compiler for the Sharp this would be the way to go. It just seems out there to try to use the stack in a traditional C compiler way.

# ddcg

There's another paper I ran into today on [Destination Driven Code Generation](https://www.cs.indiana.edu/~dyb/pubs/ddcg.pdf) and some [slides](http://cs.au.dk/~mis/dOvs/slides/46b-codegeneration-in-V8.pdf) which looked super fascinating. Now the code generator certainly wouldn't have to be single-pass, but the ideas really made it a lot clearer how you might generate code for an architecture like the gameboy's, where so many instructions only work with certain registers (like the accumulator). I spent some time imagining how you might get from `*pointer++` like code to `ld a, [hl+]` like instructions, and it occurred to me that you might want a bottom up pass where operations can tell you where they *want* their data to live. Then on the way back down, the code generator tries to provide for that, and then each operation says what it *needs* and functions like `pick()` do the work of matching these up if necessary.

Once you get to the top of the function with those 'wants' though, that can be what determines the calling convention for the function. Since we would be doing whole program optimization, each function (as long as its not through a function pointer) can have its own calling convention, and these 'wants' can determine where each argument goes.
