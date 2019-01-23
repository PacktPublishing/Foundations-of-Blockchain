# Chapter 5, Cryptocurrency
 
 This chapter dives into the original and the best implementation of the blockchain technology by exploring the concepts of Bitcoin, and helps to differentiate cryptocurrency from the traditional digital currencies.

## Quick start

### Bitcoin Core setup

#### Install from source

Clone the Bitcoin Core source code from https://github.com/bitcoin/bitcoin.git. 

1. Execute the shell script : 

    `./autogen.sh` 

2. Run the configuration script: 

    `./configure` 

3. Compile the source code and run the executable: 

    ```
    make 

    make install 
    ```
    
4. Run the Bitcoin daemon: 

    `bitcoind -daemon`

#### Install using PPA (Ubuntu distro)

    sudo add-apt-repository ppa:bitcoin/bitcoin
    sudo apt-get update
    sudo apt-get install bitcoind

#### Other platforms
[https://bitcoin.org/en/full-node](https://bitcoin.org/en/full-node)

### Running the example script

```
    pip install -r requirements.txt

    python bitcoin_example.py

```

