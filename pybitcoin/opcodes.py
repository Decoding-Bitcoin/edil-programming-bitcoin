from pybitcoin.hash import (
    ripemd160,
    sha1,
    sha256,
    hash160,
    hash256
)
from pybitcoin.ecc import (
    Signature,
    S256Point
)


def encode_num(num):
    # script uses MSB as the sign bit instead of two's complement
    if num == 0:
        return b''
    abs_num = abs(num)
    negative = num < 0
    result = bytearray()
    while abs_num:
        result.append(abs_num & 0xff)
        abs_num >>= 8
    if result[-1] & 0x80:
        if negative:
            result.append(0x80)
        else:
            result.append(0)
    elif negative:
        result[-1] |= 0x80
    return bytes(result)

def decode_num(element):
    if element == b'':
        return 0
    big_endian = element[::-1]
    if big_endian[0] & 0x80:
        negative = True
        result = big_endian[0] & 0x7f
    else:
        negative = False
        result = big_endian[0]
    for c in big_endian[1:]:
        result <<= 8
        result += c
    if negative:
        return -result
    else:
        return result

def op_disabled(*args):
    return False

# 0x00: OP_0
def op_0(stack):
    stack.append(encode_num(0))
    return True

# 0x4c: 'OP_PUSHDATA1',
# 0x4d: 'OP_PUSHDATA2',
# 0x4e: 'OP_PUSHDATA4',

# 0x4f: 'OP_1NEGATE'
def op_1negate(stack):
    stack.append(encode_num(-1))
    return True

# 0x50: 'OP_RESERVED', # reserved

# 0x51: 'OP_1'
def op_1(stack):
    stack.append(encode_num(1))
    return True

# 0x52: 'OP_2'
def op_2(stack):
    stack.append(encode_num(2))
    return True

# 0x53: 'OP_3'
def op_3(stack):
    stack.append(encode_num(3))
    return True

# 0x54: 'OP_4'
def op_4(stack):
    stack.append(encode_num(4))
    return True

# 0x55: 'OP_5'
def op_5(stack):
    stack.append(encode_num(5))
    return True

# 0x56: 'OP_6'
def op_6(stack):
    stack.append(encode_num(6))
    return True

# 0x57: 'OP_7'
def op_7(stack):
    stack.append(encode_num(7))
    return True

# 0x58: 'OP_8'
def op_8(stack):
    stack.append(encode_num(8))
    return True

# 0x59: 'OP_9'
def op_9(stack):
    stack.append(encode_num(9))
    return True

# 0x5a: 'OP_10'
def op_10(stack):
    stack.append(encode_num(10))
    return True

# 0x5b: 'OP_11'
def op_11(stack):
    stack.append(encode_num(11))
    return True

# 0x5c: 'OP_12'
def op_12(stack):
    stack.append(encode_num(12))
    return True

# 0x5d: 'OP_13'
def op_13(stack):
    stack.append(encode_num(13))
    return True

# 0x5e: 'OP_14'
def op_14(stack):
    stack.append(encode_num(14))
    return True

# 0x5f: 'OP_15'
def op_15(stack):
    stack.append(encode_num(15))
    return True

# 0x60: 'OP_16'
def op_16(stack):
    stack.append(encode_num(16))
    return True

# 0x61: 'OP_NOP'
def op_nop(stack):
    return True

# 0x62: 'OP_VER', # reserved

# 0x63: 'OP_IF'
def op_if(stack, items):
    if len(stack) < 1:
        return False
    # go through and re-make the items array based on the top stack element
    true_items = []
    false_items = []
    current_array = true_items
    found = False
    num_endifs_needed = 1
    while len(items) > 0:
        item = items.pop(0)
        if item in (99, 100):
            # nested if, we have to go another endif
            num_endifs_needed += 1
            current_array.append(item)
        elif num_endifs_needed == 1 and item == 103:
            current_array = false_items
        elif item == 104:
            if num_endifs_needed == 1:
                found = True
                break
            else:
                num_endifs_needed -= 1
                current_array.append(item)
        else:
            current_array.append(item)
    if not found:
        return False
    element = stack.pop()
    if decode_num(element) == 0:
        items[:0] = false_items
    else:
        items[:0] = true_items
    return True

