# coding=utf-8
import re
from functools import reduce

R = 32
TOTAL = 128
# G = 0x9e3779b9.to_bytes(4, byteorder='little')
G = '9e3779b9'


FPTable = [
    0, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56, 60,
    64, 68, 72, 76, 80, 84, 88, 92, 96, 100, 104, 108, 112, 116, 120, 124,
    1, 5, 9, 13, 17, 21, 25, 29, 33, 37, 41, 45, 49, 53, 57, 61,
    65, 69, 73, 77, 81, 85, 89, 93, 97, 101, 105, 109, 113, 117, 121, 125,
    2, 6, 10, 14, 18, 22, 26, 30, 34, 38, 42, 46, 50, 54, 58, 62,
    66, 70, 74, 78, 82, 86, 90, 94, 98, 102, 106, 110, 114, 118, 122, 126,
    3, 7, 11, 15, 19, 23, 27, 31, 35, 39, 43, 47, 51, 55, 59, 63,
    67, 71, 75, 79, 83, 87, 91, 95, 99, 103, 107, 111, 115, 119, 123, 127,
]


def revert_byte(byte, just=32):
    return hex(int(bin(int(byte, 16)).split('b')[-1].rjust(just, '0')[::-1], 2)).split('x')[-1]


def cyclic_shift(byte, value):
    bit = bin(int(byte, 16)).split('b')[-1].rjust(32, '0')
    byte = hex(int('0b' + bit[value:] + bit[:value], 2)).split('x')[-1]
    return byte.rjust(8, '0')


def shift(byte, value):
    bit = bin(int(byte, 16)).split('b')[-1].rjust(32, '0')
    if value > 0:
        new_bit = bit[value:] + '0' * len(bit[:value])
    else:
        new_bit = '0' * len(bit[value:]) + bit[:value]
    byte = hex(int('0b' + new_bit, 2)).split('x')[-1]
    return byte.rjust(8, '0')


def xor_func(el_prev, el):
    return hex(int(el_prev, 16) ^ int(el, 16)).split('x')[-1]


def zip_add(*arr):
    max_len = 0
    for i in arr:
        if max_len < len(i):
            max_len = len(i)
    new_arr = []
    for i in arr:
        new_arr.append((max_len - len(i)) * '0' + i)
    return zip(*new_arr)


def byte_xor(*arr_bytes):
    q = ''.join([reduce(xor_func, byte) for byte in zip_add(*arr_bytes)])
    return q


def l(x):
    x3, x2, x1, x0 = (
        x[24: 32],
        x[16: 24],
        x[8: 16],
        x[0: 8]
    )
    x0 = cyclic_shift(x0, 13)
    x2 = cyclic_shift(x2, 3)
    x1 = byte_xor(x1, x0, x2)
    x3 = byte_xor(x3, x2, shift(x0, 3))
    x1 = cyclic_shift(x1, 1)
    x3 = cyclic_shift(x3, 7)
    x0 = byte_xor(x0, x1, x3)
    x2 = byte_xor(x2, x3, shift(x1, 7))
    x0 = cyclic_shift(x0, 5)
    x2 = cyclic_shift(x2, 22)
    return ''.join((x0, x1, x2, x3))


def l_inverse(x):

    x3, x2, x1, x0 = (
        x[24: 32],
        x[16: 24],
        x[8: 16],
        x[0: 8]
    )

    x2 = cyclic_shift(x2, 10)
    x0 = cyclic_shift(x0, 27)
    x2 = byte_xor(x2, x3, shift(x1, 7))
    x0 = byte_xor(x0, x1, x3)
    x3 = cyclic_shift(x3, 25)
    x1 = cyclic_shift(x1, 31)
    x3 = byte_xor(x3, x2, shift(x0, 3))
    x1 = byte_xor(x1, x0, x2)
    x2 = cyclic_shift(x2, 29)
    x0 = cyclic_shift(x0, 19)
    return ''.join((x0, x1, x2, x3))


S_table = [
    [3, 8, 15, 1, 10, 6, 5, 11, 14, 13, 4, 2, 7, 0, 9, 12],  # S0
    [15, 12, 2, 7, 9, 0, 5, 10, 1, 11, 14, 8, 6, 13, 3, 4],  # S1
    [8, 6, 7, 9, 3, 12, 10, 15, 13, 1, 14, 4, 0, 11, 5, 2],  # S2
    [0, 15, 11, 8, 12, 9, 6, 3, 13, 1, 2, 4, 10, 7, 5, 14],  # S3
    [1, 15, 8, 3, 12, 0, 11, 6, 2, 5, 4, 10, 9, 14, 7, 13],  # S4
    [15, 5, 2, 11, 4, 10, 9, 12, 0, 3, 14, 8, 13, 6, 7, 1],  # S5
    [7, 2, 12, 5, 8, 4, 6, 11, 14, 9, 1, 15, 13, 3, 10, 0],  # S6
    [1, 13, 15, 0, 14, 8, 2, 11, 7, 4, 12, 10, 9, 3, 5, 6],  # S7
]

