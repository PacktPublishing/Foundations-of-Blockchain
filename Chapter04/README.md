# Chapter 4, Networking in Blockchain
This chapter introduces peer-to-peer networking concepts to achieve decentralization in the blockchain network. This chapter also covers how blockchain is maintained in a decentralized network with the help of an example application.


### Quick start
(set up two connected nodes and mine 1 block)

install python version >= 3.5
```
pip install -r requirements.txt

PORT=3001 python main.py
PORT=3002 PEERS=ws://localhost:3001 python main.py
curl -H "Content-type:application/json" --data '{"data" : "Some data to the first block"}' http://localhost:3001/mineBlock
```

**NOTE**: Windows users might face an issue while installing a dependency (uvloop). So, windows users are advised to run the application using docker as mentioned in the next section.

#### Using docker
Docker engine and Docker compose installation instructions can be found [here](../prerequisites/docker-installation.md).

(set up three connected nodes and mine a block)

```
docker-compose up
```

Additional node can be created by creating a new docker instance:

```
docker run --name chapter4_node1 --publish 0.0.0.0:6001:6001 chapter4_node1 /bin/bash -c "PORT=6001 python main.py
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


## Note

The project of P2P blockchain application built in chapter 4 could be found [here](https://github.com/koshikraj/pynaivechain).