# 0x64: 'OP_NOTIF'
def op_notif(stack, items):
    if len(stack) < 1:
        return False
    # go through and re-make the items array based on the top stack element
    true_items = []
    false_items = []
    current_array = true_items
    found = False
    num_endifs_needed = 1
    while len(items) > 0:
        item = items.pop(0)
        if item in (99, 100):
            # nested if, we have to go another endif
            num_endifs_needed += 1
            current_array.append(item)
        elif num_endifs_needed == 1 and item == 103:
            current_array = false_items
        elif item == 104:
            if num_endifs_needed == 1:
                found = True
                break
            else:
                num_endifs_needed -= 1
                current_array.append(item)
        else:
            current_array.append(item)
    if not found:
        return False
    element = stack.pop()
    if decode_num(element) == 0:
        items[:0] = true_items
    else:
        items[:0] = false_items
    return True

# 0x65: 'OP_VERIF', # reserved
# 0x66: 'OP_VERNOTIF', # reserved
# 0x67: 'OP_ELSE',
# 0x68: 'OP_ENDIF',

# 0x69: 'OP_VERIFY',
def op_verify(stack):
    if len(stack) < 1:
        return False
    element = stack.pop()
    if decode_num(element) == 0:
        return False
    return True

# 0x6a: 'OP_RETURN'
def op_return(stack):
    return False

# 0x6b: 'OP_TOALTSTACK'
def op_toaltstack(stack, altstack):
    if len(stack) < 1:
        return False
    altstack.append(stack.pop())
    return True

# 0x6c: 'OP_FROMALTSTACK'
def op_fromaltstack(stack, altstack):
    if len(altstack) < 1:
        return False
    stack.append(altstack.pop())
    return True

# 0x6d: 'OP_2DROP'
def op_2drop(stack):
    if len(stack) < 2:
        return False
    stack.pop()
    stack.pop()
    return True

# 0x6e: 'OP_2DUP'
def op_2dup(stack):
    if len(stack) < 2:
        return False
    stack.extend(stack[-2:])
    return True

# 0x6f: 'OP3DUP'
def op_3dup(stack):
    if len(stack) < 3:
        return False
    stack.extend(stack[-3:])
    return True

# 0x70: 'OP_2OVER'
def op_2over(stack):
    if len(stack) < 4:
        return False
    stack.extend(stack[-4:-2])
    return True

# 0x71: 'OP_2ROT'
def op_2rot(stack):
    if len(stack) < 6:
        return False
    stack.append(stack.pop(-6))
    stack.append(stack.pop(-6))
    return True

# 0x72: 'OP_2SWAP'
def op_2swap(stack):
    if len(stack) < 4:
        return False
    stack.append(stack.pop(-4))
    stack.append(stack.pop(-4))
    return True

# 0x73: 'OP_IFDUP'
def op_ifdup(stack):
    if len(stack) < 1:
        return False
    if decode_num(stack[-1]) != 0:
        stack.append(stack[-1])
    return True

# 0x74: 'OP_DEPTH'
def op_depth(stack):
    stack.append(encode_num(len(stack)))
    return True

# 0x75: 'OP_DROP'
def op_drop(stack):
    if len(stack) < 1:
        return False
    stack.pop()
    return True

# 0x76: OP_DUP
def op_dup(stack):
    if len(stack) < 1:
        return False
    stack.append(stack[-1])
    return True

# 0x77: 'OP_NIP'
def op_nip(stack):
    if len(stack) < 2:
        return False
    stack.pop(-2)
    return True

# 0x78: 'OP_OVER'
def op_over(stack):
    if len(stack) < 2:
        return False
    stack.append(stack[-2])
    return True

# 0x79: 'OP_PICK'
def op_pick(stack):
    if len(stack) < 1:
        return False
    n = decode_num(stack.pop())
    if len(stack) < n + 1:
        return False
    stack.append(stack[-n - 1])
    return True

# 0x7a: 'OP_ROLL'
def op_roll(stack):
    if len(stack) < 1:
        return False
    n = decode_num(stack.pop())
    if len(stack) < n + 1:
        return False
    stack.append(stack.pop(-n - 1))
    return True

