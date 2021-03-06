from pathlib import Path
from invoke import task, call

CC = 'clang'

HERE = Path('.')
HOME = Path.home()

GFX = HERE / 'gfx'
SRC = HERE / 'src'
OUT = HERE / 'out'
COMMON = SRC / 'common'
PROJECTS = SRC / 'projects'

GAMBATTE = HOME / 'workspace/gambatte/gambatte_sdl/gambatte_sdl'
BGB = HOME / 'workspace/bgb/bgb.exe'
EMSFLASHER = HOME / 'workspace/ems-flasher/ems-flasher'
SAMEBOY_TESTER = HERE / 'SameBoy/build/bin/tester/sameboy_tester'


@task
def clean(c):
    c.run('rm -r out')


@task
def build_sameboy(c):
    c.run('make -s -C SameBoy tester')
    c.run('mkdir -p out/SameBoy')
    c.run(f'{CC} -shared -o out/SameBoy/sameboy.so SameBoy/build/obj/Core/*.o')


@task(pre=[build_sameboy])
def test_sameboy(c):
    c.run('python3 tooling/sameboy.py')


@task
def build_gfx_2bpp(c, image):
    image = Path(image)
    out = image.with_suffix('.2bpp')
    c.run(f"rgbgfx -o {OUT / out} {image}")


@task
def build_gfx(c, name):
    in_dir = GFX / name
    c.run(f"mkdir -p {OUT / in_dir}")
    for image in in_dir.glob('**/*.png'):
        build_gfx_2bpp(c, image)


@task(pre=[call(build_gfx, 'common')])
def build_project(c, name):
    out_dir = OUT / name
    in_dir = PROJECTS / name

    c.run(f"mkdir -p {out_dir}")
    c.run(f"rgbasm -o {out_dir / 'main.o'} -i {COMMON}/ -i {in_dir}/ -i {OUT}/ {in_dir / 'main.asm'}")
    c.run(f"rgblink -m {out_dir / name}.map -n {out_dir / name}.sym -o {out_dir / name}.gb {out_dir / 'main.o'}")
    c.run(f"rgbfix -v -p0 {out_dir / name}.gb")


@task
def sameboy_tester(c, name):
    c.run(f'{SAMEBOY_TESTER} --save {OUT / name / name}.gb')
    project_log = (OUT / name / name).with_suffix('.log')
    if not project_log.exists():
        print('sameboy_tester did not generate an {}'.format(project.log))

    if project_log.exists():
        contents = project_log.read_text()
        if 'The game is deadlocked' in contents:
            pass

        if 'Game probably stuck with blank screen' in contents:
            pass

    project_sav = (OUT / name / name).with_suffix('.sav')
    if not project_sav.exists():
        print("sameboy_tester didn't write .sav")

    from tooling.sav_check import sav_check
    sav_check(c, OUT, name)


@task
def gambatte(c, name):
    project_gb = (OUT / name / name).with_suffix('.gb')
    c.run(f'{GAMBATTE} {project_gb}')


@task
def bgb(c, name):
    project_gb = (OUT / name / name).with_suffix('.gb')
    c.run(f'wine {BGB} {project_gb}')


@task
def flash(c, name):
    project_gb = (OUT / name / name).with_suffix('.gb')
    c.run(f'{EMSFLASHER} --page 1 --format')
    c.run(f'{EMSFLASHER} --page 1 --write {project_gb}')


@task
def render_frames(c, rom, frames, offset=0, frameskip=1):
    from tooling import sameboy
    from tqdm import tqdm

    frames = int(frames)
    offset = int(offset)
    frameskip = int(frameskip)

    c.run('mkdir -p rendered')

    gb = sameboy.SameBoy(sameboy.GB_MODEL_DMG_B)
    gb.load_rom(rom)

    gb.set_rendering_disabled(True)
    for _ in range(offset):
        gb.run_frame()

    gb.set_rendering_disabled(False)
    for x in tqdm(range(offset, offset + frames)):
        gb.run_frame()
        if x % frameskip != 0:
            continue
        gb.save_screenshot(f'rendered/frame_{str(x).zfill(6)}.png')

    gb.free()


@task
def format_python(c):
    c.run('autopep8 -i **/*.py')
