## Setup the NEO ecosystem


### Setup a private network

```
docker pull cityofzion/neo-privatenet 

docker run --rm -d --name neo-privatenet -p 20333-20336:20333-20336/tcp -p 30333-30336:30333-30336/tcp cityofzion/neo-privatenet

```

### Install mainnet/testnet blockchain full node (ubuntu distro)

#### Setup dotnet client (optional)

```
git clone https://github.com/neo-project/neo-cli 

dotnet neo-cli.dll 

```

#### Setup neo-python client

* Install python interpreter version >= 3.6

* Install dependencies and neo-python

    ```
    sudo apt-get install libleveldb-dev libssl-dev g++
    
    pip install neo-python
    ```

Detailed installation instructions can be found at: https://neo-python.readthedocs.io/en/latest/install.html 

### Install mainnet/testnet blockchain full node (using docker)

Alternatively, neo-python node can be launched using docker container which uses latest ubuntu. This is ideal for windows user
since windows requires lot of dependency installations.

Below commands will build and launch a ubuntu container with all the dependencies and neo-python installed.

```
docker build -t neo-python .
docker run -it neo-python bash
```

### Run the neo-python node:

`np-prompt -p`

NOTE: If the private network is not setup locally, then specify a node address which has RPC server running.
You can use the node: [projects.koshikraj.com](projects.koshikraj.com) for testing purpose.

`np-prompt -p projects.koshikraj.com`  

### Open the wallet

Once the neo shell is launched, you can open the wallet:

`neo>open wallet neo-privnet.sample.wallet` 

password: coz 