# 0x7b: 'OP_ROT'
def op_rot(stack):
    if len(stack) < 3:
        return False
    stack.append(stack.pop(-3))
    return True

# 0x7c: 'OP_SWAP'
def op_swap(stack):
    if len(stack) < 2:
        return False
    stack.append(stack.pop(-2))
    return True

# 0x7d: 'OP_TUCK'
def op_tuck(stack):
    if len(stack) < 2:
        return False
    stack.insert(-2, stack[-1])
    return True

# 0x7e: 'OP_CAT',
# 0x7f: 'OP_SUBSTR',
# 0x80: 'OP_LEFT',
# 0x81: 'OP_RIGHT',

# 0x82: 'OP_SIZE'
def op_size(stack):
    if len(stack) < 1:
        return False
    size = len(stack[-1])
    stack.append(encode_num(size))
    return True

# 0x83: 'OP_INVERT',
# 0x84: 'OP_AND',
# 0x85: 'OP_OR',
# 0x86: 'OP_XOR',

# 0x87: 'OP_EQUAL'
def op_equal(stack):
    if len(stack) < 2:
        return False
    x1 = stack.pop()
    x2 = stack.pop()
    if x1 == x2:
        stack.append(encode_num(1))
    else:
        stack.append(encode_num(0))
    return True

# 0x88: 'OP_EQUALVERIFY'
def op_equalverify(stack):
    return op_equal(stack) and op_verify(stack)

# 0x89: 'OP_RESERVED1', # reserved
# 0x8a: 'OP_RESERVED2', # reserved

# 0x8b: 'OP_1ADD'
def op_1add(stack):
    if len(stack) < 1:
        return False
    n = decode_num(stack.pop())
    stack.append(encode_num(n + 1))
    return True

# 0x8c: 'OP_1SUB'
def op_1sub(stack):
    if len(stack) < 1:
        return False
    n = decode_num(stack.pop())
    stack.append(encode_num(n - 1))
    return True

# 0x8d: 'OP_2MUL',
# 0x8e: 'OP_2DIV',

# 0x8f: 'OP_NEGATE'
def op_negate(stack):
    if len(stack) < 1:
        return False
    n = decode_num(stack.pop())
    stack.append(encode_num(-n))
    return True

# 0x90: 'OP_ABS'
def op_abs(stack):
    if len(stack) < 1:
        return False
    n = decode_num(stack.pop())
    if n > 0:
        stack.append(encode_num(n))
    else:
        stack.append(encode_num(-n))
    return True

# 0x91: 'OP_NOT'
def op_not(stack):
    if len(stack) < 1:
        return False
    n = decode_num(stack.pop())
    if n == 0:
        stack.append(encode_num(1))
    else:
        stack.append(encode_num(0))
    return True

# 0x92: 'OP_0NOTEQUAL'
def op_0notequal(stack):
    if len(stack) < 1:
        return False
    n = decode_num(stack.pop())
    if n == 0:
        stack.append(encode_num(0))
    else:
        stack.append(encode_num(1))
    return True

# 0x93: 'OP_ADD'
def op_add(stack):
    if len(stack) < 2:
        return False
    b = decode_num(stack.pop())
    a = decode_num(stack.pop())
    stack.append(encode_num(a + b))
    return True

# 0x94: 'OP_SUB'
def op_sub(stack):
    if len(stack) < 2:
        return False
    b = decode_num(stack.pop())
    a = decode_num(stack.pop())
    stack.append(encode_num(a - b))
    return True

# 0x95: 'OP_MUL',
# 0x96: 'OP_DIV',
# 0x97: 'OP_MOD',
# 0x98: 'OP_LSHIFT',
# 0x99: 'OP_RSHIFT',

# 0x9a: 'OP_BOOLAND'
def op_booland(stack):
    if len(stack) < 2:
        return False
    b = decode_num(stack.pop())
    a = decode_num(stack.pop())
    if a != 0 and b != 0:
        stack.append(encode_num(1))
    else:
        stack.append(encode_num(0))
    return True

