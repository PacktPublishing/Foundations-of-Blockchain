from bitcoin import SelectParams
import bitcoin.rpc
import math
import time

from bitcoin.core import b2x, b2lx, str_money_value, COIN, CMutableTransaction, CMutableTxIn, CMutableTxOut
from bitcoin.wallet import CBitcoinAddress


SelectParams('testnet')

rpc = bitcoin.rpc.Proxy()

dust_amount = int(0.0001 * COIN)

feeperbyte1 = 0.000011 / 1000 * COIN
feeperbyte2 = 0.001 / 1000 * COIN

optinrbf = True
tx1_nSequence = 0xFFFFFFFF-2 if optinrbf else 0xFFFFFFFF
tx2_nSequence = tx1_nSequence

payment_address = CBitcoinAddress("n4Wux6bCxwFPvj7BYNb8REvtahhJ9fHJFv")


payment_txout = CMutableTxOut(int(0.1 * COIN), payment_address.to_scriptPubKey())
change_txout = CMutableTxOut(0, rpc.getnewaddress().to_scriptPubKey())

tx = CMutableTransaction()
tx.vout.append(change_txout)
tx.vout.append(payment_txout)




unspent = sorted(rpc.listunspent(1), key=lambda x: x['amount'])
value_in = 0
value_out = sum([vout.nValue for vout in tx.vout])
while (value_in - value_out) / len(tx.serialize()) < feeperbyte1:

    delta_fee = math.ceil((feeperbyte1 * len(tx.serialize())) - (value_in - value_out))

    if change_txout.nValue - delta_fee > dust_amount:
        change_txout.nValue -= delta_fee
        value_out -= delta_fee

    if value_in - value_out < 0:
        new_outpoint = unspent[-1]['outpoint']
        new_amount = unspent[-1]['amount']
        unspent = unspent[:-1]

        print('Adding new input %s:%d with value %s BTC' % \
                      (b2lx(new_outpoint.hash), new_outpoint.n,
                       str_money_value(new_amount)))

        new_txin = CMutableTxIn(new_outpoint, nSequence=tx1_nSequence)
        tx.vin.append(new_txin)

        value_in += new_amount
        change_txout.nValue += new_amount
        value_out += new_amount

        r = rpc.signrawtransaction(tx)
        assert(r['complete'])

        tx.vin[-1].scriptSig = r['tx'].vin[-1].scriptSig

r = rpc.signrawtransaction(tx)
assert(r['complete'])
tx = CMutableTransaction.from_tx(r['tx'])

print('Payment raw transaction %s' % b2x(tx.serialize()))
print('Payment raw transaction size: %.3f KB, fees: %s, %s BTC/KB' % \
             (len(tx.serialize()) / 1000,
              str_money_value(value_in-value_out),
              str_money_value((value_in-value_out) / len(tx.serialize()) * 1000)))



txid = rpc.sendrawtransaction(tx)
print('Sent payment with txid: %s' % b2lx(txid))


print('Waiting for %d seconds before double spending' % 2)
time.sleep(10)


tx.vout = tx.vout[0:1]
change_txout = tx.vout[0]
value_out = value_in
change_txout.nValue = value_out

while (value_in - value_out) / len(tx.serialize()) < feeperbyte2:
    # What's the delta fee that we need to get to our desired fees per byte at
    # the current tx size?
    delta_fee = math.ceil((feeperbyte2 * len(tx.serialize())) - (value_in - value_out))

    print('Delta fee: %s' % str_money_value(delta_fee))

    if change_txout.nValue - delta_fee > dust_amount:
        change_txout.nValue -= delta_fee
        value_out -= delta_fee

    if value_in - value_out < 0:
        new_outpoint = unspent[-1]['outpoint']
        new_amount = unspent[-1]['amount']
        unspent = unspent[:-1]

        print('Adding new input %s:%d with value %s BTC' % \
                      (b2lx(new_outpoint.hash), new_outpoint.n,
                       str_money_value(new_amount)))

        new_txin = CMutableTxIn(new_outpoint, nSequence=tx2_nSequence)
        tx.vin.append(new_txin)

        value_in += new_amount
        change_txout.nValue += new_amount
        value_out += new_amount

        r = rpc.signrawtransaction(tx)
        assert(r['complete'])

        tx.vin[-1].scriptSig = r['tx'].vin[-1].scriptSig

r = rpc.signrawtransaction(tx)
assert(r['complete'])
tx = r['tx']

print('Double-spend raw transaction %s' % b2x(tx.serialize()))
print('Double-spend raw transaction size: %.3f KB, fees: %s, %s BTC/KB' % \
             (len(tx.serialize()) / 1000,
              str_money_value(value_in-value_out),
              str_money_value((value_in-value_out) / len(tx.serialize()) * 1000)))


txid = rpc.sendrawtransaction(tx)
print('Sent double-spend txid: %s' % b2lx(txid))