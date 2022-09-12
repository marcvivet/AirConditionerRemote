from machine import Pin, SPI
import framebuf
from framebuf_ex import FrameBufferEx
import time

from fb_numbers import NUMBERS
from fb_top_icons import TOP_ICONS
from fb_bottom_icons import BOTTOM_ICONS
from fb_vane import VANE
from fb_fan import FAN
from screen_driver import EPD, WRITE_RAM


class Icon:
    def __init__(self, epd, main_fb, fb, pos_x, pos_y):
        self._epd = epd
        self._enabled = False
        self._fb = fb
        self._main_fb = main_fb
        self._pos_x = pos_x
        self._pos_y = pos_y

    def enable(self):
        self._main_fb.blit(self._fb, self._pos_x, self._pos_y)
        self._enabled = True

    def disable(self):
        self._epd.set_memory_area(self._pos_x, self._pos_y, self._fb.width - 1, self._fb.height - 1)
        self._epd.set_memory_pointer(self._pos_x, self._pos_y)
        self._epd._command(WRITE_RAM)
        self._enabled = False

        for i in range(0, self._fb.width // 8 * self._fb.height):
            self._epd._data(bytearray([0]))

    def toggle(self):
        if self._enabled:
            pass
            #self.disable()
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
        self._epd.init(self._epd.FULL_UPDATE)
        time.sleep(1)

        self._buf = bytearray(self._epd.width * self._epd.height // 8)
        self._fb = FrameBufferEx(self._buf, self._epd.height, self._epd.width, framebuf.MONO_VLSB)

        self._top_offset = 6
        self._left_offset = 0

        self._fb.fill(0)

        # Top Icons
        separation = 28 + 3
        self._fb.blit(TOP_ICONS['auto'], 4 + self._left_offset, 1 + self._top_offset)
        self._fb.blit(TOP_ICONS['cool'], 4 + self._left_offset + separation * 1, 1 + self._top_offset)
        self._fb.blit(TOP_ICONS['dry'], 4 + self._left_offset + separation * 2, 1 + self._top_offset)
        self._fb.blit(TOP_ICONS['heat'], 4 + self._left_offset + separation * 3, 1 + self._top_offset)
        self._fb.blit(TOP_ICONS['fan'], 4 + self._left_offset + separation * 4, 1 + self._top_offset)
        self._fb.blit(TOP_ICONS['econo_cool'], 4 + self._left_offset + separation * 5, 1 + self._top_offset)
        self._fb.blit(TOP_ICONS['wifi'], self._epd.height - 4 + self._left_offset - 28, 1 + self._top_offset)

        self.top_auto = Icon(self._epd, self._fb, TOP_ICONS['auto'], 4 + self._left_offset, 1 + self._top_offset)

    def display(self):
        self._epd.set_frame_memory(self._buf, 0, 0, self._epd.width, self._epd.height)
        self._epd.display_frame()
