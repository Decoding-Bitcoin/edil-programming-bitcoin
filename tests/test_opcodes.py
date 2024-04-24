from unittest import TestCase
from pybitcoin.opcodes import *


class OpcodesTest(TestCase):

    def test_op_0(self):
        stack = []
        expected = [b'']
        self.assertTrue(op_0(stack))
        self.assertEqual(stack, expected)

        stack = [0, 1, 2]
        expected = [0, 1, 2, b'']
        self.assertTrue(op_0(stack))
        self.assertEqual(stack, expected)

    def test_op_1negate(self):
        stack = []
        expected = [b'\x81']
        self.assertTrue(op_1negate(stack))
        self.assertEqual(stack, expected)

        stack = [0, 1, 2]
        expected = [0, 1, 2, b'\x81']
        self.assertTrue(op_1negate(stack))
        self.assertEqual(stack, expected)

    def test_op_1_to_15(self):
        for i in range(1,16):
            with self.subTest(i=i):
                opcode = i + 0x50

                stack = []
                expected = [i.to_bytes(1, 'little')]
                self.assertTrue(OP_CODE_FUNCTIONS[opcode](stack))
                self.assertEqual(stack, expected)

                stack = [0, 1, 2]
                expected = [0, 1, 2, i.to_bytes(1, 'little')]
                self.assertTrue(OP_CODE_FUNCTIONS[opcode](stack))
                self.assertEqual(stack, expected)

    def test_op_dup(self):
        stack = []
        self.assertFalse(op_dup(stack))

        stack = [0,1,2]
        self.assertTrue(op_dup(stack))
        self.assertEqual(stack, [0,1,2,2])

    def test_op_hash160(self):
        stack = []
        self.assertFalse(op_hash160(stack))

        stack = [b'\x00']
        expected_stack = [bytes.fromhex('9f7fd096d37ed2c0e3f7f0cfc924beef4ffceb68')]
        self.assertTrue(op_hash160(stack))
        self.assertEqual(stack, expected_stack)

        stack = [2, 1, b'\x00']
        expected_stack = [2, 1, bytes.fromhex('9f7fd096d37ed2c0e3f7f0cfc924beef4ffceb68')]
        self.assertTrue(op_hash160(stack))
        self.assertEqual(stack, expected_stack)

    def test_op_hash256(self):
        stack = []
        self.assertFalse(op_hash256(stack))

        stack = [b'\x00']
        expected_stack = [bytes.fromhex('1406e05881e299367766d313e26c05564ec91bf721d31726bd6e46e60689539a')]
        self.assertTrue(op_hash256(stack))
        self.assertEqual(stack, expected_stack)

        stack = [2, 1, b'\x00']
        expected_stack = [2, 1, bytes.fromhex('1406e05881e299367766d313e26c05564ec91bf721d31726bd6e46e60689539a')]
        self.assertTrue(op_hash256(stack))
        self.assertEqual(stack, expected_stack)
