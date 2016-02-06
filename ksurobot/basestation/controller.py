from textwrap import dedent
import sys
from time import sleep
import sdl2
from math import isclose


class LowController(object):
    def __init__(self, number):
        self.device = sdl2.joystick.SDL_JoystickOpen(number)
        assert sdl2.haptic.SDL_JoystickIsHaptic(self.device)
        self.haptic = sdl2.haptic.SDL_HapticOpenFromJoystick(self.device)
        sdl2.haptic.SDL_HapticRumbleInit(self.haptic)

    def update(self):
        sdl2.SDL_JoystickUpdate()

    def get_name(self):
        return sdl2.joystick.SDL_JoystickName(self.device)

    def get_a(self):
        return sdl2.joystick.SDL_JoystickGetButton(self.device, 0)

    def get_b(self):
        return sdl2.joystick.SDL_JoystickGetButton(self.device, 1)

    def get_x(self):
        return sdl2.joystick.SDL_JoystickGetButton(self.device, 2)

    def get_y(self):
        return sdl2.joystick.SDL_JoystickGetButton(self.device, 3)

    def get_dpad(self):
        return sdl2.joystick.SDL_JoystickGetHat(self.device, 0)

    def get_start(self):
        return sdl2.joystick.SDL_JoystickGetButton(self.device, 6)

    def get_select(self):
        return sdl2.joystick.SDL_JoystickGetButton(self.device, 7)

    def get_center(self):
        return sdl2.joystick.SDL_JoystickGetButton(self.device, 8)

    def get_left_x(self):
        return sdl2.joystick.SDL_JoystickGetAxis(self.device, 0)

    def get_left_y(self):
        return sdl2.joystick.SDL_JoystickGetAxis(self.device, 1)

    def get_left_trigger(self):
        return sdl2.joystick.SDL_JoystickGetAxis(self.device, 2)

    def get_left_bumper(self):
        return sdl2.joystick.SDL_JoystickGetButton(self.device, 4)

    def get_left_stick(self):
        return sdl2.joystick.SDL_JoystickGetButton(self.device, 9)

    def get_right_x(self):
        return sdl2.joystick.SDL_JoystickGetAxis(self.device, 3)

    def get_right_y(self):
        return sdl2.joystick.SDL_JoystickGetAxis(self.device, 4)

    def get_right_trigger(self):
        return sdl2.joystick.SDL_JoystickGetAxis(self.device, 5)

    def get_right_bumper(self):
        return sdl2.joystick.SDL_JoystickGetButton(self.device, 5)

    def get_right_stick(self):
        return sdl2.joystick.SDL_JoystickGetButton(self.device, 10)

    def set_haptic(self, time, mag=1):
        sdl2.haptic.SDL_HapticRumblePlay(self.haptic, mag, time)

    def formatted_state(self):
        a = """
        right (x, y, trigger) : {rx:6}, {ry:6}, {rt:6}
        left (x, y, trigger)  : {lx:6}, {ly:6}, {lt:6}
        dpad, bumpers (l, r)  : {dpad:2}, {lb}, {rb}
        sticks (l, r)         : {ls}, {rs}
        start, select, center : {start}, {select}, {center}
        a, b, x, y            : {a}, {b}, {x}, {y}
        """
        a = dedent(a).strip()

        b = a.format(
            rx=self.get_right_x(),
            ry=self.get_right_y(),
            rt=self.get_right_trigger(),
            rs=self.get_right_stick(),
            lx=self.get_left_x(),
            ly=self.get_left_y(),
            lt=self.get_left_trigger(),
            ls=self.get_left_stick(),
            dpad=self.get_dpad(),
            a=self.get_a(),
            b=self.get_b(),
            x=self.get_x(),
            y=self.get_y(),
            rb=self.get_right_bumper(),
            lb=self.get_left_bumper(),
            start=self.get_start(),
            select=self.get_select(),
            center=self.get_center()
        )
        return b

    @classmethod
    def init(cls):
        sdl2.SDL_Init(sdl2.SDL_INIT_JOYSTICK | sdl2.SDL_INIT_HAPTIC)

    @classmethod
    def number_controllers(self):
        return sdl2.joystick.SDL_NumJoysticks()


class HatFixer(object):
    def fix(self, value):
        if value & 1:
            result = 'u'
        elif value & 4:
            result = 'd'
        else:
            result = ' '

        if value & 2:
            result += 'r'
        elif value & 8:
            result += 'l'
        else:
            result += ' '

        return result

    def zero(self, value):
        pass


class TriggerFixer(object):
    VAR_MAX = 32767
    VAR_MIN = -32768

    def fix(self, value):
        return (value - self.VAR_MIN) / (self.VAR_MAX - self.VAR_MIN)

    def zero(self, value):
        pass

class AxisFixer(object):
    VAR_MAX = 32767
    VAR_MIN = -32768

    def __init__(self):
        self.zero_value = 0

    def zero(self, current):
        self.zero_value = current

    def fix(self, value):
        normal = value - self.zero_value
        if value > 0:
            normal = normal / (self.VAR_MAX - self.zero_value)
        else:
            normal = -normal / (self.VAR_MIN - self.zero_value)

        if isclose(normal, 0, abs_tol=0.03):
            return 0
        return normal


def create_fixer_map():
    return {
        'get_dpad': HatFixer(),
        'get_right_x': AxisFixer(),
        'get_right_y': AxisFixer(),
        'get_right_trigger': TriggerFixer(),
        'get_left_x': AxisFixer(),
        'get_left_y': AxisFixer(),
        'get_left_trigger': TriggerFixer(),
    }


class Controller(LowController):
    def __init__(self, number):
        super().__init__(number)
        self._fixer_map = None
        self.fix_controller(create_fixer_map())
        self.zero()

    def fix_controller(self, mapping):
        self._fixer_map = mapping
        for k, v in mapping.items():
            assert hasattr(self, k)
            setattr(self, k, self._shim_of(k, v))

    def zero(self):
        for k, v in self._fixer_map.items():
            v.zero(getattr(super(), k)())

    def _shim_of(self, func, fixer):
        super_ = super()

        return lambda: fixer.fix(getattr(super_, func)())
