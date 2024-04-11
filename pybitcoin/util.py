import math

def little_endian_to_int(b):
    return int.from_bytes(b, 'little')

def int_to_little(n):
    length = math.ceil(math.log2(n + 1) / 8)
    print(length)
    return n.to_bytes(length, 'little')
