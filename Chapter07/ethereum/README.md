### Setup the Ethereum ecosystem

The Ethereum  ecosystem can be setup locally for development purpose or we can connect to an actual blockchain.
The local blockchain can be setup using an in-memory blockchain called Ganache.

Make sure that you have a latest version of `nodejs` and `npm`. Here is a [install guide](https://www.digitalocean.com/community/tutorials/how-to-install-node-js-on-ubuntu-16-04) for Ubuntu system.

#### Install local blockchain (Ganache)

`npm install ganache-cli web3@0.20.2`

NOTE: Windows users might face dependency issue while installing the ganache-cli. Alternatively, you could also install [ganache](https://truffleframework.com/ganache) for windows.



#### Install mainnet/testnet blockchain client (Optional)

##### Install using brew (Mac OSX):
```
brew tap ethereum/ethereum
brew install ethereum
```

##### Install using PPA (Ubuntu distro):

```
sudo apt-get install software-properties-common
sudo add-apt-repository -y ppa:ethereum/ethereum
sudo apt-get update
sudo apt-get install ethereum
```

##### Installing from source: 

* Clone the repository: 

    ```
    git clone https://github.com/ethereum/go-ethereum 
    ```

* Install Go and C compilers: 

    ```
    sudo apt-get install -y build-essential golang 
    ```

* Compile the source code: 

    ```
    cd go-ethereum
    make geth
    ```
    
Detailed installation instructions can be found at: https://geth.ethereum.org/install 


#### Run the Ethereum node:

```
geth --rinkeby --syncmode "fast" --rpc --rpcapi db,eth,net,web3,personal --cache=1024  --rpcport 8545 --rpcaddr 127.0.0.1 --rpccorsdomain "*"
```

### Setup an Ethereum development environment

We can start the Ethereum development from scratch or use an existing framework such as [truffle](https://truffleframework.com).
 

#### Truffle framework

Truffle framework makes the development and deployment process smoother by creating a framework for development.
The the framework will help to easily create and deploy the DApp.

```
npm install -g truffle

```
  