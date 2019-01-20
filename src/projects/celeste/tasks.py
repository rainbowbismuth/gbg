from pathlib import Path
from invoke import task

def read_section(section):
    content = Path('celeste.txt').read_text().strip()
    found = False
    section = '__' + section + '__'
    for line in content.split('\n'):
        if line != section and line.startswith('__'):
            found = False
        if found:
            yield line
        if line == section:
            found = True

BYTES_PER_TILE = 16
COLORS_PER_SPRITE = 4
PIXELS_PER_LINE = 128

def select_gfx_tile(data, idx):
    add_x = (idx & 0x0F) * 8
    add_y = ((idx & 0xF0) >> 4) * 8

    output = []
    for y in range(8):
        line = []
        for x in range(8):
            s_idx = (y + add_y) * PIXELS_PER_LINE + (x + add_x)
            line.append(data[s_idx])
        output.append(''.join(line))
    return ''.join(output)

@task
def print_tile(c, idx):
    idx = int(idx)
    data = ''.join(read_section('gfx'))
    print(select_gfx_tile(data, idx))

@task
def print_palette(c, idx):
    idx = int(idx)
    data = ''.join(read_section('gfx'))
    print(set(select_gfx_tile(data, idx)))


@task
def print_section(c, name):
    for line in read_section(name):
        print(line)
