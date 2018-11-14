# Chapter 5

Scripts present here could be used to create and deploy web server to create a REST API.
 Full project with front end integration could be found [here](https://github.com/koshikraj/proof-of-existence).

## Quick Start

### Getting started with MultiChain

- Installation

    Follow the installation instruction for Mac/Windows/Linux

    www.multichain.com/download-install/
    
- Create a chain
    
    `multichain-util create chain1` 

- Instantiate the chain by creating a process

    `multichaind chain1 –daemon`
    
- Check the chain with `getinfo`

    `multichain-cli chain1 getinfo` 
    
    It should throw the following output
    
    `{"method":"getinfo","params":[],"id":1,"chain_name":"chain1"} 
     
       
     
     { 
     
       "version": "1.0.2", 
     
       "nodeversion": 10002901, 
     
       "protocolversion": 10009, 
     
       "chainname": "chain1", 
     
       "description": "MultiChain chain1", 
     
       "protocol": "multichain", 
     
       "port": 4273, 
     
       ...
     
       "balance": 0, 
     
       "walletdbversion": 2, 
     
       ...
     
     } `
    
- Create a stream

    `create stream stream1 false`
    
- You should be able to publish stream item if everything went well

    `publish stream1 key1 73747265616d2064617461 `
    
### Deploying the Proof of Existence application     

- Install dependencies

   `pip install -r requirements.txt`

- Start python webserver

   `python poe_server.py`
   

### HTTP API
##### Publish document
```
curl -X POST -F 'name=user' -F 'email=test@test.com1' -F 'message=some message' -F 'digest=86abfbd5f1a9e928935cdee9b2fd1bc2d43254b40d996e262026e9d668555613' http://localhost:8000/publish 
```

##### Verify document
```
curl http://localhost:8000/verify?digest=86abfbd5f1a9e928935cdee9b2fd1bc2d43254b40d996e262026e9d668555613
``` 

##### Fetch latest document info
```
curl http://localhost:8000/details?count=3
```
