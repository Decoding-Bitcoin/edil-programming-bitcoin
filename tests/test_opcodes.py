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

    def test_op_toaltstack(self):
        op_toaltstack = 0x6b

        stack = []
        altstack = []
        self.assertFalse(OP_CODE_FUNCTIONS[op_toaltstack](stack, altstack))

        stack = []
        altstack = [0,1]
        self.assertFalse(OP_CODE_FUNCTIONS[op_toaltstack](stack, altstack))

        stack = [0]
        expected_stack = []
        altstack = []
        expected_altstack = [0]
        self.assertTrue(OP_CODE_FUNCTIONS[op_toaltstack](stack, altstack))
        self.assertEqual(stack, expected_stack)
        self.assertEqual(altstack, expected_altstack)

        stack = [0,1,2]
        expected_stack = [0,1]
        altstack = [3,4,5]
        expected_altstack = [3,4,5,2]
        self.assertTrue(OP_CODE_FUNCTIONS[op_toaltstack](stack, altstack))
        self.assertEqual(stack, expected_stack)
        self.assertEqual(altstack, expected_altstack)


    def test_op_fromaltstack(self):
        op_fromaltstack = 0x6c

        stack = []
        altstack = []
        self.assertFalse(OP_CODE_FUNCTIONS[op_fromaltstack](stack, altstack))

        stack = [0,1]
        altstack = []
        self.assertFalse(OP_CODE_FUNCTIONS[op_fromaltstack](stack, altstack))

        stack = []
        expected_stack = [0]
        altstack = [0]
        expected_altstack = []
        self.assertTrue(OP_CODE_FUNCTIONS[op_fromaltstack](stack, altstack))
        self.assertEqual(stack, expected_stack)
        self.assertEqual(altstack, expected_altstack)

        stack = [0,1,2]
        expected_stack = [0,1,2,5]
        altstack = [3,4,5]
        expected_altstack = [3,4]
        self.assertTrue(OP_CODE_FUNCTIONS[op_fromaltstack](stack, altstack))
        self.assertEqual(stack, expected_stack)
        self.assertEqual(altstack, expected_altstack)


    def test_op_2drop(self):
        op_2drop = 0x6d
        self.opcodeShouldFail(op_2drop, [])
        self.opcodeShouldFail(op_2drop, [0])
        self.opcodeShouldSucceed(op_2drop, [0,1], [])
        self.opcodeShouldSucceed(op_2drop, [0,1,2], [0])

    def test_op_2dup(self):
        op_2dup = 0x6e
        self.opcodeShouldFail(op_2dup, [])
        self.opcodeShouldFail(op_2dup, [0])
        self.opcodeShouldSucceed(op_2dup, [0,1], [0,1,0,1])

    def test_op_3dup(self):
        op_3dup = 0x6f
        self.opcodeShouldFail(op_3dup, [])
        self.opcodeShouldFail(op_3dup, [0])
        self.opcodeShouldFail(op_3dup, [0,1])
        self.opcodeShouldSucceed(op_3dup, [0,1,2], [0,1,2,0,1,2])

    def test_op_2over(self):
        op_2over = 0x70
        self.opcodeShouldFail(op_2over, [])
        self.opcodeShouldFail(op_2over, [0])
        self.opcodeShouldFail(op_2over, [0,1])
        self.opcodeShouldFail(op_2over, [0,1,2])
        self.opcodeShouldSucceed(op_2over, [0,1,2,3], [0,1,2,3,0,1])

    def test_op_2rot(self):
        op_2rot = 0x71
        self.opcodeShouldFail(op_2rot, [])
        self.opcodeShouldFail(op_2rot, [0])
        self.opcodeShouldFail(op_2rot, [0,1])
        self.opcodeShouldFail(op_2rot, [0,1,2])
        self.opcodeShouldFail(op_2rot, [0,1,2,3])
        self.opcodeShouldFail(op_2rot, [0,1,2,3,4])
        self.opcodeShouldSucceed(op_2rot, [0,1,2,3,4,5], [2,3,4,5,0,1])

    def test_op_2swap(self):
        op_2swap = 0x72
        self.opcodeShouldFail(op_2swap, [])
        self.opcodeShouldFail(op_2swap, [0])
        self.opcodeShouldFail(op_2swap, [0,1])
        self.opcodeShouldFail(op_2swap, [0,1,2])
        self.opcodeShouldSucceed(op_2swap, [0,1,2,3], [2,3,0,1])
        self.opcodeShouldSucceed(op_2swap, [0,1,2,3,4], [0,3,4,1,2])

    def test_op_ifdup(self):
        op_ifdup = 0x73
        self.opcodeShouldFail(op_ifdup, [])
        self.opcodeShouldSucceed(op_ifdup, [b''], [b''])
        self.opcodeShouldSucceed(op_ifdup, [b'\x00'], [b'\x00'])
        self.opcodeShouldSucceed(op_ifdup, [b'\x01'], [b'\x01', b'\x01'])

    def test_op_depth(self):
        op_depth = 0x74
        self.opcodeShouldSucceed(op_depth, [], [b''])
        self.opcodeShouldSucceed(op_depth, [0,1,2], [0,1,2,b'\x03'])

    def test_op_drop(self):
        op_drop = 0x75
        self.opcodeShouldFail(op_drop, [])
        self.opcodeShouldSucceed(op_drop, [0], [])
        self.opcodeShouldSucceed(op_drop, [0,1,2], [0,1])

    def test_op_dup(self):
        self.opcodeShouldFail(0x76, [])
        self.opcodeShouldSucceed(0x76, [0,1,2], [0,1,2,2])

    def test_op_nip(self):
        op_nip = 0x77
        self.opcodeShouldFail(op_nip, [])
        self.opcodeShouldFail(op_nip, [0])
        self.opcodeShouldSucceed(op_nip, [0,1], [1])
        self.opcodeShouldSucceed(op_nip, [0,1,2], [0,2])

    def test_op_over(self):
        op_over = 0x78
        self.opcodeShouldFail(op_over, [])
        self.opcodeShouldFail(op_over, [0])
        self.opcodeShouldSucceed(op_over, [0, 1], [0, 1, 0])

    def test_op_pick(self):
        op_pick = 0x79
        self.opcodeShouldFail(op_pick, [])
        self.opcodeShouldFail(op_pick, [b'\x01'])
        self.opcodeShouldFail(op_pick, [0, b'\x01'])
        self.opcodeShouldFail(op_pick, [b''])
        self.opcodeShouldSucceed(op_pick, [0, b''], [0,0])
        self.opcodeShouldSucceed(op_pick, [0, 1, b'\x01'], [0,1,0])
        self.opcodeShouldSucceed(op_pick, [0, 1, b'\x00'], [0,1,1])
        self.opcodeShouldSucceed(op_pick, [0, 1, 2, 3, b'\x01'], [0,1,2,3,2])

    def test_op_pick(self):
        op_roll = 0x7a
        self.opcodeShouldFail(op_roll, [])
        self.opcodeShouldFail(op_roll, [b'\x01'])
        self.opcodeShouldFail(op_roll, [0, b'\x01'])
        self.opcodeShouldFail(op_roll, [b''])
        self.opcodeShouldSucceed(op_roll, [0, b''], [0])
        self.opcodeShouldSucceed(op_roll, [0, 1, b'\x01'], [1,0])
        self.opcodeShouldSucceed(op_roll, [0, 1, b'\x00'], [0,1])
        self.opcodeShouldSucceed(op_roll, [0, 1, 2, 3, b'\x01'], [0,1,3,2])

    def test_op_rot(self):
        op_rot = 0x7b
        self.opcodeShouldFail(op_rot, [])
        self.opcodeShouldFail(op_rot, [0])
        self.opcodeShouldFail(op_rot, [0,1])
        self.opcodeShouldSucceed(op_rot, [0,1,2], [1,2,0])

    def test_op_swap(self):
        op_swap = 0x7c
        self.opcodeShouldFail(op_swap, [])
        self.opcodeShouldFail(op_swap, [0])
        self.opcodeShouldSucceed(op_swap, [0,1], [1,0])
        self.opcodeShouldSucceed(op_swap, [0,1,2], [0,2,1])

    def test_op_tuck(self):
        op_tuck = 0x7d
        self.opcodeShouldFail(op_tuck, [])
        self.opcodeShouldFail(op_tuck, [0])
        self.opcodeShouldSucceed(op_tuck, [0,1], [1,0,1])
        self.opcodeShouldSucceed(op_tuck, [0,1,2], [0,2,1,2])

    def test_op_size(self):
        op_size = 0x82
        self.opcodeShouldFail(op_size, [])
        self.opcodeShouldSucceed(op_size, [b''], [b'', b''])
        self.opcodeShouldSucceed(op_size, [b'\x01\x02'], [b'\x01\x02', b'\x02'])
        self.opcodeShouldSucceed(op_size, [0,1,b'\x01\x02'], [0,1,b'\x01\x02', b'\x02'])

    def test_op_equal(self):
        op_equal = 0x87
        self.opcodeShouldFail(op_equal, [])
        self.opcodeShouldFail(op_equal, [0])
        self.opcodeShouldSucceed(op_equal, [0,1], [b''])
        self.opcodeShouldSucceed(op_equal, [0,1,2], [0, b''])
        self.opcodeShouldSucceed(op_equal, [0,0], [b'\x01'])
        self.opcodeShouldSucceed(op_equal, [0,1,1], [0, b'\x01'])

    def test_op_equalverify(self):
        op_equal = 0x88
        self.opcodeShouldFail(op_equal, [])
        self.opcodeShouldFail(op_equal, [0])
        self.opcodeShouldFail(op_equal, [0,1])
        self.opcodeShouldFail(op_equal, [0,1,2])
        self.opcodeShouldSucceed(op_equal, [0,0], [])
        self.opcodeShouldSucceed(op_equal, [0,1,1], [0])

    def test_op_1add(self):
        op_1add = 0x8b
        self.opcodeShouldFail(op_1add, [])
        self.opcodeShouldSucceed(op_1add, [b''], [b'\x01'])
        self.opcodeShouldSucceed(op_1add, [0, 1, b''], [0, 1, b'\x01'])
        self.opcodeShouldSucceed(op_1add, [0, 1, b'\xfe\xff\xff\x7f'], [0, 1, b'\xff\xff\xff\x7f'])

    def test_op_1sub(self):
        op_1sub = 0x8c
        self.opcodeShouldFail(op_1sub, [])
        self.opcodeShouldSucceed(op_1sub, [b'\x01'], [b''])
        self.opcodeShouldSucceed(op_1sub, [b''], [b'\x81'])
        self.opcodeShouldSucceed(op_1sub, [0, 1, b'\x01'], [0, 1, b''])
        self.opcodeShouldSucceed(op_1sub, [0, 1, b'\xfe\xff\xff\x7f'], [0, 1, b'\xfd\xff\xff\x7f'])

    def test_op_negate(self):
        op_negate = 0x8f
        self.opcodeShouldFail(op_negate, [])
        self.opcodeShouldSucceed(op_negate, [b''], [b''])
        self.opcodeShouldSucceed(op_negate, [b'\x01'], [b'\x81'])
        self.opcodeShouldSucceed(op_negate, [0,1,b'\x01'], [0,1,b'\x81'])
        self.opcodeShouldSucceed(op_negate, [0,1,b'\xff'], [0,1,b'\x7f'])

    def test_op_abs(self):
        op_abs = 0x90
        self.opcodeShouldFail(op_abs, [])
        self.opcodeShouldSucceed(op_abs, [b''], [b''])
        self.opcodeShouldSucceed(op_abs, [b'\x01'], [b'\x01'])
        self.opcodeShouldSucceed(op_abs, [0,1,b'\x81'], [0,1,b'\x01'])
        self.opcodeShouldSucceed(op_abs, [0,1,b'\xff'], [0,1,b'\x7f'])
        self.opcodeShouldSucceed(op_abs, [0,1,b'\x7f'], [0,1,b'\x7f'])

    def test_op_not(self):
        op_not = 0x91
        self.opcodeShouldFail(op_not, [])
        self.opcodeShouldSucceed(op_not, [b''], [b'\x01'])
        self.opcodeShouldSucceed(op_not, [b'\x01'], [b''])
        self.opcodeShouldSucceed(op_not, [0,1,b'\x01'], [0,1,b''])
        self.opcodeShouldSucceed(op_not, [0,1,b'\xff'], [0,1,b''])

    def test_op_0notequal(self):
        op_0notequal = 0x92
        self.opcodeShouldFail(op_0notequal, [])
        self.opcodeShouldSucceed(op_0notequal, [b''], [b''])
        self.opcodeShouldSucceed(op_0notequal, [b'\x01'], [b'\x01'])
        self.opcodeShouldSucceed(op_0notequal, [0,1,b'\x01'], [0,1,b'\x01'])
        self.opcodeShouldSucceed(op_0notequal, [0,1,b'\xff'], [0,1,b'\x01'])

    def test_op_add(self):
        op_add = 0x93
        self.opcodeShouldFail(op_add, [])
        self.opcodeShouldFail(op_add, [0])
        self.opcodeShouldSucceed(op_add, [b'', b''], [b''])
        self.opcodeShouldSucceed(op_add, [0,1,b'', b''], [0,1,b''])
        self.opcodeShouldSucceed(op_add, [0,1,b'\x01', b'\x81'], [0,1,b''])
        self.opcodeShouldSucceed(op_add, [0,1,b'\x01', b'\x01'], [0,1,b'\x02'])

    def test_op_sub(self):
        op_sub = 0x94
        self.opcodeShouldFail(op_sub, [])
        self.opcodeShouldFail(op_sub, [0])
        self.opcodeShouldSucceed(op_sub, [b'', b''], [b''])
        self.opcodeShouldSucceed(op_sub, [0,1,b'', b''], [0,1,b''])
        self.opcodeShouldSucceed(op_sub, [0,1,b'\x01', b'\x81'], [0,1,b'\x02'])
        self.opcodeShouldSucceed(op_sub, [0,1,b'\x01', b'\x01'], [0,1,b''])

    def test_op_booland(self):
        op_booland = 0x9a
        self.opcodeShouldFail(op_booland, [])
        self.opcodeShouldFail(op_booland, [0])
        self.opcodeShouldSucceed(op_booland, [b'', b''], [b''])
        self.opcodeShouldSucceed(op_booland, [b'', b'\x01'], [b''])
        self.opcodeShouldSucceed(op_booland, [b'\x01', b''], [b''])
        self.opcodeShouldSucceed(op_booland, [b'\x01', b'\x01'], [b'\x01'])
        self.opcodeShouldSucceed(op_booland, [0,1,b'\x02', b'\x03'], [0,1,b'\x01'])

    def test_op_boolor(self):
        op_boolor = 0x9b
        self.opcodeShouldFail(op_boolor, [])
        self.opcodeShouldFail(op_boolor, [0])
        self.opcodeShouldSucceed(op_boolor, [b'', b''], [b''])
        self.opcodeShouldSucceed(op_boolor, [b'', b'\x01'], [b'\x01'])
        self.opcodeShouldSucceed(op_boolor, [b'\x01', b''], [b'\x01'])
        self.opcodeShouldSucceed(op_boolor, [b'\x01', b'\x01'], [b'\x01'])
        self.opcodeShouldSucceed(op_boolor, [0,1,b'\x02', b'\x03'], [0,1,b'\x01'])

    def test_op_numequal(self):
        op_numequal = 0x9c
        self.opcodeShouldFail(op_numequal, [])
        self.opcodeShouldFail(op_numequal, [0])
        self.opcodeShouldSucceed(op_numequal, [b'', b''], [b'\x01'])
        self.opcodeShouldSucceed(op_numequal, [b'', b'\x01'], [b''])
        self.opcodeShouldSucceed(op_numequal, [0,1,b'', b'\x01'], [0,1,b''])

    def test_op_numequalverify(self):
        op_numequal = 0x9d
        self.opcodeShouldFail(op_numequal, [])
        self.opcodeShouldFail(op_numequal, [0])
        self.opcodeShouldSucceed(op_numequal, [b'', b''], [])
        self.opcodeShouldFail(op_numequal, [b'', b'\x01'])
        self.opcodeShouldFail(op_numequal, [0,1,b'', b'\x01'])
        self.opcodeShouldSucceed(op_numequal, [0,1,b'\x01', b'\x01'], [0,1])

    def test_op_numnotequal(self):
        op_numequal = 0x9e
        self.opcodeShouldFail(op_numequal, [])
        self.opcodeShouldFail(op_numequal, [0])
        self.opcodeShouldSucceed(op_numequal, [b'', b''], [b''])
        self.opcodeShouldSucceed(op_numequal, [b'', b'\x01'], [b'\x01'])
        self.opcodeShouldSucceed(op_numequal, [0,1,b'', b'\x01'], [0,1,b'\x01'])

    def test_op_lessthan(self):
        op_lessthan = 0x9f
        self.opcodeShouldFail(op_lessthan, [])
        self.opcodeShouldFail(op_lessthan, [0])
        self.opcodeShouldSucceed(op_lessthan, [b'', b''], [b''])
        self.opcodeShouldSucceed(op_lessthan, [b'', b'\x01'], [b'\x01'])
        self.opcodeShouldSucceed(op_lessthan, [0,1,b'', b'\x01'], [0,1,b'\x01'])

    def test_op_greaterthan(self):
        op_greaterthan = 0xa0
        self.opcodeShouldFail(op_greaterthan, [])
        self.opcodeShouldFail(op_greaterthan, [0])
        self.opcodeShouldSucceed(op_greaterthan, [b'', b''], [b''])
        self.opcodeShouldSucceed(op_greaterthan, [b'', b'\x01'], [b''])
        self.opcodeShouldSucceed(op_greaterthan, [b'\x02', b'\x01'], [b'\x01'])
        self.opcodeShouldSucceed(op_greaterthan, [0,1,b'\x02', b'\x01'], [0,1,b'\x01'])

    def test_op_lessthanorequal(self):
        op_lessthanorequal = 0xa1
        self.opcodeShouldFail(op_lessthanorequal, [])
        self.opcodeShouldFail(op_lessthanorequal, [0])
        self.opcodeShouldSucceed(op_lessthanorequal, [b'', b''], [b'\x01'])
        self.opcodeShouldSucceed(op_lessthanorequal, [b'', b'\x01'], [b'\x01'])
        self.opcodeShouldSucceed(op_lessthanorequal, [b'\x02', b'\x01'], [b''])
        self.opcodeShouldSucceed(op_lessthanorequal, [0,1,b'', b'\x01'], [0,1,b'\x01'])

    def test_op_greaterthanorequal(self):
        op_greaterthanorequal = 0xa2
        self.opcodeShouldFail(op_greaterthanorequal, [])
        self.opcodeShouldFail(op_greaterthanorequal, [0])
        self.opcodeShouldSucceed(op_greaterthanorequal, [b'', b''], [b'\x01'])
        self.opcodeShouldSucceed(op_greaterthanorequal, [b'', b'\x01'], [b''])
        self.opcodeShouldSucceed(op_greaterthanorequal, [b'\x02', b'\x01'], [b'\x01'])
        self.opcodeShouldSucceed(op_greaterthanorequal, [0,1,b'\x02', b'\x01'], [0,1,b'\x01'])


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
