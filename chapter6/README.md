# Chapter 6, Diving into Blockchain: Proof of Existence
This chapter introduces the decentralized application development using MultiChain blockchain framework by implementing a use case — Proof of Existence.

Scripts present here could be used to create and deploy web server to create a REST API.
 Full project with front end integration could be found [here](https://github.com/koshikraj/proof-of-existence).

## Quick Start

### Getting started with MultiChain

- Installation (ubuntu distro)
    More installation instructions for Mac/Windows/Linux can be found at: www.multichain.com/download-install/

    * Change directory to tmp folder: 
    
        `cd /tmp` 
    
    * Download the MultiChain bundle: 
    
        ```
        wget https://www.multichain.com/download/multichain-1.0.6.tar.gz
        ```    
    * Exctract the tar file: 
    
        ```
        tar -xvzf multichain-1.0.6.tar.gz 
        ```
    * Change directory to the extracted folder: 
    
        `cd multichain-1.0.6` 
    
    * Move few files to `/usr/local/bin`: 
    
        ```
        mv multichaind multichain-cli multichain-util /usr/local/bin
        ``` 

    
    
- Create a chain
    
    `multichain-util create testchain -default-rpc-port=4416` 
    
- Configure multichain node

    Copy the file `./multichain.conf` to `~/.multichain/testchain/` to setup required rpc user and password to communicate from POE server

- Instantiate the chain by creating a process

    `multichaind testchain –daemon`
    
- Check the chain with `getinfo`

    `multichain-cli testchain getinfo` 
    
    It should throw the following output
    
    `{"method":"getinfo","params":[],"id":1,"chain_name":"chain1"} 
     
       
     
     { 
     
       "version": "1.0.2", 
     
       "nodeversion": 10002901, 
     
       "protocolversion": 10009, 
     
       "chainname": "chain1", 
     
       "description": "MultiChain testchain", 
     
       "protocol": "multichain", 
     
       "port": 4273, 
     
       ...
     
       "balance": 0, 
     
       "walletdbversion": 2, 
     
       ...
     
     } `
    
- Create a stream

    `multichain-cli testchain create stream poe false`
    
- Subscribe to the stream

    `multichain-cli testchain subscribe poe`
    
- You should be able to publish stream item if everything went well

    `multichain-cli testchain publish poe key1 73747265616d2064617461 `
    
### Deploying the Proof of Existence application     

- Install dependencies

   `pip install -r requirements.txt`

- Start python webserver

   `python poe_server.py`
   
### Using Docker

You can also run the docker containers for both MultiChain node and POE server if you do not want to play around with the commands.
Windows/Mac users can also run this docker instances.

Docker engine and Docker compose installation instructions can be found [here](../prerequisites/docker-installation.md).

Following command will setup both MultiChain node and the POE server to interact.
```
docker-compose up

```
   

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
