import json

from functools import reduce
from transaction import validate_transaction


transaction_pool = []


def get_transaction_pool():
    return transaction_pool


def add_to_transaction_pool(tx, unspent_tx_outs):

    if not validate_transaction(tx, unspent_tx_outs):
        print('Trying to add invalid tx to pool')

    if not is_valid_tx_for_pool(tx, transaction_pool):
        print('Trying to add invalid tx to pool')

    print('adding transaction to txPool')
    transaction_pool.append(tx)


def has_tx_in(tx_in, unspent_tx_outs):
    try:
        next(utxo for utxo in unspent_tx_outs
                         if utxo.tx_out_id == tx_in.tx_out_id and utxo.tx_out_index == tx_in.tx_out_index)
        return True
    except StopIteration:
        return False


def update_transaction_pool(unspent_tx_outs):

    global transaction_pool
    for tx in transaction_pool[:]:
        for tx_in in tx.tx_ins:
            if not has_tx_in(tx_in, unspent_tx_outs):
                transaction_pool.remove(tx)
                print('removing the following transactions from txPool: %s' % json.dumps(tx))
                break


def get_tx_pool_ins(atransaction_pool):
    return reduce(lambda a,b : a + b, map(lambda tx: tx.tx_ins, atransaction_pool), [])


def is_valid_tx_for_pool(tx, atransaction_pool):
    tx_pool_ins = get_tx_pool_ins(atransaction_pool)

    def contains_tx_in(tx_in):
        try:
            return next(tx_pool_in for tx_pool_in in tx_pool_ins if tx_in.tx_out_index == tx_pool_in.tx_out_index and tx_in.tx_out_id == tx_pool_in.tx_out_id)
        except StopIteration:
            return False


    for tx_in in tx.tx_ins:
        if contains_tx_in(tx_in):
            print('txIn already found in the txPool')
            return False

    return True
