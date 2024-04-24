from pybitcoin import opcodes
from pybitcoin.util import (
    encode_varint,
    read_varint,
    little_endian_to_int,
    int_to_little_endian
)


class Script:

    def __init__(self, cmds=None):
        if cmds is None:
            self.cmds = []
        else:
            self.cmds = cmds

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
