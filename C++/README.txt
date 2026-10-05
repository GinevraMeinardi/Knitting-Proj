README file for knitting proj in C++

from the cmd prompt:
to move to the F disk
- F: 
- cd to/your/path

g++ -std=c++20 Shape.cxx Swatch.cxx Test.C -o knit_calculator.exe
knit_calculator.exe

Using Makefile:
make
knit_calculator.exe
or use "make run"


// how to install Makefile
in MSYS2 MINGW64 terminal:
- pacman -S mingw-w64-x86_64-make
- cp /mingw64/bin/mingw32-make.exe /mingw64/bin/make.exe
then in cmd:
- make --version