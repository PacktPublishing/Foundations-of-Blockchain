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


#### Run the neo-python node:

`np-prompt -p`
