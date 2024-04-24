from unittest import TestCase
from io import BytesIO
from pybitcoin.util import *

class UtilTest(TestCase):

    def test_little_to_big_endian(self):
        n = 0x010203040506070809
        self.assertEqual(little_endian_to_int(n.to_bytes(9, 'big')), 0x090807060504030201)

    def test_big_to_little_endian(self):
        n = 0x010203040506070809
        self.assertEqual(int_to_little_endian(n, 9), n.to_bytes(9, 'little'))

    def test_read_varint(self):
        n = bytes.fromhex('64')
        stream = BytesIO(n)
        self.assertEqual(read_varint(stream), 100)

        n = bytes.fromhex('fdff00')
        stream = BytesIO(n)
        self.assertEqual(read_varint(stream), 255)

        n = bytes.fromhex('fd2b02')
        stream = BytesIO(n)
        self.assertEqual(read_varint(stream), 555)

        n = bytes.fromhex('fe7f110100')
        stream = BytesIO(n)
        self.assertEqual(read_varint(stream), 70015)

        n = bytes.fromhex('ff6dc7ed3e60100000')
        stream = BytesIO(n)
        self.assertEqual(read_varint(stream), 18005558675309)

    def test_encode_varint(self):
        n = bytes.fromhex('64')
        self.assertEqual(n, encode_varint(100))

        n = bytes.fromhex('fdff00')
        self.assertEqual(n, encode_varint(255))

        n = bytes.fromhex('fd2b02')
        self.assertEqual(n, encode_varint(555))

        n = bytes.fromhex('fe7f110100')
        self.assertEqual(n, encode_varint(70015))

        n = bytes.fromhex('ff6dc7ed3e60100000')
        self.assertEqual(n, encode_varint(18005558675309))


if __name__ == '__main__':
    unittest.main()
