import binascii
import os
import json

from ecdsa import SigningKey, SECP256k1
from functools import reduce

from transaction import Transaction, TxOut, TxIn, get_public_key, get_transaction_id, sign_tx_in


try:
    PRIV_KEY_LOC = os.environ['PRIVATE_KEY']
except KeyError as e:
    PRIV_KEY_LOC = 'node/wallet/private_key'


def get_private_from_wallet():

    return binascii.a2b_hex(open(PRIV_KEY_LOC).read())


def get_public_from_wallet():

    sk = SigningKey.from_string(get_private_from_wallet(), curve=SECP256k1)
    vk = sk.get_verifying_key()
    return binascii.b2a_hex(vk.to_string()).decode()


def generate_private_key():

    sk = SigningKey.generate(curve=SECP256k1)
    with open(PRIV_KEY_LOC, 'wt') as file_obj:
        file_obj.write(binascii.b2a_hex(sk.to_string()).decode())


def init_wallet():

    # let's not override existing private keys
    if os.path.isfile(PRIV_KEY_LOC):
        return

    generate_private_key()
    print('new wallet with private key created at : %s' % PRIV_KEY_LOC)


def delete_wallet():
    if os.path.isfile(PRIV_KEY_LOC):
        os.remove(PRIV_KEY_LOC)


def get_balance(address, unspent_tx_outs):

    return sum(map(lambda utxo : utxo.amount, find_unspent_tx_outs(address, unspent_tx_outs)))


def find_unspent_tx_outs(owner_address, unspent_tx_outs):

    return list(filter(lambda utxo: utxo.address == owner_address, unspent_tx_outs))


def find_tx_outs_for_amount(amount, my_unspent_tx_outs):
    current_amount = 0
    incl_unspent_tx_outs = []
    for my_unspent_tx_out in my_unspent_tx_outs:
        incl_unspent_tx_outs.append(my_unspent_tx_out)
        current_amount = current_amount + my_unspent_tx_out.amount
        if current_amount >= amount:
            left_over_amount = current_amount - amount
            return incl_unspent_tx_outs, left_over_amount

    e_msg = 'Cannot create transaction from the available unspent transaction outputs.' \
            ' Required amount:' + str(amount) + '. Available unspent_tx_outs:' + json.dumps(my_unspent_tx_outs)
    print(e_msg)
    return None, None


def create_tx_outs(receiver_address, my_address, amount, left_over_amount):
    tx_out = TxOut(receiver_address, amount)
    if left_over_amount == 0:
        return [tx_out]
    else:
        left_over_tx = TxOut(my_address, left_over_amount)
        return [tx_out, left_over_tx]


def filter_tx_pool_txs(unspent_tx_outs, transaction_pool):
    tx_ins = reduce((lambda a, b: a + b), map(lambda tx: tx.tx_ins, transaction_pool), [])

    for unspent_tx_out in unspent_tx_outs[:]:
        try:
            next(a_tx_in for a_tx_in in tx_ins if a_tx_in.tx_out_index == unspent_tx_out.tx_out_index
                 and a_tx_in.tx_out_id == unspent_tx_out.tx_out_id)
            unspent_tx_outs.remove(unspent_tx_out)
        except StopIteration as e:
            pass

    return unspent_tx_outs


def create_transaction(receiver_address, amount, private_key,
                       unspent_tx_outs, tx_pool):

    print('txPool has %d transactions', len(tx_pool))

    my_address = get_public_key(private_key)

    my_unspent_tx_outs_a = list(filter(lambda utxo: utxo.address == my_address, unspent_tx_outs))

    my_unspent_tx_outs = filter_tx_pool_txs(my_unspent_tx_outs_a, tx_pool)

    # filter from unspentOutputs such inputs that are referenced in pool
    incl_unspent_tx_outs, left_over_amount = find_tx_outs_for_amount(amount, my_unspent_tx_outs)
    if not incl_unspent_tx_outs:
        return None

    def to_unsigned_tx_in(unspent_tx_out):

        tx_in = TxIn(unspent_tx_out.tx_out_id, unspent_tx_out.tx_out_index, '')
        return tx_in

    unsigned_tx_ins = list(map(to_unsigned_tx_in, incl_unspent_tx_outs))

    tx = Transaction(unsigned_tx_ins,
                     create_tx_outs(receiver_address, my_address, amount, left_over_amount))

    def sign_transaction(tx, index):
        tx.tx_ins[index].signature = sign_tx_in(tx, index, private_key, unspent_tx_outs)

    for index, txIn in enumerate(tx.tx_ins):
        sign_transaction(tx, index)

    return tx
