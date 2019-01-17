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
SAMEBOY_TESTER = HERE / 'SameBoy/build/bin/tester/sameboy_tester'

PARSER = argparse.ArgumentParser()
PARSER.add_argument('-v', '--verbose', action='store_true')
PARSER.add_argument('-r', '--run', action='store_true', help='run with gambatte')
PARSER.add_argument('-f', '--flash', action='store_true', help='flash with emsflasher')
PARSER.add_argument('-t', '--test', action='store_true', help='test with sameboy_tester')
PARSER.add_argument('project')
ARGS = PARSER.parse_args()

def rm(path):
    path = Path(path)
    if path.exists():
        run('rm', '-r', path)


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
    run(SAMEBOY_TESTER, '--save', project.gb, capture_output=True)
    if not project.log.exists():
        print('sameboy_tester did not generate an {}'.format(project.log))

    if project.log.exists():
        contents = project.log.read_text()
        if 'The game is deadlocked' in contents:
            pass

        if 'Game probably stuck with blank screen' in contents:
            pass

    #if project.bmp.exists():
    #    run('open', project.bmp)

    if not project.sav.exists():
        print("SameBoy didn't write .sav")
    sav_check(project)


def sav_check(project):
    # The protocol is that
    #  first byte = $FA
    #  second byte = $CE
    #  third byte is number of tests planned
    #  fourth byte is number of tests run
    # Followed by a byte per test where
    #  $00 = failure
    #  $01 = success
    # All other values should be $FF
    results = project.sav.read_bytes()

    if results[0] != 0xFA and results[1] != 0xCE:
        print("{} is not a test framework .sav".format(project.sav))
        return

    planned = results[2]
    ran = results[3]

    print("{} tests planned".format(planned))
    print("{} tests ran".format(ran))

    if ran > planned:
        print("more tests run then planned!")

    successes = 0
    failures = []
    unexpected = []
    unplanned = []
    for idx in range(4, len(results)):
        byte = results[idx]
        if ran and byte == 0:
            failures.append(idx-3)
            planned -= 1
        if ran and byte == 1:
            successes += 1
            planned -= 1
        if ran and byte > 1:
            unexpected.append((idx, byte))
        if not ran and byte != 0xFF:
            unexpected.append((idx, byte))
        ran = max(0, ran-1)

    print("{} successes".format(successes))
    if planned > 0:
        print("{} tests planned, but not executed!".format(planned))
    if failures:
        print("{} failures".format(len(failures)))
        print("caused by tests: {}".format(', '.join(map(str,failures))))
    if unexpected:
        # TODO: Print unexpected values instead of hexdump
        print("{} unexpected values\n".format(len(unexpected)))
        run('hexdump', project.sav)


def gambatte(project):
    run(GAMBATTE, project.gb, capture_output=True)


def emsflash(project):
    run(EMSFLASHER, '--page', '1', '--format')
    run(EMSFLASHER, '--page', '1', '--write', project.gb)


def main():
    for gfx in GFX.iterdir():
        build_gfx(gfx.name)

    project = Project(ARGS.project)

    rm(project.out_dir)
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

    @property
    def sav(self):
        return self.out_file('.sav')


if __name__ == '__main__':
    try:
        main()
    except subprocess.CalledProcessError as e:
        pass
