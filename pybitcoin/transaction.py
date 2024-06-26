from pybitcoin.util import (
    read_varint,
    encode_varint,
    int_to_little_endian,
    little_endian_to_int,
    SIGHASH_ALL
)
from pybitcoin.hash import hash256
from pybitcoin.script import Script

from io import BytesIO
import json
import requests

class TxIn:
    def __init__(self, prev_tx, prev_index, script_sig=None, sequence=0xffffffff):
        self.prev_tx = prev_tx
        self.prev_index = prev_index
        if script_sig is None:
            self.script_sig = Script()
        else:
            self.script_sig = script_sig
        self.sequence = sequence

    def __repr__(self):
        return '{}:{}'.format(
            self.prev_tx.hex(),
            self.prev_index,
        )

    def serialize(self):
        '''Returns the byte serialization of the transaction input'''
        result = self.prev_tx[::-1] # to endian little
        result += int_to_little_endian(self.prev_index, 4)
        result += self.script_sig.serialize()
        result += int_to_little_endian(self.sequence, 4)
        return result

    @classmethod
    def parse(cls, stream):
        # previous transaction ID
        previous_id = stream.read(32)[::-1] # little to big endian

        # previous index
        previous_index = little_endian_to_int(stream.read(4))

        # scriptSig
        script_sig = Script.parse(stream)

        # sequence
        sequence = little_endian_to_int(stream.read(4))

        # return parsed transaction
        return TxIn(previous_id, previous_index, script_sig, sequence)

    def fetch_tx(self, testnet=False):
        return TxFetcher.fetch(self.prev_tx.hex(), testnet=testnet)

    def value(self, testnet=False):
        '''Get the output value by looking up the tx hash.
        Returns the amount in satoshi.
        '''
        tx = self.fetch_tx(testnet=testnet)
        return tx.tx_outs[self.prev_index].amount

    def script_pubkey(self, testnet=False):
        '''Get the scriptPubkey by looking up the tx hash.
        Returns a Script object.
        '''
        tx = self.fetch_tx(testnet=testnet)
        return tx.tx_outs[self.prev_index].script_pubkey


class TxOut:
    def __init__(self, amount, script_pubkey):
        self.amount = amount
        self.script_pubkey = script_pubkey

    def __repr__(self):
        return '{}:{}'.format(self.amount, self.script_pubkey)

    def serialize(self):
        '''Returns the byte serialization of the transaction output'''
        result = int_to_little_endian(self.amount, 8)
        result += self.script_pubkey.serialize()
        return result

    @classmethod
    def parse(cls, stream):
        # amount
        amount = int.from_bytes(stream.read(8), 'little')

        # scriptPubkey
        script_pubkey = Script.parse(stream)

        # return parsed transaction
        return TxOut(amount, script_pubkey)


