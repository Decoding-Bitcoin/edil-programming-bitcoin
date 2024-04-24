from unittest import TestCase
from pybitcoin.opcodes import *


class OpcodesTest(TestCase):

    def opcodeShouldSucceed(self, opcode, stack, expected_stack):
        self.assertTrue(OP_CODE_FUNCTIONS[opcode](stack))
        self.assertEqual(stack, expected_stack)

    def opcodeShouldFail(self, opcode, stack):
        self.assertFalse(OP_CODE_FUNCTIONS[opcode](stack))

    def test_op_0(self):
        self.opcodeShouldSucceed(0x00, [], [b''])
        self.opcodeShouldSucceed(0x00, [0,1,2], [0,1,2,b''])

    def test_op_1negate(self):
        self.opcodeShouldSucceed(0x4f, [], [b'\x81'])
        self.opcodeShouldSucceed(0x4f, [0,1,2], [0,1,2,b'\x81'])

    def test_op_1_to_15(self):
        for i in range(1,17):
            with self.subTest(i=i):
                opcode = i + 0x50
                self.opcodeShouldSucceed(opcode, [], [i.to_bytes(1, 'little')])
                self.opcodeShouldSucceed(opcode, [0,1,2], [0,1,2,i.to_bytes(1, 'little')])

    def test_op_nop(self):
        self.opcodeShouldSucceed(0x61, [], [])

    def test_op_verify(self):
        self.opcodeShouldFail(0x69, [])
        self.opcodeShouldFail(0x69, [b''])
        self.opcodeShouldFail(0x69, [b'\x00'])
        self.opcodeShouldSucceed(0x69, [b'\x01'], [])

    def test_op_return(self):
        self.opcodeShouldFail(0x6a, [])
        self.opcodeShouldFail(0x6a, [b'\x00'])

    def test_op_ifdup(self):
        op_ifdup = 0x73
        self.opcodeShouldFail(op_ifdup, [])
        self.opcodeShouldSucceed(op_ifdup, [b''], [b''])
        self.opcodeShouldSucceed(op_ifdup, [b'\x00'], [b'\x00'])
        self.opcodeShouldSucceed(op_ifdup, [b'\x01'], [b'\x01', b'\x01'])

    def test_op_dup(self):
        self.opcodeShouldFail(0x76, [])
        self.opcodeShouldSucceed(0x76, [0,1,2], [0,1,2,2])

    def test_op_hash160(self):
        self.opcodeShouldFail(0xa9, [])
        self.opcodeShouldSucceed(opcode=0xa9,
                                 stack=[b'\x00'],
                          expected_stack=[bytes.fromhex('9f7fd096d37ed2c0e3f7f0cfc924beef4ffceb68')])
        self.opcodeShouldSucceed(opcode=0xa9,
                                 stack=[2, 1, b'\x00'],
                                 expected_stack=[2, 1, bytes.fromhex('9f7fd096d37ed2c0e3f7f0cfc924beef4ffceb68')])

    def test_op_hash256(self):
        self.opcodeShouldFail(0xaa, [])
        self.opcodeShouldSucceed(0xaa,
                          stack = [b'\x00'],
                          expected_stack = [bytes.fromhex('1406e05881e299367766d313e26c05564ec91bf721d31726bd6e46e60689539a')])
        self.opcodeShouldSucceed(0xaa,
                          stack = [2, 1, b'\x00'],
                          expected_stack = [2, 1, bytes.fromhex('1406e05881e299367766d313e26c05564ec91bf721d31726bd6e46e60689539a')])


if __name__ == '__main__':
    unittest.main()