# 0x9b: 'OP_BOOLOR'
def op_boolor(stack):
    if len(stack) < 2:
        return False
    b = decode_num(stack.pop())
    a = decode_num(stack.pop())
    if a == 0 and b == 0:
        stack.append(encode_num(0))
    else:
        stack.append(encode_num(1))
    return True

# 0x9c: 'OP_NUMEQUAL'
def op_numequal(stack):
    if len(stack) < 2:
        return False
    b = decode_num(stack.pop())
    a = decode_num(stack.pop())
    if a == b:
        stack.append(encode_num(1))
    else:
        stack.append(encode_num(0))
    return True

# 0x9d: 'OP_NUMEQUALVERIFY'
def op_numequalverify(stack):
    return op_numequal(stack) and op_verify(stack)

# 0x9e: 'OP_NUMNOTEQUAL'
def op_numnotequal(stack):
    if len(stack) < 2:
        return False
    b = decode_num(stack.pop())
    a = decode_num(stack.pop())
    if a != b:
        stack.append(encode_num(1))
    else:
        stack.append(encode_num(0))
    return True

# 0x9f: 'OP_LESSTHAN'
def op_lessthan(stack):
    if len(stack) < 2:
        return False
    b = decode_num(stack.pop())
    a = decode_num(stack.pop())
    if a < b:
        stack.append(encode_num(1))
    else:
        stack.append(encode_num(0))
    return True

# 0xa0: 'OP_GREATERTHAN'
def op_greaterthan(stack):
    if len(stack) < 2:
        return False
    b = decode_num(stack.pop())
    a = decode_num(stack.pop())
    if a > b:
        stack.append(encode_num(1))
    else:
        stack.append(encode_num(0))
    return True

# 0xa1: 'OP_LESSTHANOREQUAL'
def op_lessthanorequal(stack):
    if len(stack) < 2:
        return False
    b = decode_num(stack.pop())
    a = decode_num(stack.pop())
    if a <= b:
        stack.append(encode_num(1))
    else:
        stack.append(encode_num(0))
    return True

# 0xa2: 'OP_GREATERTHANOREQUAL'
def op_greaterthanorequal(stack):
    if len(stack) < 2:
        return False
    b = decode_num(stack.pop())
    a = decode_num(stack.pop())
    if a >= b:
        stack.append(encode_num(1))
    else:
        stack.append(encode_num(0))
    return True

# 0xa3: 'OP_MIN'
def op_min(stack):
    if len(stack) < 2:
        return False
    b = decode_num(stack.pop())
    a = decode_num(stack.pop())
    if a < b:
        stack.append(encode_num(a))
    else:
        stack.append(encode_num(b))
    return True

# 0xa4: 'OP_MAX'
def op_max(stack):
    if len(stack) < 2:
        return False
    b = decode_num(stack.pop())
    a = decode_num(stack.pop())
    if a < b:
        stack.append(encode_num(b))
    else:
        stack.append(encode_num(a))
    return True

# 0xa5: 'OP_WITHIN'
def op_within(stack):
    if len(stack) < 3:
        return False
    max = decode_num(stack.pop())
    min = decode_num(stack.pop())
    n   = decode_num(stack.pop())
    if min <= n and n < max:
        stack.append(encode_num(1))
    else:
        stack.append(encode_num(0))
    return True

# 0xa6: 'OP_RIPEMD160'
def op_ripemd160(stack):
    if len(stack) < 1:
        return False
    element = stack.pop()
    stack.append(ripemd160(element))
    return True

# 0xa7: 'OP_SHA1'
def op_sha1(stack):
    if len(stack) < 1:
        return False
    element = stack.pop()
    stack.append(sha1(element))
    return True

# 0xa8: 'OP_SHA256'
def op_sha256(stack):
    if len(stack) < 1:
        return False
    element = stack.pop()
    stack.append(sha256(element))
    return True

# 0xa9: 'OP_HASH160',
def op_hash160(stack):
    if len(stack) < 1:
        return False
    element = stack.pop()
    stack.append(hash160(element))
    return True

# 0xaa: OP_HASH256
def op_hash256(stack):
    if len(stack) < 1:
        return False
    element = stack.pop()
    stack.append(hash256(element))
    return True

# 0xab: 'OP_CODESEPARATOR',