S_table_inverse = (
    (13,	3,	11,	0,	10,	6,	5,	12,	1,	14,	4,	7,	15,	9,	8,	2),
    (5,	8,	2,	14,	15,	6,	12,	3,	11,	4,	7,	9,	1,	13,	10,	0),
    (12,	9,	15,	4,	11,	14,	1,	2,	0,	3,	6,	13,	5,	8,	10,	7),
    (0,	9,	10,	7,	11,	14,	6,	13,	3,	5,	12,	2,	4,	8,	15,	1),
    (5,	0,	8,	3,	10,	9,	7,	14,	2,	12,	11,	6,	4,	15,	13,	1),
    (8,	15,	2,	9,	4,	1,	13,	14,	11,	6,	5,	3,	7,	12,	10,	0),
    (15,	10,	1,	13,	5,	3,	6,	0,	4,	9,	14,	7,	2,	12,	8,	11),
    (3,	0,	6,	13,	9,	14,	15,	8,	5,	12,	11,	7,	10,	1,	4,	2)
)


def ip(arr=None, bits=None):
    if arr:
        x = bin(int(''.join(arr), 16)).split('b')[-1].rjust(TOTAL, '0')
    if bits:
        x = bits
    c = [0] * TOTAL
    t = ''
    for index in range(TOTAL):
        # j = index // 4
        # new_index = (index % 4) * 32 + j
        # c[new_index] = x[index]
        t += x[IPTable[index]]
    new_value = int('0b' + t, 2)
    return hex(new_value).split('x')[-1]


def fp(arr=None, bits=None):
    if arr:
        x = bin(int(''.join(arr), 16)).split('b')[-1].rjust(TOTAL, '0')
    if bits:
        x = bits
    t = ''
    for index in range(TOTAL):
        t += x[FPTable[index]]
    new_value = int('0b' + t, 2)
    return hex(new_value).split('x')[-1]


def validate_key(k):

    l = len(k)
    if l > 256:
        return k[:256]

    if l == 256:
        return k
    else:
        return k + "1" + "0" * (256 - l - 1)


def get_s_table_val(index, args, s_table=S_table):
    row_s_table = s_table[index]
    arr = []
    for arg in args:
        s = ''
        for i in arg:
            s += hex(row_s_table[int(i, 16)]).split('x')[-1]
        arr.append(s)
    return ''.join(arr)


def word4(i):
    return '0' * 6 + hex(i).split('x')[-1]


IPTable = [
    0, 32, 64, 96, 1, 33, 65, 97, 2, 34, 66, 98, 3, 35, 67, 99,
    4, 36, 68, 100, 5, 37, 69, 101, 6, 38, 70, 102, 7, 39, 71, 103,
    8, 40, 72, 104, 9, 41, 73, 105, 10, 42, 74, 106, 11, 43, 75, 107,
    12, 44, 76, 108, 13, 45, 77, 109, 14, 46, 78, 110, 15, 47, 79, 111,
    16, 48, 80, 112, 17, 49, 81, 113, 18, 50, 82, 114, 19, 51, 83, 115,
    20, 52, 84, 116, 21, 53, 85, 117, 22, 54, 86, 118, 23, 55, 87, 119,
    24, 56, 88, 120, 25, 57, 89, 121, 26, 58, 90, 122, 27, 59, 91, 123,
    28, 60, 92, 124, 29, 61, 93, 125, 30, 62, 94, 126, 31, 63, 95, 127,
]


def get_sub_keys(key):
    w = [0] * 12
    k = []
    for i in range(8):
        w[i] = key[i * 8: (i + 1) * 8]

    for i in range(33):
        for j in range(4):
            w[j + 8] = cyclic_shift(
                byte_xor(w[j], w[j + 3], w[j + 5],
                         w[j + 7], G, word4(4 * i + j)),
                11)
        k.append(ip(get_s_table_val((11 - i) % 8, w[8:12])).rjust(8, '0'))
        w[0:8] = w[4:12]
    return k


def decrypt(encrypted, key):
    key = validate_key(key)
    k = get_sub_keys(key)
    B = ip(encrypted)
    B = B.rjust(32, '0')
    B = byte_xor(get_s_table_val(7, byte_xor(B, k[32]).rjust(32, '0'), S_table_inverse), k[31])
    B = B.rjust(32, '0')
    for i in reversed(range(31)):
        B = l_inverse(B)
        B = byte_xor(get_s_table_val(i % 8, B.rjust(32, '0'), S_table_inverse), k[i]).rjust(32, '0')

    B = fp(B)

    return B.rjust(32, '0').upper()


def encrypt(decrypted, key):
    key = validate_key(key)
    k = get_sub_keys(key)
    C = ip(decrypted)
    C = C.rjust(32, '0')
    for i in range(31):
        C = l(get_s_table_val(i % 8, byte_xor(C, k[i]).rjust(32, '0')))
        C = C.rjust(32, '0')
    C = byte_xor(get_s_table_val(7, byte_xor(C, k[31]).rjust(32, '0')).rjust(32, '0'), k[32]).rjust(32, '0')
    C = fp(C)

    return C.rjust(32, '0').upper()


