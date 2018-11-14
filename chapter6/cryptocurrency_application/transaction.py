import binascii
import json

from Crypto.Hash import SHA256
from collections import defaultdict
from ecdsa import SigningKey, VerifyingKey, SECP256k1
from functools import reduce

COINBASE_AMOUNT = 50


class UnspentTxOut:

    def __init__(self, tx_out_id, tx_out_index, address, amount):
        self.tx_out_id = tx_out_id
        self.tx_out_index = tx_out_index
        self.address = address
        self.amount = amount


class TxIn:
    def __init__(self, tx_out_id, tx_out_index, signature):
        self.tx_out_id = tx_out_id
        self.tx_out_index = tx_out_index
        self.signature = signature


class TxOut:
    def __init__(self, address, amount):
        self.address = address
        self.amount = amount


class Transaction:

    def __init__(self, tx_ins, tx_outs):

        self.tx_ins = tx_ins
        self.tx_outs = tx_outs
        self.id = get_transaction_id(self)


def get_transaction_id(transaction):

    tx_in_content = reduce(lambda a, b : a + b, map(
        (lambda tx_in: str(tx_in.tx_out_id) + str(tx_in.tx_out_index)), transaction.tx_ins), '')

    tx_out_content = reduce(lambda a, b : a + b, map(
        (lambda tx_out: str(tx_out.address) + str(tx_out.amount)), transaction.tx_outs), '')

    return SHA256.new((tx_in_content + tx_out_content).encode()).hexdigest()


def validate_transaction(transaction, a_unspent_tx_outs):

    if not is_valid_transaction_structure(transaction):
        return False

    if get_transaction_id(transaction) != transaction.id:
        print('invalid tx id: ' + transaction.id)
        return False

    has_valid_tx_ins = reduce((lambda a, b: a and b), map(lambda tx_in: validate_tx_in(tx_in, transaction, a_unspent_tx_outs), transaction.tx_ins), True)


    if not has_valid_tx_ins:
        print('some of the tx_ins are invalid in tx: ' + transaction.id)
        return False

    total_tx_in_values = reduce((lambda a, b : a + b),
                             map(lambda tx_in : get_tx_in_amount(tx_in, a_unspent_tx_outs), transaction.tx_ins), 0)

    total_tx_out_values = reduce((lambda a, b : a + b),
                              map(lambda tx_out : tx_out.amount, transaction.tx_outs), 0)

    if total_tx_out_values != total_tx_in_values:
        print('total_tx_out_values !== total_tx_in_values in tx: ' + transaction.id)
        return False

    return True


def validate_block_transactions(a_transactions, a_unspent_tx_outs, block_index):

    coinbaseTx = a_transactions[0]
    if not validate_coinbase_tx(coinbaseTx, block_index):
        print('invalid coinbase transaction: ' + json.dumps(coinbaseTx))
        return False

    # check for duplicate tx_ins. Each tx_in can be included only once
    tx_ins = reduce((lambda a, b : a + b), map(lambda tx : tx.tx_ins, a_transactions))

    if has_duplicates(tx_ins):
        return False

    # all but coinbase transactions
    normalTransactions = a_transactions[1:]
    return reduce((lambda a, b : a and b), map(lambda tx : validate_transaction(tx, a_unspent_tx_outs), normalTransactions), True)


def has_duplicates(tx_ins):

    grouped = defaultdict(list)
    for tx_in in tx_ins:
        grouped[tx_in.tx_out_id].append(tx_in.tx_out_index)
    for key, value in grouped.items():
        if len(value) != len(set(value)):
            print('duplicate tx_in: ' + key)
            return True
    return  False


def validate_coinbase_tx(transaction, block_index):
    if transaction is None:
        print('the first transaction in the block must be coinbase transaction')
        return False

    if get_transaction_id(transaction) != transaction.id:
        print('invalid coinbase tx id: ' + transaction.id)
        return False

    if len(transaction.tx_ins) != 1:
        print('one tx_in must be specified in the coinbase transaction')
        return False

    if transaction.tx_ins[0].tx_out_index != block_index:
        print('the tx_in signature in coinbase tx must be the block height')
        return False

    if len(transaction.tx_outs) != 1:
        print('invalid number of tx_outs in coinbase transaction')
        return False

    if transaction.tx_outs[0].amount != COINBASE_AMOUNT:
        print('invalid coinbase amount in coinbase transaction')
        return False

    return True


def validate_tx_in(tx_in, transaction, a_unspent_tx_outs):

    referenced_utxo = [utxo for utxo in a_unspent_tx_outs if utxo.tx_out_id == tx_in.tx_out_id and utxo.tx_out_index == tx_in.tx_out_index][0]
    if referenced_utxo == []:
        print('referenced txOut not found: ' + json.dumps(tx_in))
        return False

    address = referenced_utxo.address

    vk = VerifyingKey.from_string(bytes.fromhex(address), curve=SECP256k1)

    try:
        vk.verify(bytes.fromhex(tx_in.signature), transaction.id.encode())

    except Exception as e:
        # change the exception
        print('invalid tx_in signature: %s txId: %s address: %s' % (tx_in.signature, transaction.id, referenced_utxo.address))
        return False

    return True


