# Cryptocurrency application

### Quick start
(set up two connected nodes)

install python version >= 3.5
```
pip install -r requirements.txt

PORT=3001 python main.py
PORT=3002 PEERS=ws://localhost:3001 python main.py
curl -H "Content-type:application/json" --data '{"data" : "Some data to the first block"}' http://localhost:3001/mineBlock
```

### HTTP API
#### Get blockchain
```
curl http://localhost:3001/blocks
```
#### Create block
```
curl -H "Content-type:application/json" --data '{"data" : "Some data to the first block"}' http://localhost:3001/mineBlock
``` 
#### Add peer
```
curl -H "Content-type:application/json" --data '{"peer" : "ws://localhost:6001"}' http://localhost:3001/addPeer
```
### Query connected peers
```
curl http://localhost:3001/peers
```

##### Send transaction
```
curl -H "Content-type: application/json" --data '{"address": "04bfcab8722991ae774db48f934ca79cfb7dd991229153b9f732ba5334aafcd8e7266e47076996b55a14bf9913ee3145ce0cfc1372ada8ada74bd287450313534b", "amount" : 35}' http://localhost:3001/sendTransaction
```

##### Query transaction pool
```
curl http://localhost:3001/transactionPool
```

##### Mine transaction
```
curl -H "Content-type: application/json" --data '{"address": "04bfcab8722991ae774db48f934ca79cfb7dd991229153b9f732ba5334aafcd8e7266e47076996b55a14bf9913ee3145ce0cfc1372ada8ada74bd287450313534b", "amount" : 35}' http://localhost:3001/mineTransaction
```

##### Get balance
```
curl http://localhost:3001/balance
```


## Note

The project of P2P cryptocurrency application could be found [here](https://github.com/koshikraj/pynaivecoin).