class Tx:

    def __init__(self, version, tx_ins, tx_outs, locktime, testnet=False):
        self.version = version
        self.tx_ins = tx_ins
        self.tx_outs = tx_outs
        self.locktime = locktime
        self.testnet = testnet

    def __repr__(self):
        tx_ins = ''
        for tx_in in self.tx_ins:
            tx_ins += tx_in.__repr__() + '\n'

        tx_outs = ''
        for tx_out in self.tx_outs:
            tx_outs += tx_out.__repr__() + '\n'

        return 'tx: {}\nversion: {}\ntx_ins:\n{}tx_outs:\n{}locktime: {}'.format(
            self.id(),
            self.version,
            tx_ins,
            tx_outs,
            self.locktime,
        )

    def id(self):
        '''Human-readable hexadecimal of the transaction hash'''
        return self.hash().hex()

    def hash(self):
        '''Binary hash of the legacy serialization'''
        return hash256(self.serialize())[::-1]

    def fee(self, testnet=False):
        # Get input amount
        input_amount = 0
        for tx_in in self.tx_ins:
            input_amount += tx_in.value()

        # Get output amount
        output_amount = 0
        for tx_out in self.tx_outs:
            output_amount += tx_out.amount

        # Return fee
        return input_amount - output_amount

    def serialize(self):
        '''Returns the byte serialization of the transaction'''
        result = int_to_little_endian(self.version, 4)
        result += encode_varint(len(self.tx_ins))
        for tx_in in self.tx_ins:
            result += tx_in.serialize()
        result += encode_varint(len(self.tx_outs))
        for tx_out in self.tx_outs:
            result += tx_out.serialize()
        result += int_to_little_endian(self.locktime, 4)
        return result

    @classmethod
    def parse(cls, stream, testnet=False):
        # parse version
        version = little_endian_to_int(stream.read(4))

        # parse inputs
        tx_ins = []
        n_inputs = read_varint(stream)
        for n in range(n_inputs):
            tx_ins.append(TxIn.parse(stream))

        # parse outputs
        tx_outs = []
        n_outputs = read_varint(stream)
        for n in range(n_outputs):
            tx_outs.append(TxOut.parse(stream))

        # parse locktime
        locktime = little_endian_to_int(stream.read(4))

        # build final transaction
        return Tx(version, tx_ins, tx_outs, locktime)

    def sig_hash(self, index, redeem_script=None):
        '''Returns the integer representation of the hash that needs to get
        signed for index input_index'''

        # start the serialization with version
        # use int_to_little_endian in 4 bytes
        modified_tx_raw = int_to_little_endian(self.version, 4)

        # add how many inputs there are using encode_varint
        modified_tx_raw += encode_varint(len(self.tx_ins))

        # loop through each input using enumerate, so we have the input index
        for i, tx_in in enumerate(self.tx_ins):
            # if the input index is the one we're signing
            if i == index:
            # the previous tx's ScriptPubkey is the ScriptSig
                if redeem_script == None:
                    script_sig = tx_in.script_pubkey(self.testnet)
                else:
                    script_sig = redeem_script
            # Otherwise, the ScriptSig is empty
            else:
                script_sig = None
            # add the serialization of the input with the ScriptSig we want
            modified_tx_raw += TxIn(
                prev_tx=tx_in.prev_tx,
                prev_index=tx_in.prev_index,
                script_sig=script_sig,
                sequence=tx_in.sequence,
            ).serialize()

        # add how many outputs there are using encode_varint
        modified_tx_raw += encode_varint(len(self.tx_outs))

        # add the serialization of each output
        for tx_out in self.tx_outs:
            modified_tx_raw += tx_out.serialize()

        # add the locktime using int_to_little_endian in 4 bytes
        modified_tx_raw += int_to_little_endian(self.locktime, 4)

        # add SIGHASH_ALL using int_to_little_endian in 4 bytes
        modified_tx_raw += int_to_little_endian(SIGHASH_ALL, 4)

        # hash256 the serialization
        h256 = hash256(modified_tx_raw)

        # convert the result to an integer using int.from_bytes(x, 'big')
        return int.from_bytes(h256)


class TxFetcher:
    cache = {}

    @classmethod
    def get_url(cls, testnet=False):
        if testnet:
            return 'http://testnet.programmingbitcoin.com'
        else:
            return 'http://mainnet.programmingbitcoin.com'

    @classmethod
    def fetch(cls, tx_id, testnet=False, fresh=False):
        if fresh or (tx_id not in cls.cache):
            url = '{}/tx/{}.hex'.format(cls.get_url(testnet), tx_id)
            response = requests.get(url)
            try:
                raw = bytes.fromhex(response.text.strip())
            except ValueError:
                raise ValueError('unexpected response: {}'.format(response.txt))
            if raw[4] == 0:
                raw = raw[:4] + raw[6:]
                tx = Tx.parse(BytesIO(raw), testnet=testnet)
                tx.locktime = little_endian_to_int(raw[-4:])
            else:
                tx = Tx.parse(BytesIO(raw), testnet=testnet)
            if tx.id() != tx_id:
                raise ValueError('not the same id: {} vs {}'.format(tx.id(), tx_id))
            cls.cache[tx_id] = tx
        cls.cache[tx_id].testnet = testnet
        return cls.cache[tx_id]
