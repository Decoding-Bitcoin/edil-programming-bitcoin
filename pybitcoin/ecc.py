from random import randint
from unittest import TestCase

import hashlib
import hmac

# Finite field operations
class FieldElement:

    def __init__(self, num, prime):
        if num >= prime or num < 0:
            error = "Num {} not in field range 0 to {}".format(num, prime - 1)
            raise ValueError(error)
        self.num = num
        self.prime = prime

    def __repr__(self):
        return "FieldElement_{}({})".format(self.prime, self.num)

    def __eq__(self, other):
        if other is None:
            return False
        return self.num == other.num and self.prime == other.prime

    def __ne__(self, other):
        # this should be the inverse of the == operator
        return not (self == other)

    def __add__(self, other):
        if self.prime != other.prime:
            raise TypeError("Cannot add two numbers in different Fields")
        # self.num and other.num are the actual values
        # self.prime is what we need to mod against
        num = (self.num + other.num) % self.prime
        # We return an element of the same class
        return self.__class__(num, self.prime)

    def __sub__(self, other):
        if self.prime != other.prime:
            raise TypeError("Cannot subtract two numbers in different Fields")
        # self.num and other.num are the actual values
        # self.prime is what we need to mod against
        num = (self.num - other.num) % self.prime
        # We return an element of the same class
        return self.__class__(num, self.prime)

    def __mul__(self, other):
        if self.prime != other.prime:
            raise TypeError("Cannot multiply two numbers in different Fields")
        # self.num and other.num are the actual values
        # self.prime is what we need to mod against
        num = (self.num * other.num) % self.prime
        # We return an element of the same class
        return self.__class__(num, self.prime)

    def __pow__(self, exponent):
        n = exponent % (self.prime - 1)
        num = pow(self.num, n, self.prime)
        return self.__class__(num, self.prime)

    def __truediv__(self, other):
        if self.prime != other.prime:
            raise TypeError("Cannot divide two numbers in different Fields")
        # self.num and other.num are the actual values
        # self.prime is what we need to mod against
        # use fermat's little theorem:
        # self.num**(p-1) % p == 1
        # this means:
        # 1/n == pow(n, p-2, p)
        num = (self.num * pow(other.num, self.prime - 2, self.prime)) % self.prime
        # We return an element of the same class
        return self.__class__(num, self.prime)

    def __rmul__(self, coefficient):
        num = (self.num * coefficient) % self.prime
        return self.__class__(num=num, prime=self.prime)


# Elliptic curve operations
class Point:

    def __init__(self, x, y, a, b):
        self.a = a
        self.b = b
        self.x = x
        self.y = y
        if self.x is None and self.y is None:
            return
        if self.y**2 != self.x**3 + a * x + b:
            raise ValueError("({}, {}) is not on the curve".format(x, y))

    def __eq__(self, other):
        return (
            self.x == other.x
            and self.y == other.y
            and self.a == other.a
            and self.b == other.b
        )

    def __ne__(self, other):
        # this should be the inverse of the == operator
        return not (self == other)

    def __repr__(self):
        if self.x is None:
            return "Point(infinity)"
        elif isinstance(self.x, FieldElement):
            return "Point({},{})_{}_{} FieldElement({})".format(
                self.x.num, self.y.num, self.a.num, self.b.num, self.x.prime
            )
        else:
            return "Point({},{})_{}_{}".format(self.x, self.y, self.a, self.b)

    def __add__(self, other):
        if self.a != other.a or self.b != other.b:
            raise TypeError(
                "Points {}, {} are not on the same curve".format(self, other)
            )
        # Case 0.0: self is the point at infinity, return other
        if self.x is None:
            return other
        # Case 0.1: other is the point at infinity, return self
        if other.x is None:
            return self

        # Case 1: self.x == other.x, self.y != other.y
        # Result is point at infinity
        if self.x == other.x and self.y != other.y:
            return self.__class__(None, None, self.a, self.b)

        # Case 2: self.x ≠ other.x
        # Formula (x3,y3)==(x1,y1)+(x2,y2)
        # s=(y2-y1)/(x2-x1)
        # x3=s**2-x1-x2
        # y3=s*(x1-x3)-y1
        if self.x != other.x:
            s = (other.y - self.y) / (other.x - self.x)
            x = s**2 - self.x - other.x
            y = s * (self.x - x) - self.y
            return self.__class__(x, y, self.a, self.b)

        # Case 4: if we are tangent to the vertical line,
        # we return the point at infinity
        # note instead of figuring out what 0 is for each type
        # we just use 0 * self.x
        if self == other and self.y == 0 * self.x:
            return self.__class__(None, None, self.a, self.b)

        # Case 3: self == other
        # Formula (x3,y3)=(x1,y1)+(x1,y1)
        # s=(3*x1**2+a)/(2*y1)
        # x3=s**2-2*x1
        # y3=s*(x1-x3)-y1
        if self == other:
            s = (3 * self.x**2 + self.a) / (2 * self.y)
            x = s**2 - 2 * self.x
            y = s * (self.x - x) - self.y
            return self.__class__(x, y, self.a, self.b)

    def __rmul__(self, coefficient):
        coef = coefficient
        current = self
        result = self.__class__(None, None, self.a, self.b)
        while coef:
            if coef & 1:
                result += current
            current += current
            coef >>= 1
        return result


