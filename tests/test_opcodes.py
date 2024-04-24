from unittest import TestCase
from pybitcoin.opcodes import *


class OpcodesTest(TestCase):

    def _test_opcode(self, opcode, stack, expected_stack):
        self.assertTrue(OP_CODE_FUNCTIONS[opcode](stack))
        self.assertEqual(stack, expected_stack)

    def opcode_should_fail(self, opcode, stack):
        self.assertFalse(OP_CODE_FUNCTIONS[opcode](stack))

    def test_op_0(self):
        self._test_opcode(0x00, [], [b''])
        self._test_opcode(0x00, [0,1,2], [0,1,2,b''])

    def test_op_1negate(self):
        self._test_opcode(0x4f, [], [b'\x81'])
        self._test_opcode(0x4f, [0,1,2], [0,1,2,b'\x81'])

    def test_op_1_to_15(self):
        for i in range(1,17):
            with self.subTest(i=i):
                opcode = i + 0x50
                self._test_opcode(opcode, [], [i.to_bytes(1, 'little')])
                self._test_opcode(opcode, [0,1,2], [0,1,2,i.to_bytes(1, 'little')])

    def test_op_nop(self):
        self._test_opcode(0x61, [], [])

    def test_op_verify(self):
        self.opcode_should_fail(0x69, [])
        self.opcode_should_fail(0x69, [b''])
        self.opcode_should_fail(0x69, [b'\x00'])
        self._test_opcode(0x69, [b'\x01'], [])

    def test_op_dup(self):
        stack = []
        self.assertFalse(op_dup(stack))

        self._test_opcode(0x76, [0,1,2], [0,1,2,2])

    def test_op_hash160(self):
        stack = []
        self.assertFalse(op_hash160(stack))

        self._test_opcode(opcode=0xa9,
                          stack=[b'\x00'],
                          expected_stack=[bytes.fromhex('9f7fd096d37ed2c0e3f7f0cfc924beef4ffceb68')])
        self._test_opcode(opcode=0xa9,
                          stack=[2, 1, b'\x00'],
                          expected_stack=[2, 1, bytes.fromhex('9f7fd096d37ed2c0e3f7f0cfc924beef4ffceb68')])

    def test_op_hash256(self):
        stack = []
        self.assertFalse(op_hash256(stack))

        self._test_opcode(0xaa,
                          stack = [b'\x00'],
                          expected_stack = [bytes.fromhex('1406e05881e299367766d313e26c05564ec91bf721d31726bd6e46e60689539a')])
        self._test_opcode(0xaa,
                          stack = [2, 1, b'\x00'],
                          expected_stack = [2, 1, bytes.fromhex('1406e05881e299367766d313e26c05564ec91bf721d31726bd6e46e60689539a')])


if __name__ == '__main__':
    unittest.main()
