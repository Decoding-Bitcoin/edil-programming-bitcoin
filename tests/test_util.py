from unittest import TestCase
from pybitcoin.util import *

class UtilTest(TestCase):

    def test_little_to_big_endian(self):
        n = 0x010203040506070809
        self.assertEqual(little_endian_to_int(n.to_bytes(9, 'big')), 0x090807060504030201)

    def test_big_to_little_endian(self):
        n = 0x010203040506070809
        self.assertEqual(int_to_little_endian(n, 9), n.to_bytes(9, 'little'))
