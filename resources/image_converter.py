import math
import numpy as np
import cv2


def convert_to_bytes(image_path: str, threshold: int = 220) -> str:

    data = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

    if data.shape[2] == 4:
        # make mask of where the transparent bits are
        trans_mask = data[:, :, 3] == 0
        data[trans_mask] = [255, 255, 255, 255]

    data = cv2.cvtColor(data, cv2.COLOR_BGRA2GRAY)

    data[data <= threshold] = 0
    data[data > threshold] = 1

    bits = ''
    height, width = data.shape

    for y in range(height):
        for x in range(int(math.ceil(width / 8))):
            real_index = x * 8
            bytes_raw = '0b'
            for bit in range(8):
                bit_index = real_index + bit
                if bit_index >= width:
                    bytes_raw += '0'
                else:
                    bytes_raw += str(int(data[y][real_index + bit] == 0))

            bits += f"\\x{int(bytes_raw, 2):02x}"
        
    return f"FrameBufferEx(bytearray(b'{bits}'), {width}, {height}, framebuf.MONO_HLSB)"
