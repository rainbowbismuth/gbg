import ctypes
from pathlib import Path

# built with a `clang -shared -o shared.so *.o` in Core
_sameboy = ctypes.cdll.LoadLibrary('SameBoy/build/obj/Core/shared.so')

GB_MODEL_DMG_B = 0x002
GB_MODEL_CGB_C = 0x203

# typedef void (*GB_vblank_callback_t)(GB_gameboy_t *gb);
# typedef void (*GB_log_callback_t)(GB_gameboy_t *gb, const char *string, GB_log_attributes attributes);
# typedef char *(*GB_input_callback_t)(GB_gameboy_t *gb);
# typedef void (*GB_infrared_callback_t)(GB_gameboy_t *gb, bool on, long cycles_since_last_update);
# typedef void (*GB_rumble_callback_t)(GB_gameboy_t *gb, bool rumble_on);
# typedef void (*GB_serial_transfer_start_callback_t)(GB_gameboy_t *gb, uint8_t byte_to_send);
# typedef uint8_t (*GB_serial_transfer_end_callback_t)(GB_gameboy_t *gb);

# TODO: Honestly should just write some C with default versions of these..
#  I mean, a callback across ctypes just to encode rgb ????
GB_rgb_encode_callback = ctypes.CFUNCTYPE(
    ctypes.c_uint32, ctypes.c_void_p, ctypes.c_uint8, ctypes.c_uint8, ctypes.c_uint8)

class GB:
    def __init__(self, model=GB_MODEL_CGB_C):
        self.memory = ctypes.create_string_buffer(0xF000)
        self.rgb_callback = None
        _sameboy.GB_init(self.memory, model)

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
        self.rgb_callback = None

    def is_inited(self):
        self._assert_memory()
        return _sameboy.GB_is_inited(self.memory)

    def load_boot_rom(self, path):
        self._assert_memory()
        res = _sameboy.GB_load_boot_rom(self.memory, path)

    def load_rom(self, path):
        self._assert_memory()
        res = _sameboy.GB_load_rom(self.memory, path)

    def run(self):
        self._assert_memory()
        return _sameboy.GB_run(self.memory)

    def run_frame(self):
        self._assert_memory()
        return _sameboy.GB_run_frame(self.memory)

    def save_battery(self, path):
        self._assert_memory()
        return _sameboy.GB_save_battery(self.memory, path)

    def read_memory(self, addr):
        self._assert_memory()
        return _sameboy.GB_read_memory(self.memory, addr)

    def set_rgb_encode_callback(self, callback):
        self._assert_memory()
        self.rgb_callback = GB_rgb_encode_callback(lambda _, r, g, b: callback(self,r,g,b))
        _sameboy.GB_set_rgb_encode_callback(self.memory, self.rgb_callback)

if __name__ == '__main__':
    gb = GB(GB_MODEL_CGB_C)
    assert(gb.is_inited())
    gb.load_boot_rom('./SameBoy/build/bin/BootROMs/cgb_boot.bin')
    gb.load_rom('./out/testing/testing.gb')

    gb.set_rgb_encode_callback(lambda gb,r,g,b: r<<24 | g<<16 | b<<8)

    for _ in range(5):
        # Crashes here because apperantly callbacks are a necessary part
        # of the API, see initialization in `Tester/main.c`...
        gb.run_frame()
    print(f"0x{gb.read_memory(0xFF44):X}")
    gb.free()