# 0xac: 'OP_CHECKSIG'
def op_checksig(stack, z):
    if len(stack) < 2:
        return False
    pubkey = S256Point.parse(stack.pop())
    signature = Signature.parse(stack.pop())
    if pubkey.verify(z, signature):
        stack.append(encode_num(1))
    else:
        stack.append(encode_num(0))
    return True

# 0xad: 'OP_CHECKSIGVERIFY'
def op_checksigverify(stack, z):
    return op_checksig(stack, z) and op_verify(stack)

# 0xae: 'OP_CHECKMULTISIG'
def op_checkmultisig(stack, z):
    raise NotImplementedError

# 0xaf: 'OP_CHECKMULTISIGVERIFY'
def op_checkmultisigverify(stack, z):
    return op_checkmultisig(stack, z) and op_verify(stack)

# 0xb0: 'OP_NOP1', # reserved

# 0xb1: 'OP_CHECKLOCKTIMEVERIFY', # previously OP_NOP2
def op_checklocktimeverify(stack, locktime, sequence):
    if sequence == 0xffffffff:
        return False
    if len(stack) < 1:
        return False
    element = decode_num(stack[-1])
    if element < 0:
        return False
    if element < 500000000 and locktime > 500000000:
        return False
    if locktime < element:
        return False
    return True

# 0xb2: 'OP_CHECKSEQUENCEVERIFY', # previously OP_NOP3
def op_checksequenceverify(stack, version, sequence):
    if sequence & (1 << 31) == (1 << 31):
        return False
    if len(stack) < 1:
        return False
    element = decode_num(stack[-1])
    if element < 0:
        return False
    if element & (1 << 31) == (1 << 31):
        if version < 2:
            return False
        elif sequence & (1 << 31) == (1 << 31):
            return False
        elif element & (1 << 22) != sequence & (1 << 22):
            return False
        elif element & 0xffff > sequence & 0xffff:
            return False
    return True

# 0xb3: 'OP_NOP4', # reserved
# 0xb4: 'OP_NOP5', # reserved
# 0xb5: 'OP_NOP6', # reserved
# 0xb6: 'OP_NOP7', # reserved
# 0xb7: 'OP_NOP8', # reserved
# 0xb8: 'OP_NOP9', # reserved
# 0xb9: 'OP_NOP10', # reserved
# 0xba: 'OP_CHECKSIGADD',

# 0xfd: 'OP_PUBKEYHASH',
# 0xfe: 'OP_PUBKEY',
# 0xff: 'OP_INVALIDOPCODE',


