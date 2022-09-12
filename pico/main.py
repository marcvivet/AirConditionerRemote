from screen_driver import EPD
from framebuf_ex import FrameBufferEx
from fb_top_icons import TOP_ICONS
from fb_bottom_icons import BOTTOM_ICONS
from fb_fan import FAN
from fb_vane import VANE
from fb_numbers import NUMBERS

class DegreesNumbers:
    def __init__(self, screen_fb: FrameBufferEx, pos_x: int, pos_y: int):
        self._value = 0
        self._screen_fb = screen_fb
        self._pos_x = pos_x
        self._pos_y = pos_y

    def next(self):
        self.value = self._value + 1

    def prev(self):
        self.value = self._value - 1

    @property
    def value(self) -> int:
        return self._value

    @value.setter
    def value(self, number: int) -> None:
        self._value = number % 100
        str_number = '{:02}'.format(self._value)
        self._screen_fb.blit(NUMBERS[str_number[0]], self._pos_x, self._pos_y)
        self._screen_fb.blit(NUMBERS[str_number[1]], self._pos_x + 51, self._pos_y)

        self._screen_fb.blit(BOTTOM_ICONS['thermometer'], self._pos_x - 11, self._pos_y - 1)
        self._screen_fb.blit(BOTTOM_ICONS['celcius'], self._pos_x + 99, self._pos_y + 52)


class Icon:
    def __init__(self, fb: FrameBufferEx, screen_fb: FrameBufferEx, pos_x: int, pos_y: int):
        self._enabled = False
        self._screen_fb = screen_fb
        self._fb = fb
        self._pos_x = pos_x
        self._pos_y = pos_y

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, value: bool):
        if value:
            self.enable()
        else:
            self.disable()

    def enable(self):
        if not self._enabled:
            self._enabled = True
            self._screen_fb.blit(self._fb, self._pos_x, self._pos_y)

    def disable(self):
        if self._enabled:
            self._enabled = False
            self._screen_fb.fill_rect(self._pos_x, self._pos_y, self._fb.width, self._fb.height, 0)

    def toggle(self):
        if self._enabled:
            self.disable()
        else:
            self.enable()


class MultiIcons:
    def __init__(self, icons: list):
        self._enabled = False
        self._icons = icons

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, value: bool):
        if value:
            self.enable()
        else:
            self.disable()

    def enable(self):
        if not self._enabled:
            self._enabled = True
            for icon in self._icons:
                icon.enable()

    def disable(self):
        if self._enabled:
            self._enabled = False
            for icon in self._icons:
                icon.disable()

    def toggle(self):
        if self._enabled:
            self.disable()
        else:
            self.enable()


