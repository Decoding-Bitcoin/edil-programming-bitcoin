import hashlib

def ripemd160(s):
    '''ripemd160 hash'''
    return hashlib.new('ripemd160', s).digest()

def sha1(s):
    '''sha1 hash'''
    return hashlib.sha1(s).digest()

def sha256(s):
    '''sha256 hash'''
    return hashlib.sha256(s).digest()

def hash160(s):
    '''sha256 followed by ripemd160'''
    return hashlib.new('ripemd160', hashlib.sha256(s).digest()).digest()

def hash256(s):
    '''double sha256'''
    return hashlib.sha256(hashlib.sha256(s).digest()).digest()