# Secp256k1 parameters
class S256Params:
    A = 0
    B = 7
    P = 2**256 - 2**32 - 977
    N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
    Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
    Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8


# Secp256k1 finite field
class S256Field(FieldElement, S256Params):

    def __init__(self, num, prime=None):
        super().__init__(num=num, prime=self.P)

    def __repr__(self):
        return "{:x}".format(self.num).zfill(64)


# A point on the secp256k1 curve
class S256Point(Point, S256Params):

    def __init__(self, x, y, a=None, b=None):
        a, b = S256Field(self.A), S256Field(self.B)
        if type(x) == int:
            super().__init__(x=S256Field(x), y=S256Field(y), a=a, b=b)
        else:
            super().__init__(x=x, y=y, a=a, b=b)

    def __repr__(self):
        if self.x is None:
            return "S256Point(infinity)"
        else:
            return "S256Point({}, {})".format(self.x, self.y)

    def __rmul__(self, coefficient):
        coef = coefficient % self.N
        return super().__rmul__(coef)

    def verify(self, z, sig):
        s_inv = pow(sig.s, self.N - 2, self.N)
        u = z * s_inv % self.N
        v = sig.r * s_inv % self.N
        G = S256Point(self.Gx, self.Gy)
        total = u * G + v * self
        return total.x.num == sig.r

    def sec(self, compressed=True):
        '''Returns the binary version of the SEC format'''
        if compressed:
            if self.y.num % 2 == 0:
                return b'\x02' + self.x.num.to_bytes(32, 'big')
            else:
                return b'\x03' + self.x.num.to_bytes(32, 'big')
        else:
            return b'\x04' + self.x.num.to_bytes(32, 'big') \
                + self.y.num.to_bytes(32, 'big')


# ECDSA signature
class Signature:

    def __init__(self, r, s):
        self.r = r
        self.s = s

    def __repr__(self):
        return "Signature({:x},{:x})".format(self.r, self.s)


# Bitcoin Private Key
class PrivateKey(S256Params):
    G = S256Point(S256Params.Gx, S256Params.Gy)

    def __init__(self, secret):
        self.secret = secret
        self.point = secret * self.G

    def hex(self):
        return "{:x}".format(self.secret).zfill(64)

    def sign(self, z):
        k = self.deterministic_k(z)
        r = (k * self.G).x.num
        k_inv = pow(k, self.N - 2, self.N)
        s = (z + r * self.secret) * k_inv % self.N
        if s > self.N / 2:
            s = self.N - s
        return Signature(r, s)

    def deterministic_k(self, z):
        k = b"\x00" * 32
        v = b"\x01" * 32
        if z > self.N:
            z -= self.N
        z_bytes = z.to_bytes(32, "big")
        secret_bytes = self.secret.to_bytes(32, "big")
        s256 = hashlib.sha256
        k = hmac.new(k, v + b"\x00" + secret_bytes + z_bytes, s256).digest()
        v = hmac.new(k, v, s256).digest()
        k = hmac.new(k, v + b"\x01" + secret_bytes + z_bytes, s256).digest()
        v = hmac.new(k, v, s256).digest()
        while True:
            v = hmac.new(k, v, s256).digest()
            candidate = int.from_bytes(v, "big")
            if candidate >= 1 and candidate < self.N:
                return candidate
            k = hmac.new(k, v + b"\x00", s256).digest()
            v = hmac.new(k, v, s256).digest()
