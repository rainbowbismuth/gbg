#!/bin/sh
GBPATH=$HOME/workspace/gambatte/gambatte_sdl/gambatte_sdl
EMSFLASHER=$HOME/workspace/ems-flasher/ems-flasher
SAMEBOY_TESTER=$HOME/workspace/SameBoy/build/bin/tester/sameboy_tester

rm -r out/*
mkdir -p out/gfx

rgbgfx -o out/gfx/potash.2bpp gfx/potash.png

rgbasm -o out/game.obj -i src/ src/main.asm
rgblink -m out/game.map -n out/game.sym -o out/game.gb out/game.obj
rgbfix -v -p0 out/game.gb

while getopts "rft" opt; do
    case "$opt" in
    r)
        $GBPATH out/game.gb &> /dev/null &
        ;;
    f)
        $EMSFLASHER --page 1 --format
        $EMSFLASHER --page 1 --write out/game.gb
        ;;
    t)
        $SAMEBOY_TESTER out/game.gb &> /dev/null
        if [ -f out/game.log ]
        then
          cat out/game.log
        fi
        if [ -f out/game.bmp ]
        then
          open out/game.bmp
        fi
        ;;
    esac
done
