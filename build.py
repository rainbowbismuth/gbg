#!/usr/bin/env python3

import glob
import subprocess
import argparse
from pathlib import Path

HERE = Path('.')
HOME = Path.home()

GFX = HERE / 'gfx'
SRC = HERE / 'src'
OUT = HERE / 'out'
COMMON = SRC / 'common'
PROJECTS = SRC / 'projects'

GAMBATTE = HOME / 'workspace/gambatte/gambatte_sdl/gambatte_sdl'
EMSFLASHER = HOME / 'workspace/ems-flasher/ems-flasher'
SAMEBOY_TESTER = HOME / 'workspace/SameBoy/build/bin/tester/sameboy_tester'

PARSER = argparse.ArgumentParser()
PARSER.add_argument('-v', '--verbose', action='store_true')
PARSER.add_argument('-r', '--run', action='store_true', help='run with gambatte')
PARSER.add_argument('-f', '--flash', action='store_true', help='flash with emsflasher')
PARSER.add_argument('-t', '--test', action='store_true', help='test with sameboy_tester')
PARSER.add_argument('project', nargs='?')
ARGS = PARSER.parse_args()


def run(*args, **kwargs):
    if ARGS.verbose:
        print(' '.join([str(arg) for arg in args]))
    return subprocess.run(args, check=True, **kwargs)


def build_gfx(name):
    in_dir = GFX / name
    run('mkdir', '-p', OUT / in_dir)
    for image in in_dir.glob('**/*.png'):
        out_file = image.with_suffix('.2bpp')
        run('rgbgfx', '-o', OUT / out_file, image)


def build_project(name):
    out_dir = OUT / name

    run('mkdir', '-p', out_dir)

    project_dir = PROJECTS / name
    main_file =  project_dir / 'main.asm'
    obj_file = out_dir / (name + '.obj')
    map_file = out_dir / (name + '.map')
    sym_file = out_dir / (name + '.sym')
    gb_file = out_dir / (name + '.gb')

    run('rgbasm',
        '-o', obj_file,
        '-i', str(COMMON) + '/',
        '-i', str(project_dir) + '/',
        main_file)
        
    run('rgblink', '-m', map_file, '-n', sym_file, '-o', gb_file, obj_file)
    run('rgbfix', '-v', '-p0', gb_file)


def main():
    run('rm', '-r', OUT)

    for gfx in GFX.iterdir():
        build_gfx(gfx.name)

    if ARGS.project:
        build_project(ARGS.project)
    else:
        for project in PROJECTS.iterdir():
            build_project(project.name)

    if ARGS.project:
        gb = OUT / ARGS.project / (ARGS.project + '.gb')

        if ARGS.test:
            run(SAMEBOY_TESTER, gb, capture_output=True)

        if ARGS.run:
            run(GAMBATTE, gb, capture_output=True)

        if ARGS.flash:
            run(EMSFLASHER, '--page', '1', '--format')
            run(EMSFLASHER, '--page', '1', '--write', gb)


if __name__ == '__main__':
    try:
        main()
    except subprocess.CalledProcessError as e:
        pass