class ScreenController:
    def __init__(self):
        spi = SPI(0, bits=8, baudrate=20000000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(19), miso=Pin(16))
        cs = Pin(20, Pin.OUT)
        dc = Pin(21, Pin.OUT)
        rst = Pin(15, Pin.OUT)
        busy = Pin(14, Pin.IN)

        self._epd = EPD(spi, cs, dc, rst, busy)
        self._fb = FrameBufferEx(bytearray(self._epd.width * self._epd.height // 8), self._epd.height, self._epd.width, framebuf.MONO_VLSB)

        self.clean(True)      

        self._top_offset = 6
        self._left_offset = 0

        self._fb.fill(0)

        self.draw_static_elements()

        separation = 28 + 3

        self._mode_state = 0
        self._mode_states = ['auto', 'cool', 'dry', 'heat', 'fan']
        self._modes_lut = {
            'auto': 0,
            'cool': 1,
            'dry': 2,
            'heat': 3,
            'fan': 4
        }
        self._modes_icons = {
            'auto': Icon(TOP_ICONS['auto'], self._fb, 4 + self._left_offset, 1 + self._top_offset),
            'cool': Icon(TOP_ICONS['cool'], self._fb, 4 + self._left_offset + separation * 1, 1 + self._top_offset),
            'dry': Icon(TOP_ICONS['dry'], self._fb, 4 + self._left_offset + separation * 2, 1 + self._top_offset),
            'heat': Icon(TOP_ICONS['heat'], self._fb, 4 + self._left_offset + separation * 3, 1 + self._top_offset),
            'fan': Icon(TOP_ICONS['fan'], self._fb, 4 + self._left_offset + separation * 4, 1 + self._top_offset)
        }

        self._fan_state = 0
        self._fan_states = ['auto', 'quiet', '1', '2', '3', '4']
        self._fan_lut = {
            'auto': 0,
            'quiet': 1,
            '1': 2,
            '2': 3,
            '3': 4,
            '4': 4
        }
        self._fan_icons = {
            'auto': Icon(BOTTOM_ICONS['auto'], self._fb, 182 + self._left_offset, 37 + self._top_offset),
            'quiet': Icon(BOTTOM_ICONS['quiet'], self._fb, 157 + self._left_offset, 61 + self._top_offset),
            '1': Icon(FAN['1'], self._fb, 183 + self._left_offset, 59 + self._top_offset),
            '2': Icon(FAN['2'], self._fb, 183 + self._left_offset, 59 + self._top_offset),
            '3': Icon(FAN['3'], self._fb, 183 + self._left_offset, 59 + self._top_offset),
            '4': Icon(FAN['4'], self._fb, 183 + self._left_offset, 59 + self._top_offset)
        }

        self._vane_state = 0
        self._vane_states = ['auto', '1', '2', '3', '4', '5', 'swing']
        self._vane_lut = {
            'auto': 0,
            '1': 1,
            '2': 2,
            '3': 3,
            '4': 4,
            '5': 5,
            'swing': 6
        }
        self._vane_icons = {
            'auto': MultiIcons([
                Icon(BOTTOM_ICONS['auto'], self._fb, 157 + self._left_offset, 84 + self._top_offset),
                Icon(VANE['none'], self._fb, 179 + self._left_offset, 80 + self._top_offset)
            ]),
            '1': Icon(VANE['1'], self._fb, 179 + self._left_offset, 80 + self._top_offset),
            '2': Icon(VANE['2'], self._fb, 179 + self._left_offset, 80 + self._top_offset),
            '3': Icon(VANE['3'], self._fb, 179 + self._left_offset, 80 + self._top_offset),
            '4': Icon(VANE['4'], self._fb, 179 + self._left_offset, 80 + self._top_offset),
            '5': Icon(VANE['5'], self._fb, 179 + self._left_offset, 80 + self._top_offset),
            'swing': Icon(VANE['swing'], self._fb, 179 + self._left_offset, 80 + self._top_offset)
        }

        self.update()

        self._econo_cool_icon = Icon(TOP_ICONS['econo_cool'], self._fb, 4 + self._left_offset + separation * 5, 1 + self._top_offset)
        self._wifi_icon = Icon(TOP_ICONS['wifi'], self._fb, self._epd.height - 4 + self._left_offset - 28, 1 + self._top_offset)

        self._degrees = DegreesNumbers(self._fb, 15 + self._left_offset, 42 + self._top_offset)

        self._wifi_icon = Icon(TOP_ICONS['wifi'], self._fb, self._epd.height - 4 + self._left_offset - 28, 1 + self._top_offset)
        self._low_battery_icon = Icon(BOTTOM_ICONS['low_battery'], self._fb, 215 + self._left_offset, 38 + self._top_offset)

    def wiffi_enable(self):
        self._wifi_icon.enable()

    def wiffi_disable(self):
        self._wifi_icon.disable()

    def wiffi_toggle(self):
        self._wifi_icon.toggle()

    def low_battery_enable(self):
        self._low_battery_icon.enable()

    def low_battery_disable(self):
        self._low_battery_icon.disable()

    def low_battery_toggle(self):
        self._low_battery_icon.toggle()

    @property
    def degrees(self):
        return self._degrees

    @property
    def mode(self):
        return self._mode_states[self._mode_state]

    @mode.setter
    def mode(self, state):
        if isinstance(state, str):
            state = self._modes_lut[state]
        self._mode_state = state % len(self._mode_states)
        self.update()

    def next_mode(self):
        self.mode = self._mode_state + 1

    def update_mode(self):
        for _, icon in self._modes_icons.items():
            icon.disable()
        self._modes_icons[self.mode].enable()

    @property
    def fan(self):
        return self._fan_states[self._fan_state]

    @fan.setter
    def fan(self, state):
        if isinstance(state, str):
            state = self._fan_lut[state]
        self._fan_state = state % len(self._fan_states)
        self.update()

    def next_fan(self):
        self.fan = self._fan_state + 1

    def update_fan(self):
        for _, icon in self._fan_icons.items():
            icon.disable()
        self._fan_icons[self.fan].enable()


    @property
    def vane(self):
        return self._vane_states[self._vane_state]

    @vane.setter
    def vane(self, state):
        if isinstance(state, str):
            state = self._vane_lut[state]
        self._vane_state = state % len(self._vane_states)
        self.update()

    def next_vane(self):
        self.vane = self._vane_state + 1

    def update_vane(self):
        for _, icon in self._vane_icons.items():
            icon.disable()
        self._vane_icons[self.vane].enable()

    def update(self):
        self.update_mode()
        self.update_fan()
        self.update_vane()


    def draw_static_elements(self):
        self._fb.hline(0 + self._left_offset, 32 + self._top_offset, self._epd.height - 1, 0xffff)
        self._fb.hline(0 + self._left_offset, 33 + self._top_offset, self._epd.height - 1, 0xffff)
        self._fb.vline(150 + self._left_offset, 32 + self._top_offset, self._epd.width - 1, 0xffff)
        self._fb.vline(151 + self._left_offset, 32 + self._top_offset, self._epd.width - 1, 0xffff)

        self._fb.blit(BOTTOM_ICONS['fan'], 157 + self._left_offset, 37 + self._top_offset)


    def clean(self, clear_memory = False):
        self._epd.init(self._epd.FULL_UPDATE)
        if clear_memory:
            self._epd.clear_frame_memory(0)
            self._fb.fill(0)
        self._epd.display_frame()
        self._epd.init(self._epd.PART_UPDATE)

    def display(self):
        self._epd.set_frame_memory(self._fb.buffer, 0, 0, self._epd.width, self._epd.height)
        self._epd.display_frame()

    def sleep(self):
        #self._epd.reset()
        #self._epd.init(self._epd.FULL_UPDATE)
        #self._epd.set_frame_memory(self._fb.buffer, 0, 0, self._epd.width, self._epd.height)
        #self._epd.display_frame()
        self._epd.sleep()


from machine import Pin, SPI
import framebuf

import time


sc = ScreenController()

for _ in range(50):
    sc.next_mode()
    sc.next_fan()
    sc.next_vane()
    sc.degrees.next()
    sc.low_battery_toggle()
    sc.wiffi_toggle()
    sc.display()
    #time.sleep(1)


sc.sleep()

while True:
    time.sleep(1)



spi = SPI(0, bits=8, baudrate=20000000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(19), miso=Pin(16))
cs = Pin(20, Pin.OUT)
dc = Pin(21, Pin.OUT)
rst = Pin(15, Pin.OUT)
busy = Pin(14, Pin.IN)


epd = EPD(spi, cs, dc, rst, busy)
epd.init(epd.FULL_UPDATE)
# epd.init(epd.PART_UPDATE)
time.sleep(1)

epd.clear_frame_memory(0)

buf = bytearray(epd.width * epd.height // 8)
fb = framebuf.FrameBuffer(buf, epd.height, epd.width, framebuf.MONO_VLSB)

top_offset = 6
left_offset = 0

fb.fill(0)
# fb.text('MicroPython!', 2, 40, 0xffff)

fb.hline(0 + left_offset, 32 + top_offset, epd.height - 1, 0xffff)
fb.hline(0 + left_offset, 33 + top_offset, epd.height - 1, 0xffff)

fb.vline(150 + left_offset, 32 + top_offset, epd.width - 1, 0xffff)
fb.vline(151 + left_offset, 32 + top_offset, epd.width - 1, 0xffff)

# Top Icons
separation = 28 + 3
fb.blit(TOP_ICONS['auto'], 4 + left_offset, 1 + top_offset)
fb.blit(TOP_ICONS['cool'], 4 + left_offset + separation * 1, 1 + top_offset)
fb.blit(TOP_ICONS['dry'], 4 + left_offset + separation * 2, 1 + top_offset)
fb.blit(TOP_ICONS['heat'], 4 + left_offset + separation * 3, 1 + top_offset)
fb.blit(TOP_ICONS['fan'], 4 + left_offset + separation * 4, 1 + top_offset)
fb.blit(TOP_ICONS['econo_cool'], 4 + left_offset + separation * 5, 1 + top_offset)
fb.blit(TOP_ICONS['wifi'], epd.height - 4 + left_offset - 28, 1 + top_offset)

#epd.set_frame_memory(buf, 0, 0, epd.width, epd.height)
#epd.display_frame()
#epd.sleep()

print(TOP_ICONS['auto'].width)

while True:
    fb.blit(TOP_ICONS['auto'], 4 + left_offset, 1 + top_offset)
    epd.set_frame_memory(buf, 0, 0, epd.width, epd.height)
    epd.display_frame()
    time.sleep(0)

    fb.fill_rect(4 + left_offset, 1 + top_offset, TOP_ICONS['auto'].width, TOP_ICONS['auto'].height, 0)
    epd.set_frame_memory(buf, 0, 0, epd.width, epd.height)
    epd.display_frame()

    time.sleep(0)
