import re
import ir_raw as raw


def ir_raw_encode(raw_str: str) -> str:
    int_raw = [int(element) for element in re.sub(r'Raw \(\d+\)\: ', '', raw_str).split(' ')]

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


def ir_lir_encode(string: str) -> str:
    values = re.sub(r'LIR: ', '', string).split(' ')
    code = ''
    for value in values:
        if len(value) == 2:
            code += f'{int(value, 16):0>8b}'
        else:
            code += f'{int(value, 16):0>16b}'
    return code


def main():
    for key, value in raw.BASIC_COMMANDS.items():
        print(f'{ir_raw_encode(value)} : {key}')

    for key, value in raw.MODE.items():
        print(f'{ir_raw_encode(value)} : {key}')


def permutations_():
    mode_states = ['auto', 'cool', 'dry', 'heat', 'fan']
    fan_states = ['auto', 'quiet', '1', '2', '3', '4']
    vane_states = ['auto', '1', '2', '3', '4', '5', 'swing']
    econocool = ['off', 'on']
    degrees = list(range(16, 32))


def test():
    m_cool_f_2_v_4_ec_off_d_16_on_lir = 'LIR: 26 0D1C 068C 01A2 04E6 01A6 01A6 0190 2C50 01 12 22 12 21 12 12 21 12 11 22 12 21 F2 EF 26 1F 25 11 F2 C1 12 11 22 21 22 21 12 12 11 21 1F 2E F2 EF 2E F2 81 22 12 12 30 11 22 21 22 11 21 22 11 21 12 21 22 1F 2E F2 61 F2 51 1F 2C 11 21 12 22 12 22 11 21 21 12 11 F2 EF 2E F2 EF 28 12 21 21 21'
    m_cool_f_2_v_4_ec_off_d_16_on_raw = 'Raw (583): 3356 -1676 418 -1254 418 -1254 422 -422 422 -422 422 -422 418 -1254 422 -422 422 -422 418 -1254 418 -1254 422 -422 418 -1254 422 -422 422 -422 418 -1254 418 -1254 422 -422 418 -1254 418 -1254 422 -422 422 -422 418 -1254 422 -422 422 -422 418 -1254 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 418 -1254 422 -422 422 -422 422 -422 422 -422 422 -422 418 -1254 418 -1254 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 418 -1254 418 -1254 422 -422 418 -1254 418 -1254 422 -422 422 -422 422 -422 418 -1254 422 -422 422 -422 422 -422 418 -1254 418 -1254 422 -422 418 -1254 422 -422 418 -1254 418 -1254 422 -422 418 -1254 418 -1254 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 418 -1254 422 -422 422 -422 418 -1254 422 -422 418 -1254 422 -422 400 -11344 3356 -1676 418 -1254 418 -1254 422 -422 422 -422 422 -422 418 -1254 422 -422 422 -422 418 -1254 418 -1254 422 -422 418 -1254 422 -422 422 -422 418 -1254 418 -1254 422 -422 418 -1254 418 -1254 422 -422 422 -422 418 -1254 422 -422 422 -422 418 -1254 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 418 -1254 422 -422 422 -422 422 -422 422 -422 422 -422 418 -1254 418 -1254 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 418 -1254 418 -1254 422 -422 418 -1254 418 -1254 422 -422 422 -422 422 -422 418 -1254 422 -422 422 -422 422 -422 418 -1254 418 -1254 422 -422 418 -1254 422 -422 418 -1254 418 -1254 422 -422 418 -1254 418 -1254 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 422 -422 418 -1254 422 -422 422 -422 418 -1254 422 -422 418 -1254 422 -422 418'

    print(ir_raw_encode(m_cool_f_2_v_4_ec_off_d_16_on_raw))
    print()
    print(ir_lir_encode(m_cool_f_2_v_4_ec_off_d_16_on_lir))

    m_cool_f_auto_v_auto_ec_on_d_16_off_lir = 'LIR: 26 0D1C 068C 01A2 04E6 01A4 01A4 0194 2C54 01 12 22 12 21 12 12 21 12 11 22 12 21 F2 EF 2C 11 F2 C1 12 11 F2 81 22 21 12 11 F2 EF 2E 22 1F 2E F2 4F 14 21 22 30 11 22 21 22 11 21 22 11 21 12 21 22 1F 2E F2 C1 1F 2C 11 21 1F 28 12 22 11 21 1F 2E F2 E2 21 F2 EF 24 F1 42 12 21'
    m_cool_f_auto_v_auto_ec_on_d_16_off_raw = 'Raw (583): 3356 -1676 418 -1254 418 -1254 420 -420 420 -420 420 -420 418 -1254 420 -420 420 -420 418 -1254 418 -1254 420 -420 418 -1254 420 -420 420 -420 418 -1254 418 -1254 420 -420 418 -1254 418 -1254 420 -420 420 -420 418 -1254 420 -420 420 -420 418 -1254 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 418 -1254 418 -1254 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 418 -1254 418 -1254 420 -420 418 -1254 418 -1254 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 418 -1254 420 -420 420 -420 420 -420 418 -1254 418 -1254 420 -420 418 -1254 418 -1254 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 418 -1254 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 418 -1254 418 -1254 418 -1254 418 -1254 420 -420 418 -1254 420 -420 420 -420 404 -11348 3356 -1676 418 -1254 418 -1254 420 -420 420 -420 420 -420 418 -1254 420 -420 420 -420 418 -1254 418 -1254 420 -420 418 -1254 420 -420 420 -420 418 -1254 418 -1254 420 -420 418 -1254 418 -1254 420 -420 420 -420 418 -1254 420 -420 420 -420 418 -1254 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 418 -1254 418 -1254 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 418 -1254 418 -1254 420 -420 418 -1254 418 -1254 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 418 -1254 420 -420 420 -420 420 -420 418 -1254 418 -1254 420 -420 418 -1254 418 -1254 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 418 -1254 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 420 -420 418 -1254 418 -1254 418 -1254 418 -1254 420 -420 418 -1254 420 -420 420 -420 418'

if __name__ == '__main__':
    test()