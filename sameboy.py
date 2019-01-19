import ctypes
from pathlib import Path
from PIL import Image

# built with a `clang -shared -o shared.so *.o` in Core
_sameboy = ctypes.cdll.LoadLibrary('SameBoy/build/obj/Core/shared.so')

GB_MODEL_DMG_B = 0x002
GB_MODEL_CGB_C = 0x203

# typedef void (*GB_infrared_callback_t)(GB_gameboy_t *gb, bool on, long cycles_since_last_update);
# typedef void (*GB_rumble_callback_t)(GB_gameboy_t *gb, bool rumble_on);
# typedef void (*GB_serial_transfer_start_callback_t)(GB_gameboy_t *gb, uint8_t byte_to_send);
# typedef uint8_t (*GB_serial_transfer_end_callback_t)(GB_gameboy_t *gb);

# Not sure if this is necessary for us..
GB_input_callback = ctypes.CFUNCTYPE(ctypes.c_char_p, ctypes.c_void_p)

GB_vblank_callback = ctypes.CFUNCTYPE(None, ctypes.c_void_p)

GB_log_callback = ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_char_p,
                                   ctypes.c_int)

GB_rgb_encode_callback = ctypes.CFUNCTYPE(ctypes.c_uint32, ctypes.c_void_p,
                                          ctypes.c_uint8, ctypes.c_uint8,
                                          ctypes.c_uint8)


def default_rgb_encode_callback(gb, r, g, b):
    return 0xFF000000 | (r << 16) | (g << 8) | b


def default_vblank_callback(gb):
    return None


def default_log_callback(gb, msg, attr):
    return None


def default_input_callback(gb):
    return None


# TODO: Add context manager?
class GB:
    def __init__(self, model=GB_MODEL_CGB_C):
        self.memory = ctypes.create_string_buffer(0xF000)
        _sameboy.GB_init(self.memory, model)
        width = self.get_screen_width()
        height = self.get_screen_height()
        self.screen = ctypes.create_string_buffer(4 * width * height)
        _sameboy.GB_set_pixels_output(self.memory, self.screen)
        self.set_rgb_encode_callback(default_rgb_encode_callback)
        self.set_vblank_callback(default_vblank_callback)
        self.set_log_callback(default_log_callback)
        self.set_input_callback(default_input_callback)

    def __del__(self):
        if not self.memory:
            return
        self.free()

    def _assert_memory(self):
        assert (self.memory is not None)

    def free(self):
        self._assert_memory()
        _sameboy.GB_free(self.memory)
        self.memory = None
        self.input_callback = None
        self.async_input_callback = None
        self.vblank_callback = None
        self.rgb_callback = None
        self.log_callback = None

    def is_inited(self):
        self._assert_memory()
        return _sameboy.GB_is_inited(self.memory)

    def get_screen_width(self):
        self._assert_memory()
        return _sameboy.GB_get_screen_width(self.memory)

    def get_screen_height(self):
        self._assert_memory()
        return _sameboy.GB_get_screen_height(self.memory)

    def _encode_path(self, path):
        return str(Path(path).resolve()).encode('utf-8')

    def load_boot_rom(self, path):
        self._assert_memory()
        res = _sameboy.GB_load_boot_rom(self.memory, self._encode_path(path))
        if res:
            raise Exception("Error loading boot ROM at {}".format(path))

    def load_boot_rom_from_bytes(self, bytes):
        self._assert_memory()
        _sameboy.GB_load_boot_rom_from_buffer(self.memory, bytes, len(bytes))

    def load_rom(self, path):
        self._assert_memory()
        res = _sameboy.GB_load_rom(self.memory, self._encode_path(path))
        if res:
            raise Exception("Error loading ROM {}".format(path))

    def run(self):
        self._assert_memory()
        return _sameboy.GB_run(self.memory)

    def run_frame(self):
        self._assert_memory()
        return _sameboy.GB_run_frame(self.memory)

    def debugger_set_disabled(self, disabled=True):
        self._assert_memory()
        _sameboy.GB_debugger_set_disabled(self.memory, disabled)

    def debugger_break(self):
        self._assert_memory()
        _sameboy.GB_debugger_break(self.memory)

    def reset(self):
        self._assert_memory()
        return _sameboy.GB_reset(self.memory)

    def save_battery(self, path):
        self._assert_memory()
        res = _sameboy.GB_save_battery(self.memory, self._encode_path(path))
        if res:
            raise Exception("Error saving battery at {}".format(path))

    def read_memory(self, addr):
        self._assert_memory()
        return _sameboy.GB_read_memory(self.memory, addr)

    def set_rendering_disabled(self, disabled=True):
        self._assert_memory()
        return _sameboy.GB_set_rendering_disabled(self.memory, disabled)

    def set_input_callback(self, callback):
        self._assert_memory()
        self.input_callback = GB_input_callback(lambda _: callback(self))
        _sameboy.GB_set_input_callback(self.memory, self.input_callback)

    def set_async_input_callback(self, callback):
        self._assert_memory()
        self.async_input_callback = GB_input_callback(lambda _: callback(self))
        _sameboy.GB_set_async_input_callback(self.memory,
                                             self.async_input_callback)

    def set_vblank_callback(self, callback):
        self._assert_memory()
        self.vblank_callback = GB_vblank_callback(lambda _: callback(self))
        _sameboy.GB_set_vblank_callback(self.memory, self.vblank_callback)

    def set_rgb_encode_callback(self, callback):
        self._assert_memory()
        self.rgb_callback = GB_rgb_encode_callback(
            lambda _, r, g, b: callback(self, r, g, b))
        _sameboy.GB_set_rgb_encode_callback(self.memory, self.rgb_callback)

    def set_log_callback(self, callback):
        self._assert_memory()
        self.log_callback = GB_log_callback(
            lambda _, s, a: callback(self, s, a))
        _sameboy.GB_set_log_callback(self.memory, self.log_callback)

    def screen_to_image(self):
        (width, height) = self.get_screen_width(), self.get_screen_height()
        img = Image.frombytes('RGBA', (width, height), self.screen)
        return img

    def save_screenshot(self, path, format=None, **options):
        self.screen_to_image().save(path, format, **options)

    def memory_to_bytearray(self):
        # TODO: write a function in C that does this!
        mem = bytearray(0xFFFF + 1)
        for addr in range(0xFFFF + 1):
            mem[addr] = self.read_memory(addr)
        return mem

    def dump_memory(self, path):
        with open(path, 'wb') as f:
            f.write(self.memory_to_bytearray())


if __name__ == '__main__':
    gb = GB(GB_MODEL_DMG_B)
    # gb = GB(GB_MODEL_CGB_C)

    gb.load_boot_rom('SameBoy/build/bin/tester/dmg_boot.bin')
    # gb.load_boot_rom('SameBoy/build/bin/tester/cgb_boot.bin')

    # boot_rom = Path('SameBoy/build/bin/tester/dmg_boot.bin').read_bytes()
    # gb.load_boot_rom_from_bytes(boot_rom)

    gb.load_rom('out/instrument/instrument.gb')
    # gb.load_rom('./out/testing/testing.gb')
    # gb.load_rom('extra_roms/pocket.gb')

    # gb.dump_memory('test_before.mem')

    # gb.debugger_set_disabled(False)
    # gb.debugger_break()
    gb.set_rendering_disabled(True)
    for _ in range(60 * 40):
        gb.run_frame()

    # gb.dump_memory('test_after.mem')

    gb.set_rendering_disabled(False)
    gb.run_frame()

    gb.save_screenshot('test.png', optimize=True)
    # gb.save_battery('./testing.sav')

    gb.free()