def load_file(file_name):
    with open(file_name, 'r') as f:
        exp = re.compile(
            r'Set (\d+), vector#\W*(\d+):'
            r'\n*\W*key=(\w+)\W*\n*'
            r'\W*plain=(\w+)\W*\n*'
            r'\W*cipher=(\w+)\W*\n*'
            r'\W*decrypted=(\w+)\W*\n*'
            r'\W*(Iterated 100 times=(\w+))?\W*\n*'
            r'\W*(Iterated 1000 times=(\w+))?\W*\n*',
            re.IGNORECASE
        )
        lines = ''.join(f.readlines())
        all_test = []
        for test in exp.findall(lines):

            # Если в тесте есть Iterated
            if len(test) > 6:
                (set_n, vector, key, plain, cipher,
                 decrypted, is_it_100, it_100, is_it_1000, it_1000) = test
            else:
                set_n, vector, key, plain, cipher, decrypted = test
                it_100 = None
                it_1000 = None

            all_test.append({
                'set': set_n,
                'vector': vector,
                'key': key,
                'plain': plain,
                'cipher': cipher,
                'decrypted': decrypted,
                'it_100': it_100,
                'it_1000': it_1000,
            })

        return all_test


def test_file(tests):
    for test in tests:
        print('Set {}, vector# {}'.format(test['set'], test['vector']))
        encrypted = encrypt(test['plain'], test['key'])
        print('Шифрование {}'.format(str(encrypted == test['cipher'])))
        decrypted = decrypt(encrypted, test['key'])
        print('Расшифрование {}'.format(str(decrypted == test['plain'])))
        if test['it_100']:
            d = test['plain']
            for i in range(100):
                d = encrypt(d, test['key'])
            print('100 Итераций {}'.format(str(d == test['it_100'])))
        if test['it_1000']:
            d = test['plain']
            for i in range(1000):
                d = encrypt(d, test['key'])
            print('1000 Итераций {}'.format(d == test['it_1000']))


test_128 = load_file('9.2.30.Serpent.vectors128.txt')
test_192 = load_file('9.2.30.Serpent.vectors192.txt')
test_256 = load_file('9.2.30.Serpent.vectors256.txt')

test_file(test_256)
test_file(test_192)
test_file(test_128)


# Простое разложение (Режим ECB)
def test_ecb_mode(text, key):
    encrypted_blocks = []
    # TOTAL - размер одного блока (128 бит)
    # text - 16-ричное число. Чтобы не переводить в биты
    # TOTAL делим на 4
    for i in range(len(text) // (TOTAL // 4)):
        block = text[i * (TOTAL // 4): (i + 1) * (TOTAL // 4)]
        encrypted_blocks.append(encrypt(block, key))
    encrypt_text = ''.join(encrypted_blocks)
    decrypted_block = []
    for i in range(len(encrypt_text) // (TOTAL // 4)):
        block = encrypt_text[i * (TOTAL // 4): (i + 1) * (TOTAL // 4)]
        if block:
            decrypted_block.append(decrypt(block, key))
    print(''.join(decrypted_block) == text)


test_ecb_mode(text='3DA46FFA6F4D6F30CD258333E5A61369'
                   '3DA46FFA6F4D6F30CD258333E5A61369'
                   '3DA46FFA6F4D6F30CD258333E5A61369'
                   '3DA46FFA6F4D6F30CD258333E5A61369'
                   '3DA46FFA6F4D6F30CD258333E5A61369',
              key='8000000000000000000000000000000000000000000000000000000000000000')
"""
Вывод:
True
"""


# Режим обратной связи по открытому тексту
def test_pfb_mode(text, key):
    p0 = '00000000000000000000000000000000'
    encrypted_blocks = []
    p_prev = p0
    for i in range(len(text) // (TOTAL // 4)):
        block = text[i * (TOTAL // 4): (i + 1) * (TOTAL // 4)]
        # Ci = Pi + E(Pi-1, key)
        encrypted_blocks.append(byte_xor(block, encrypt(p_prev, key)))
        p_prev = block
    encrypt_text = ''.join(encrypted_blocks)

    decrypted_blocks = []
    p_prev = p0
    for i in range(len(encrypt_text) // (TOTAL // 4)):
        block = text[i * (TOTAL // 4): (i + 1) * (TOTAL // 4)]
        # Pi = Ci + E(Pi-1, key)
        Pi = byte_xor(block, decrypt(p_prev, key))
        decrypted_blocks.append(Pi)
        p_prev = Pi
    decrypted_text = ''.join(decrypted_blocks)

    print(decrypted_text == text)


test_pfb_mode(text='3DA46FFA6F4D6F30CD258333E5A61369'
                   '3DA46FFA6F4D6F30CD258333E5A61369'
                   '3DA46FFA6F4D6F30CD258333E5A61369'
                   '3DA46FFA6F4D6F30CD258333E5A61369'
                   '3DA46FFA6F4D6F30CD258333E5A61369',
              key='8000000000000000000000000000000000000000000000000000000000000000')

"""
Вывод
True
"""