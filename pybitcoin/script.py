from logging import getLogger

from pybitcoin.opcodes import OP_CODE_FUNCTIONS, OP_CODE_NAMES
from pybitcoin.util import (
    encode_varint,
    read_varint,
    little_endian_to_int,
    int_to_little_endian
)

LOGGER = getLogger(__name__)


class Script:

    def __init__(self, cmds=None):
        if cmds is None:
            self.cmds = []
        else:
            self.cmds = cmds

    def __repr__(self):
        result = []
        for cmd in self.cmds:
            if type(cmd) == int:
                if OP_CODE_NAMES.get(cmd):
                    name = OP_CODE_NAMES.get(cmd)
                else:
                    name = 'OP_[{}]'.format(cmd)
                result.append(name)
            else:
                result.append(cmd.hex())
        return ' '.join(result)

    def __add__(self, other):
        return Script(self.cmds + other.cmds)

    def evaluate(self, z):
        cmds = self.cmds[:]   # copy cmds list, it will mutate
        stack = []
        altstack = []
        while len(cmds) > 0:
            cmd = cmds.pop(0)
            if type(cmd) == int:
                operation = OP_CODE_FUNCTIONS[cmd]

                # OP_IF and OP_NOTIF
                if cmd in (0x63,0x64):
                    if not operation(stack, cmds):
                        LOGGER.info('bad op: {}'.format(OP_CODE_NAMES[cmd]))
                        return False

                # OP_TOALTSTACK and OP_FROMALTSTACK
                elif cmd in (0x6b, 0x6c):
                    if not operation(stack, altstack):
                        LOGGER.info('bad op: {}'.format(OP_CODE_NAMES[cmd]))
                        return False

                # OP_CHECKSIG, OP_CHECKSIGVERIFY,
                # OP_CHECKMULTISIG, OP_CHECKMULTISIGVERIFY
                elif cmd in (0xac, 0xad, 0xae, 0xaf):
                    if not operation(stack, z):
                        LOGGER.info('bad op: {}'.format(OP_CODE_NAMES[cmd]))
                        return False

                else:
                    if not operation(stack):
                        LOGGER.info('bad op: {}'.format(OP_CODE_NAMES[cmd]))
                        return False

            # element (not opcode), push to stack
            else:
                stack.append(cmd)

        # if stack is empty at the end, script fails
        if len(stack) == 0:
            return False
        # if stack's top element is empty (zero), script fails
        if stack.pop == b'':
            return False
        # otherwise, scrip succeeds
        return True
    
    @classmethod
    def parse(cls, s):
        length = read_varint(s)
        cmds = []
        count = 0
        while count < length:
            current = s.read(1)
            count += 1
            current_byte = current[0]

            # for bytes between 0x01 and 0x4b (75), next n bytes are an element
            if current_byte >= 0x01 and current_byte <= 0x4b:
                n = current_byte
                cmds.append(s.read(n))
                count += n

            # 0x4c is OP_PUSHDATA1
            elif current_byte == 0x4c:
                data_length = little_endian_to_int(s.read(1))
                cmds.append(s.read(data_length))
                count += data_length + 1

            # 0x4d is OP_PUSHDATA2
            elif current_byte == 0x4d:
                data_length = little_endian_to_int(s.read(2))
                cmds.append(s.read(data_length))
                count += data_length + 2

            # we have an opcode to store
            else:
                op_code = current_byte
                cmds.append(op_code)

        if count != length:
            raise SyntaxError('parsing script failed')

        return cls(cmds)


    def raw_serialize(self):
        result = b''
        for cmd in self.cmds:
            # cmd is an opcode
            if type(cmd) == int:
                result += int_to_little_endian(cmd, 1)
            # cmd is data
            else:
                length = len(cmd)
                # push data directly
                if length < 75:
                    result += int_to_little_endian(length, 1)
                # use OP_PUSHDATA1
                elif length > 75 and length < 0x100:
                    result += int_to_little_endian(76, 1)
                    result += int_to_little_endian(length, 1)
                # use OP_PUSHDATA2
                elif length >= 0x100 and length <= 520:
                    result += int_to_little_endian(77,1)
                    result += int_to_little_endian(length, 2)
                else:
                    raise ValueError('too long an cmd')
                result += cmd
        return result

    def serialize(self):
        result = self.raw_serialize()
        total = len(result)
        return encode_varint(total) + result
