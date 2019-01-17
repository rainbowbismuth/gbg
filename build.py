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
PARSER.add_argument('project')
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


def build_project(project):
    run('mkdir', '-p', project.out_dir)

    run('rgbasm',
        '-o', project.obj,
        '-i', str(COMMON) + '/',
        '-i', str(project.src_dir) + '/',
        project.main)

    run('rgblink',
        '-m', project.map,
        '-n', project.sym,
        '-o', project.gb,
        project.obj)

    run('rgbfix', '-v', '-p0', project.gb)


def sameboy_test(project):
    run(SAMEBOY_TESTER, project.gb, capture_output=True)
    if not project.log.exists():
        print('sameboy_tester did not generate an {}'.format(project.log))

    if project.log.exists():
        contents = project.log.read_text()
        if 'The game is deadlocked' in contents:
            print("gameboy deadlocked")

        if 'Game probably stuck with blank screen' in contents:
            print("gameboy blank screen")

    if project.bmp.exists():
        run('open', project.bmp)


def gambatte(project):
    run(GAMBATTE, project.gb, capture_output=True)


def emsflash(project):
    run(EMSFLASHER, '--page', '1', '--format')
    run(EMSFLASHER, '--page', '1', '--write', project.gb)


def main():
    for gfx in GFX.iterdir():
        build_gfx(gfx.name)

    project = Project(ARGS.project)
    run('rm', '-r', project.out_dir)
    build_project(project)

    if ARGS.test:
        sameboy_test(project)

    if ARGS.run:
        gambatte(project)

    if ARGS.flash:
        emsflash(project)


class Project:
    def __init__(self, name):
        self.name = name

    @property
    def src_dir(self):
        return PROJECTS / self.name

    @property
    def main(self):
        return self.src_dir / 'main.asm'

    @property
    def out_dir(self):
        return OUT / self.name

    def out_file(self, suffix):
        return (self.out_dir / self.name).with_suffix(suffix)

    @property
    def gb(self):
        return self.out_file('.gb')

    @property
    def log(self):
        return self.out_file('.log')

    @property
    def obj(self):
        return self.out_file('.obj')

    @property
    def map(self):
        return self.out_file('.map')

    @property
    def sym(self):
        return self.out_file('.sym')

    @property
    def bmp(self):
        return self.out_file('.bmp')


if __name__ == '__main__':
    try:
        main()
    except subprocess.CalledProcessError as e:
        pass
