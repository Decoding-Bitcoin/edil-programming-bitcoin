from pybitcoin.util import read_varint, encode_varint


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

    @classmethod
    def parse(cls, stream):
        # previous transaction ID
        previous_id_raw = stream.read(32)
        previous_id = int.from_bytes(previous_id_raw, 'little').to_bytes(32, 'big')

        # previous index
        previous_index_raw = stream.read(4)
        previous_index = int.from_bytes(previous_index_raw, 'little')

        # scriptSig
        # TODO: parse scriptSig
        script_length = read_varint(stream)
        script_raw = encode_varint(script_length) + stream.read(script_length)

        # sequence
        sequence_raw = stream.read(4)
        sequence = int.from_bytes(sequence_raw, 'little')

        # return parsed transaction
        return TxIn(previous_id, previous_index, script_raw, sequence)



class TxOut:
    def __init__(self, amount, script_pubkey):
        self.amount = amount
        self.script_pubkey = script_pubkey

    def __repr__(self):
        return '{}:{}'.format(self.amount, self.script_pubkey)

    @classmethod
    def parse(cls, stream):
        # amount
        amount = int.from_bytes(stream.read(8), 'little')

        # scriptPubkey
        # TODO: parse scriptPubkey
        script_length = read_varint(stream)
        script_pubkey_raw = encode_varint(script_length) + stream.read(script_length)

        # return parsed transaction
        return TxOut(amount, script_pubkey_raw)


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

    @classmethod
    def parse(cls, stream, testnet=False):
        # parse version
        serialized_version = stream.read(4)
        version = int.from_bytes(serialized_version, 'little')

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
        locktime = int.from_bytes(stream.read(4), 'little')

        # build final transaction
        return Tx(version, tx_ins, tx_outs, locktime)
