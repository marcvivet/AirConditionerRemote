import re
import sys
print(sys.path)

import numpy as np
import pandas as pd

import ir_raw as raw
from lir_tools import lir_2_raw


def ir_encode(raw_str: str) -> str:
    if raw_str.startswith('LIR:'):
        raw_str = lir_2_raw(raw_str)
    int_raw = [int(element) for element in re.sub(r'Raw \(\d*\)\: ', '', raw_str).split(' ')]

    code = ''
    for index in range(len(int_raw) // 2):
        up = int_raw[index * 2]
        down = abs(int_raw[(index * 2) + 1])

        if up > 3000 and down > 1500:
            continue

        if up > 410 and down < 500:
            code += '0'
            continue

        if up > 410 and down > 500 and down < 2000:
            code += '1'
            continue
        break
    return code

def bin_2_hex(code: str) -> list:
    hex_list = []
    for byte in re.findall('........', code):
        hex_list.append(hex(int(byte, 2)))

    return hex_list


def main():
    columns = ['mode', 'fan', 'vane', 'econocool', 'degress', 'power']
    pattern = re.compile(r'm_(?P<mode>[a-z]+)_f_(?P<fan>[a-z]*\d*)_v_(?P<vane>[a-z]*\d*)_ec_(?P<econocool>[a-z]*)_d_(?P<degrees>\d*)_(?P<power>\w*)')

    data = []
    with open('ir/lir_library.txt', 'r') as file_r:
        for line in file_r.readlines():
            if not line:
                break

            elements = line.split(';')
            # m_auto_f_auto_v_auto_ec_off_d_16_off
            command = elements[4]
            bin_code = ir_encode(elements[6])
            byte_code = re.findall('........', bin_code)
            command_data = pattern.match(command).groupdict()

            data.append([
                command_data['mode'],
                command_data['fan'],
                command_data['vane'],
                command_data['econocool'],
                command_data['degrees'],
                command_data['power'],
            ] + byte_code)

    dataframe = pd.DataFrame(np.array(data), columns=columns + [f'byte {index}' for index in range(len(byte_code))])
    dataframe.to_excel('ir_library.xlsx')

    

def permutations_():
    mode_states = ['auto', 'cool', 'dry', 'heat', 'fan']
    fan_states = ['auto', 'quiet', '1', '2', '3', '4']
    vane_states = ['auto', '1', '2', '3', '4', '5', 'swing']
    econocool = ['off', 'on']
    degrees = list(range(16, 32))

if __name__ == '__main__':
    main()
