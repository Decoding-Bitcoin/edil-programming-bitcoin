import hashlib

def hash160(s):
    '''sha256 followed by ripemd160'''
    return hashlib.new('ripemd160', hashlib.sha256(s).digest()).digest()

def hash256(s):
    '''double sha256'''
    return hashlib.sha256(hashlib.sha256(s).digest()).digest()