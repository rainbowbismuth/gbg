# sdcc

I tried this a little bit (didn't save any of the code), and it worked fine, and it could even generate RGBDS assembly, so the output was easy to read, but there was just not a lot of options for the code generation, and I couldn't get it to generate anything really reasonable..

# my own cc?

I'm inspired by this paper I read a long time ago called [PICOBIT](http://www.iro.umontreal.ca/~feeley/papers/StAmourFeeleyIFL09.pdf), which is a Scheme for micro-controllers. The main idea that was new to me at the time was using a language like C, but having a special compiler that enforced a restriction of no-recursion, not even mutual recursion. When you combine that property with whole program optimization you have a complete, static, acyclic call tree, and no longer need to use a stack to store arguments or local variables. Not only that but you can essentially do register allocation on every variable in the program.

I think if you were to write a C compiler for the Sharp this would be the way to go. It just seems out there to try to use the stack in a traditional C compiler way.
