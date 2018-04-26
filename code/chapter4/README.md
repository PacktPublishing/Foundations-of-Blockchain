# Chapter 4


### Quick start
(set up two connected nodes and mine 1 block)
```
install python version >= 3.5

pip install -r requirements.txt
PORT=3001 python main.py
PORT=3002 PEERS=ws://localhost:3001 python main.py
curl -H "Content-type:application/json" --data '{"data" : "Some data to the first block"}' http://localhost:3001/mineBlock
```

### HTTP API
##### Get blockchain
```
curl http://localhost:3001/blocks
```
##### Create block
```
curl -H "Content-type:application/json" --data '{"data" : "Some data to the first block"}' http://localhost:3001/mineBlock
``` 
##### Add peer
```
curl -H "Content-type:application/json" --data '{"peer" : "ws://localhost:6001"}' http://localhost:3001/addPeer
```
#### Query connected peers
```
curl http://localhost:3001/peers
```


## Note

The project of P2P blockchain application built in chapter 4 could be found [here](https://github.com/koshikraj/pynaivechain).