OP_CODE_FUNCTIONS = {
    0x00: op_0,
    # # 0x01 - 0x4b: the next opcode bytes is data to be pushed onto the stack
    # 0x4c: 'OP_PUSHDATA1',
    # 0x4d: 'OP_PUSHDATA2',
    # 0x4e: 'OP_PUSHDATA4',
    0x4f: op_1negate,
    # 0x50: 'OP_RESERVED', # reserved
    0x51: op_1,
    0x52: op_2,
    0x53: op_3,
    0x54: op_4,
    0x55: op_5,
    0x56: op_6,
    0x57: op_7,
    0x58: op_8,
    0x59: op_9,
    0x5a: op_10,
    0x5b: op_11,
    0x5c: op_12,
    0x5d: op_13,
    0x5e: op_14,
    0x5f: op_15,
    0x60: op_16,
    0x61: op_nop,
    # 0x62: 'OP_VER', # reserved
    0x63: op_if,
    0x64: op_notif,
    # 0x65: 'OP_VERIF', # reserved
    # 0x66: 'OP_VERNOTIF', # reserved
    # 0x67: 'OP_ELSE',
    # 0x68: 'OP_ENDIF',
    0x69: op_verify,
    0x6a: op_return,
    0x6b: op_toaltstack,
    0x6c: op_fromaltstack,
    0x6d: op_2drop,
    0x6e: op_2dup,
    0x6f: op_3dup,
    0x70: op_2over,
    0x71: op_2rot,
    0x72: op_2swap,
    0x73: op_ifdup,
    0x74: op_depth,
    0x75: op_drop,
    0x76: op_dup,
    0x77: op_nip,
    0x78: op_over,
    0x79: op_pick,
    0x7a: op_roll,
    0x7b: op_rot,
    0x7c: op_swap,
    0x7d: op_tuck,
    0x7e: op_disabled,
    0x7f: op_disabled,
    0x80: op_disabled,
    0x81: op_disabled,
    0x82: op_size,
    0x83: op_disabled,
    0x84: op_disabled,
    0x85: op_disabled,
    0x86: op_disabled,
    0x87: op_equal,
    0x88: op_equalverify,
    # 0x89: 'OP_RESERVED1', # reserved
    # 0x8a: 'OP_RESERVED2', # reserved
    0x8b: op_1add,
    0x8c: op_1sub,
    0x8d: op_disabled,
    0x8e: op_disabled,
    0x8f: op_negate,
    0x90: op_abs,
    0x91: op_not,
    0x92: op_0notequal,
    0x93: op_add,
    0x94: op_sub,
    0x95: op_disabled,
    0x96: op_disabled,
    0x97: op_disabled,
    0x98: op_disabled,
    0x99: op_disabled,
    0x9a: op_booland,
    0x9b: op_boolor,
    0x9c: op_numequal,
    0x9d: op_numequalverify,
    0x9e: op_numnotequal,
    0x9f: op_lessthan,
    0xa0: op_greaterthan,
    0xa1: op_lessthanorequal,
    0xa2: op_greaterthanorequal,
    0xa3: op_min,
    0xa4: op_max,
    0xa5: op_within,
    0xa6: op_ripemd160,
    0xa7: op_sha1,
    0xa8: op_sha256,
    0xa9: op_hash160,
    0xaa: op_hash256,
    # 0xab: 'OP_CODESEPARATOR',
    0xac: op_checksig,
    0xad: op_checksigverify,
    0xae: op_checkmultisig,
    0xaf: op_checkmultisigverify,
    # 0xb0: 'OP_NOP1', # reserved
    0xb1: op_checklocktimeverify,
    0xb2: op_checksequenceverify,
    # 0xb3: 'OP_NOP4', # reserved
    # 0xb4: 'OP_NOP5', # reserved
    # 0xb5: 'OP_NOP6', # reserved
    # 0xb6: 'OP_NOP7', # reserved
    # 0xb7: 'OP_NOP8', # reserved
    # 0xb8: 'OP_NOP9', # reserved
    # 0xb9: 'OP_NOP10', # reserved
    # 0xba: 'OP_CHECKSIGADD',
    # # 0xbb .. 0xfc: not assigned
    # # These words are used internally for assisting with transaction matching.
    # # They are invalid if used in actual scripts.
    # 0xfd: 'OP_PUBKEYHASH',
    # 0xfe: 'OP_PUBKEY',
    # 0xff: 'OP_INVALIDOPCODE',
}