def get_tx_in_amount(tx_in, a_unspent_tx_outs):
    return find_unspent_tx_out(tx_in.tx_out_id, tx_in.tx_out_index, a_unspent_tx_outs).amount


def find_unspent_tx_out(transaction_id, index, a_unspent_tx_outs):
    try:
        return next(utxo for utxo in a_unspent_tx_outs if utxo.tx_out_id == transaction_id and utxo.tx_out_index == index)
    except Exception:
        return False


def get_coinbase_transaction(address, block_index):

    tx_in = TxIn('', block_index, '')
    t = Transaction([tx_in], [TxOut(address, COINBASE_AMOUNT)])
    return t


def sign_tx_in(transaction, tx_in_index,
               private_key, a_unspent_tx_outs):

    tx_in = transaction.tx_ins[tx_in_index]
    data_to_sign = str(transaction.id)
    referenced_utxo = find_unspent_tx_out(tx_in.tx_out_id, tx_in.tx_out_index, a_unspent_tx_outs)
    if referenced_utxo is None:
        print('could not find referenced txOut')
        # throw Error()

    referenced_address = referenced_utxo.address

    if get_public_key(private_key) != referenced_address:
        print('trying to sign an input with private' +
              ' key that does not match the address that is referenced in tx_in')
        # throw Error()

    # key = ec.keyFromPrivate(private_key, 'hex')
    sk = SigningKey.from_string(private_key, curve=SECP256k1)
    signature = binascii.b2a_hex(sk.sign(data_to_sign.encode())).decode()
    return signature


def update_unspent_tx_outs(a_transactions, a_unspent_tx_outs):

    def find_utxos(t):
        utxos = []
        for index, tx_out in enumerate(t.tx_outs):
            utxos.append(UnspentTxOut(t.id, index, tx_out.address, tx_out.amount))
        return utxos

    new_utxos = reduce((lambda a, b: a + b), map(lambda t: find_utxos(t), a_transactions), [])


    consumed_utxos = list(map(lambda txin: UnspentTxOut(txin.tx_out_id, txin.tx_out_index, '', 0),
                              reduce((lambda a, b : a + b), map(lambda t: t.tx_ins, a_transactions), [])))

    resulting_utxos = list(filter(lambda utxo : not find_unspent_tx_out(utxo.tx_out_id, utxo.tx_out_index, consumed_utxos), a_unspent_tx_outs)) + new_utxos

    return resulting_utxos


def process_transactions(a_transactions, a_unspent_tx_outs, block_index):

    if not validate_block_transactions(a_transactions, a_unspent_tx_outs, block_index):
        print('invalid block transactions')
        return None
    return update_unspent_tx_outs(a_transactions, a_unspent_tx_outs)


# def toHexString = (byteArray): string => {
# return Array.from(byteArray, (byte: any) => {
# return ('0' + (byte & 0xFF).toString(16)).slice(-2)
# }).join('')
# }

def get_public_key(private_key):

    sk = SigningKey.from_string(private_key
                                , curve=SECP256k1)
    vk = sk.get_verifying_key()
    return binascii.b2a_hex(vk.to_string()).decode()


def is_valid_tx_in_structure(tx_in):
    if tx_in is None:
        print('tx_in is null')
        return False
    elif type(tx_in.signature) is not str:
        print('invalid signature type in tx_in')
        return False
    elif type(tx_in.tx_out_id) is not str:
        print('invalid tx_out_id type in tx_in')
        return False
    elif type(tx_in.tx_out_index) is not int:
        print('invalid tx_out_index type in tx_in')
        return False
    else:
        return True


def is_valid_tx_out_structure(tx_out):
    if tx_out is None:
        print('tx_out is null')
        return False
    elif type(tx_out.address) != str:
        print('invalid address type in tx_out')
        return False
    elif not is_valid_address(tx_out.address):
        print('invalid TxOut address')
        return False
    elif type(tx_out.amount) != int:
        print('invalid amount type in tx_out')
        return False
    else:
        return True


def is_valid_transaction_structure(transaction):

    if type(transaction.id) != str:
        print('transaction_id missing')
        return False

    if not isinstance(transaction.tx_ins, list):
        print('invalid tx_ins type in transaction')
        return False

    if (not reduce((lambda a, b : a and b),
                   map(lambda tx_in : is_valid_tx_in_structure(tx_in), transaction.tx_ins), True)):

        return False

    if not isinstance(transaction.tx_outs, list):

        print('invalid tx_ins type in transaction')
        return False

    if (not reduce((lambda a, b: a and b),
                   map(lambda tx_out: is_valid_tx_out_structure(tx_out), transaction.tx_outs), True)):

        return False

    return True


# valid address is a valid ecdsa public key in the 04 + X-coordinate + Y-coordinate format
def is_valid_address(address):

    import re
    if len(address) != 128:
        print('invalid public key length')
        return False
    elif re.match('^[a-fA-F0-9]+$', address) is None:
        print('public key must contain only hex characters')
        return False
    # elif not address.startsWith('04'):
    #     print('public key must start with 04')
    #     return False

    return True



