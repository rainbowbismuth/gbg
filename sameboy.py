import ctypes
from pathlib import Path

# built with a `clang -shared -o shared.so *.o` in Core
_sameboy = ctypes.cdll.LoadLibrary('SameBoy/build/obj/Core/shared.so')

GB_MODEL_DMG_B = 0x002
GB_MODEL_CGB_C = 0x203


# typedef void (*GB_infrared_callback_t)(GB_gameboy_t *gb, bool on, long cycles_since_last_update);
# typedef void (*GB_rumble_callback_t)(GB_gameboy_t *gb, bool rumble_on);
# typedef void (*GB_serial_transfer_start_callback_t)(GB_gameboy_t *gb, uint8_t byte_to_send);
# typedef uint8_t (*GB_serial_transfer_end_callback_t)(GB_gameboy_t *gb);

# Not sure if this is necessary for us..
GB_input_callback = ctypes.CFUNCTYPE(
    ctypes.c_char_p, ctypes.c_void_p)

GB_vblank_callback = ctypes.CFUNCTYPE(
    None, ctypes.c_void_p)

GB_log_callback = ctypes.CFUNCTYPE(
    None, ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int)

# TODO: Honestly should just write some C with default versions of these..
#  I mean, a callback across ctypes just to encode rgb ????
GB_rgb_encode_callback = ctypes.CFUNCTYPE(
    ctypes.c_uint32, ctypes.c_void_p, ctypes.c_uint8, ctypes.c_uint8, ctypes.c_uint8)


BMP_HEADER = bytes([0x42, 0x4D, 0x48, 0x68, 0x01, 0x00, 0x00, 0x00,
0x00, 0x00, 0x46, 0x00, 0x00, 0x00, 0x38, 0x00,
0x00, 0x00, 0xA0, 0x00, 0x00, 0x00, 0x70, 0xFF,
0xFF, 0xFF, 0x01, 0x00, 0x20, 0x00, 0x03, 0x00,
0x00, 0x00, 0x02, 0x68, 0x01, 0x00, 0x12, 0x0B,
0x00, 0x00, 0x12, 0x0B, 0x00, 0x00, 0x00, 0x00,
0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
0x00, 0xFF, 0x00, 0x00, 0xFF, 0x00, 0x00, 0xFF,
0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

class GB:
    def __init__(self, model=GB_MODEL_CGB_C):
        self.memory = ctypes.create_string_buffer(0xF000)
        self.screen = ctypes.create_string_buffer(4*160*144)
        _sameboy.GB_init(self.memory, model)
        _sameboy.GB_set_pixels_output(self.memory, self.screen)

    def __del__(self):
        if not self.memory:
            return
        self.free()

    def _assert_memory(self):
        assert(self.memory is not None)

    def free(self):
        self._assert_memory()
        _sameboy.GB_free(self.memory)
        self.memory = None
        self.input_callback = None
        self.vblank_callback = None
        self.rgb_callback = None
        self.log_callback = None

    def is_inited(self):
        self._assert_memory()
        return _sameboy.GB_is_inited(self.memory)

    def load_boot_rom(self, path):
        self._assert_memory()
        path = str(Path(path).resolve())
        print(path)
        res = _sameboy.GB_load_boot_rom(self.memory, path)
        if res:
            raise Exception("Error loading boot ROM at {}".format(path))

    def load_rom(self, path):
        self._assert_memory()
        path = str(Path(path).resolve())
        res = _sameboy.GB_load_rom(self.memory, path)
        if res:
            raise Exception("Error loading ROM {}".format(path))

    def run(self):
        self._assert_memory()
        return _sameboy.GB_run(self.memory)

    def run_frame(self):
        self._assert_memory()
        return _sameboy.GB_run_frame(self.memory)

    def reset(self):
        self._assert_memory()
        return _sameboy.GB_reset(self.memory)

    def save_battery(self, path):
        self._assert_memory()
        path = str(Path(path).resolve())
        res = _sameboy.GB_save_battery(self.memory, path)
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

    def set_vblank_callback(self, callback):
        self._assert_memory()
        self.vblank_callback = GB_vblank_callback(lambda _: callback(self))
        _sameboy.GB_set_vblank_callback(self.memory, self.vblank_callback)

    def set_rgb_encode_callback(self, callback):
        self._assert_memory()
        self.rgb_callback = GB_rgb_encode_callback(lambda _, r, g, b: callback(self,r,g,b))
        _sameboy.GB_set_rgb_encode_callback(self.memory, self.rgb_callback)

    def set_log_callback(self, callback):
        self._assert_memory()
        self.log_callback = GB_log_callback(lambda _, s, a: callback(self, s, a))
        _sameboy.GB_set_log_callback(self.memory, self.log_callback)

    def save_screenshot(self, path):
        with open(path, 'wb') as f:
            f.write(BMP_HEADER)
            f.write(self.screen.raw)


if __name__ == '__main__':
    remaining = 10
    def limited_logger(gb, s, attr):
        global remaining
        if not remaining:
            return
        remaining -= 1
        print(s.decode('utf-8'))


    # gb = GB(GB_MODEL_DMG_B)
    gb = GB(GB_MODEL_CGB_C)

    # gb.load_boot_rom('SameBoy/build/bin/tester/dmg_boot.bin')
    gb.load_boot_rom('SameBoy/build/bin/tester/cgb_boot.bin')

    # default callbacks
    gb.set_vblank_callback(lambda gb: 0)
    gb.set_rgb_encode_callback(lambda gb,r,g,b: (r<<24) | (g<<16) | (b<<8))
    gb.set_log_callback(limited_logger)
    gb.set_input_callback(lambda gb: None)

    # gb.load_rom('./out/instrument/instrument.gb')
    # gb.load_rom('./out/testing/testing.gb')
    gb.load_rom('extra_roms/pocket.gb')

    # gb.set_rendering_disabled(True)
    for _ in range(60*40):
       gb.run_frame()

    # gb.set_rendering_disabled(False)
    gb.run_frame()

    gb.save_screenshot('test.bmp')
    # gb.save_battery('./testing.sav')

    gb.free()
