import bitcoin.rpc
from bitcoin.core import lx

bitcoin.SelectParams('testnet')

proxy_connection = bitcoin.rpc.Proxy()
tx_id = lx(input())
print(proxy_connection.gettransaction(tx_id))