OP_CODE_NAMES = {
    0x00: 'OP_0',
    # 0x01 - 0x4b: the next opcode bytes is data to be pushed onto the stack
    0x4c: 'OP_PUSHDATA1',
    0x4d: 'OP_PUSHDATA2',
    0x4e: 'OP_PUSHDATA4',
    0x4f: 'OP_1NEGATE',
    0x50: 'OP_RESERVED', # reserved
    0x51: 'OP_1',
    0x52: 'OP_2',
    0x53: 'OP_3',
    0x54: 'OP_4',
    0x55: 'OP_5',
    0x56: 'OP_6',
    0x57: 'OP_7',
    0x58: 'OP_8',
    0x59: 'OP_9',
    0x5a: 'OP_10',
    0x5b: 'OP_11',
    0x5c: 'OP_12',
    0x5d: 'OP_13',
    0x5e: 'OP_14',
    0x5f: 'OP_15',
    0x60: 'OP_16',
    0x61: 'OP_NOP',
    0x62: 'OP_VER', # reserved
    0x63: 'OP_IF',
    0x64: 'OP_NOTIF',
    0x65: 'OP_VERIFY', # reserved
    0x66: 'OP_VERNOTIF', # reserved
    0x67: 'OP_ELSE',
    0x68: 'OP_ENDIF',
    0x69: 'OP_VERIFY',
    0x6a: 'OP_RETURN',
    0x6b: 'OP_TOALTSTACK',
    0x6c: 'OP_FROMALTSTACK',
    0x6d: 'OP_2DROP',
    0x6e: 'OP_2DUP',
    0x6f: 'OP3DUP',
    0x70: 'OP_2OVER',
    0x71: 'OP_2ROT',
    0x72: 'OP_2SWAP',
    0x73: 'OP_IFDUP',
    0x74: 'OP_DEPTH',
    0x75: 'OP_DROP',
    0x76: 'OP_DUP',
    0x77: 'OP_NIP',
    0x78: 'OP_OVER',
    0x79: 'OP_PICK',
    0x7a: 'OP_ROLL',
    0x7b: 'OP_ROT',
    0x7c: 'OP_SWAP',
    0x7d: 'OP_TUCK',
    0x7e: 'OP_CAT',
    0x7f: 'OP_SUBSTR',
    0x80: 'OP_LEFT',
    0x81: 'OP_RIGHT',
    0x82: 'OP_SIZE',
    0x83: 'OP_INVERT',
    0x84: 'OP_AND',
    0x85: 'OP_OR',
    0x86: 'OP_XOR',
    0x87: 'OP_EQUAL',
    0x88: 'OP_EQUALVERIFY',
    0x89: 'OP_RESERVED1', # reserved
    0x8a: 'OP_RESERVED2', # reserved
    0x8b: 'OP_1ADD',
    0x8c: 'OP_1SUB',
    0x8d: 'OP_2MUL',
    0x8e: 'OP_2DIV',
    0x8f: 'OP_NEGATE',
    0x90: 'OP_ABS',
    0x91: 'OP_NOT',
    0x92: 'OP_0NOTEQUAL',
    0x93: 'OP_ADD',
    0x94: 'OP_SUB',
    0x95: 'OP_MUL',
    0x96: 'OP_DIV',
    0x97: 'OP_MOD',
    0x98: 'OP_LSHIFT',
    0x99: 'OP_RSHIFT',
    0x9a: 'OP_BOOLAND',
    0x9b: 'OP_BOOLOR',
    0x9c: 'OP_NUMEQUAL',
    0x9d: 'OP_NUMEQUALVERIFY',
    0x9e: 'OP_NUMNOTEQUAL',
    0x9f: 'OP_LESSTHAN',
    0xa0: 'OP_GREATERTHAN',
    0xa1: 'OP_LESSTHANOREQUAL',
    0xa2: 'OP_GREATERTHANOREQUAL',
    0xa3: 'OP_MIN',
    0xa4: 'OP_MAX',
    0xa5: 'OP_WITHIN',
    0xa6: 'OP_RIPEMD160',
    0xa7: 'OP_SHA1',
    0xa8: 'OP_SHA256',
    0xa9: 'OP_HASH160',
    0xaa: 'OP_HASH256',
    0xab: 'OP_CODESEPARATOR',
    0xac: 'OP_CHECKSIG',
    0xad: 'OP_CHECKSIGVERIFY',
    0xae: 'OP_CHECKMULTISIG',
    0xaf: 'OP_CHECKMULTISIGVERIFY',
    0xb0: 'OP_NOP1', # reserved
    0xb1: 'OP_CHECKLOCKTIMEVERIFY', # previously OP_NOP2
    0xb2: 'OP_CHECKSEQUENCEVERIFY', # previously OP_NOP3
    0xb3: 'OP_NOP4', # reserved
    0xb4: 'OP_NOP5', # reserved
    0xb5: 'OP_NOP6', # reserved
    0xb6: 'OP_NOP7', # reserved
    0xb7: 'OP_NOP8', # reserved
    0xb8: 'OP_NOP9', # reserved
    0xb9: 'OP_NOP10', # reserved
    0xba: 'OP_CHECKSIGADD',
    # 0xbb .. 0xfc: not assigned
    # These words are used internally for assisting with transaction matching.
    # They are invalid if used in actual scripts.
    0xfd: 'OP_PUBKEYHASH',
    0xfe: 'OP_PUBKEY',
    0xff: 'OP_INVALIDOPCODE',
}
