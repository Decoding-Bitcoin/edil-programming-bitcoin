from pybitcoin.hash import hash160, hash256


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
# 0x63: 'OP_IF',
# 0x64: 'OP_NOTIF',
# 0x65: 'OP_VERIFY', # reserved
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

# 0x6b: 'OP_TOALTSTACK',
# 0x6c: 'OP_FROMALTSTACK',
# 0x6d: 'OP_2DROP',
# 0x6e: 'OP_2DUP',
# 0x6f: 'OP3DUP',
# 0x70: 'OP_2OVER',
# 0x71: 'OP_2ROT',
# 0x72: 'OP_2SWAP',

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

# 0x75: 'OP_DROP',

# 0x76: OP_DUP
def op_dup(stack):
    if len(stack) < 1:
        return False
    stack.append(stack[-1])
    return True

# 0x77: 'OP_NIP',
# 0x78: 'OP_OVER',
# 0x79: 'OP_PICK',
# 0x7a: 'OP_ROLL',
# 0x7b: 'OP_ROT',
# 0x7c: 'OP_SWAP',
# 0x7d: 'OP_TUCK',
# 0x7e: 'OP_CAT',
# 0x7f: 'OP_SUBSTR',
# 0x80: 'OP_LEFT',
# 0x81: 'OP_RIGHT',
# 0x82: 'OP_SIZE',
# 0x83: 'OP_INVERT',
# 0x84: 'OP_AND',
# 0x85: 'OP_OR',
# 0x86: 'OP_XOR',
# 0x87: 'OP_EQUAL',
# 0x88: 'OP_EQUALVERIFY',
# 0x89: 'OP_RESERVED1', # reserved
# 0x8a: 'OP_RESERVED2', # reserved
# 0x8b: 'OP_1ADD',
# 0x8c: 'OP_1SUB',
# 0x8d: 'OP_2MUL',
# 0x8e: 'OP_2DIV',
# 0x8f: 'OP_NEGATE',
# 0x90: 'OP_ABS',
# 0x91: 'OP_NOT',
# 0x92: 'OP_0NOTEQUAL',
# 0x93: 'OP_ADD',
# 0x94: 'OP_SUB',
# 0x95: 'OP_MUL',
# 0x96: 'OP_DIV',
# 0x97: 'OP_MOD',
# 0x98: 'OP_LSHIFT',
# 0x99: 'OP_RSHIFT',
# 0x9a: 'OP_BOOLAND',
# 0x9b: 'OP_BOOLOR',
# 0x9c: 'OP_NUMEQUAL',
# 0x9d: 'OP_NUMEQUALVERIFY',
# 0x9e: 'OP_NUMNOTEQUAL',
# 0x9f: 'OP_LESSTHAN',
# 0xa0: 'OP_GREATERTHAN',
# 0xa1: 'OP_LESSTHANOREQUAL',
# 0xa2: 'OP_GREATERTHANOREQUAL',
# 0xa3: 'OP_MIN',
# 0xa4: 'OP_MAX',
# 0xa5: 'OP_WITHIN',
# 0xa6: 'OP_RIPEMD160',
# 0xa7: 'OP_SHA1',
# 0xa8: 'OP_SHA256',

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
# 0xac: 'OP_CHECKSIG',
# 0xad: 'OP_CHECKSIGVERIFY',
# 0xae: 'OP_CHECKMULTISIG',
# 0xaf: 'OP_CHECKMULTISIGVERIFY',
# 0xb0: 'OP_NOP1', # reserved
# 0xb1: 'OP_CHECKLOCKTIMEVERIFY', # previously OP_NOP2
# 0xb2: 'OP_CHECKSEQUENCEVERIFY', # previously OP_NOP3
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
    # 0x63: 'OP_IF',
    # 0x64: 'OP_NOTIF',
    # 0x65: 'OP_VERIFY', # reserved
    # 0x66: 'OP_VERNOTIF', # reserved
    # 0x67: 'OP_ELSE',
    # 0x68: 'OP_ENDIF',
    0x69: op_verify,
    0x6a: op_return,
    # 0x6b: 'OP_TOALTSTACK',
    # 0x6c: 'OP_FROMALTSTACK',
    # 0x6d: 'OP_2DROP',
    # 0x6e: 'OP_2DUP',
    # 0x6f: 'OP3DUP',
    # 0x70: 'OP_2OVER',
    # 0x71: 'OP_2ROT',
    # 0x72: 'OP_2SWAP',
    0x73: op_ifdup,
    0x74: op_depth,
    # 0x75: 'OP_DROP',
    0x76: op_dup,
    # 0x77: 'OP_NIP',
    # 0x78: 'OP_OVER',
    # 0x79: 'OP_PICK',
    # 0x7a: 'OP_ROLL',
    # 0x7b: 'OP_ROT',
    # 0x7c: 'OP_SWAP',
    # 0x7d: 'OP_TUCK',
    # 0x7e: 'OP_CAT',
    # 0x7f: 'OP_SUBSTR',
    # 0x80: 'OP_LEFT',
    # 0x81: 'OP_RIGHT',
    # 0x82: 'OP_SIZE',
    # 0x83: 'OP_INVERT',
    # 0x84: 'OP_AND',
    # 0x85: 'OP_OR',
    # 0x86: 'OP_XOR',
    # 0x87: 'OP_EQUAL',
    # 0x88: 'OP_EQUALVERIFY',
    # 0x89: 'OP_RESERVED1', # reserved
    # 0x8a: 'OP_RESERVED2', # reserved
    # 0x8b: 'OP_1ADD',
    # 0x8c: 'OP_1SUB',
    # 0x8d: 'OP_2MUL',
    # 0x8e: 'OP_2DIV',
    # 0x8f: 'OP_NEGATE',
    # 0x90: 'OP_ABS',
    # 0x91: 'OP_NOT',
    # 0x92: 'OP_0NOTEQUAL',
    # 0x93: 'OP_ADD',
    # 0x94: 'OP_SUB',
    # 0x95: 'OP_MUL',
    # 0x96: 'OP_DIV',
    # 0x97: 'OP_MOD',
    # 0x98: 'OP_LSHIFT',
    # 0x99: 'OP_RSHIFT',
    # 0x9a: 'OP_BOOLAND',
    # 0x9b: 'OP_BOOLOR',
    # 0x9c: 'OP_NUMEQUAL',
    # 0x9d: 'OP_NUMEQUALVERIFY',
    # 0x9e: 'OP_NUMNOTEQUAL',
    # 0x9f: 'OP_LESSTHAN',
    # 0xa0: 'OP_GREATERTHAN',
    # 0xa1: 'OP_LESSTHANOREQUAL',
    # 0xa2: 'OP_GREATERTHANOREQUAL',
    # 0xa3: 'OP_MIN',
    # 0xa4: 'OP_MAX',
    # 0xa5: 'OP_WITHIN',
    # 0xa6: 'OP_RIPEMD160',
    # 0xa7: 'OP_SHA1',
    # 0xa8: 'OP_SHA256',
    0xa9: op_hash160,
    0xaa: op_hash256,
    # 0xab: 'OP_CODESEPARATOR',
    # 0xac: 'OP_CHECKSIG',
    # 0xad: 'OP_CHECKSIGVERIFY',
    # 0xae: 'OP_CHECKMULTISIG',
    # 0xaf: 'OP_CHECKMULTISIGVERIFY',
    # 0xb0: 'OP_NOP1', # reserved
    # 0xb1: 'OP_CHECKLOCKTIMEVERIFY', # previously OP_NOP2
    # 0xb2: 'OP_CHECKSEQUENCEVERIFY', # previously OP_NOP3
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
