# Chapter 10, Blockchain Security
This chapter gives an insight on the level of security in the blockchain technology by pointing out the possible attacks in the blockchain network and how they can be prevented

## Double spend attack

We will perform a double spend attack on the Bitcoin unconfirmed transaction. A Bitcoin full node should be running locally to run this script.


## Quick start

A Bitcoin full node should be running locally to run this script. You can follow the instructions from [Chapter 5](../chapter5) to install the Bitcoin full node.

Alternatively, you can use the a remote Bitcoin full node whose RPC interface is exposed. You can use the remote Bitcoin testnet node deployed at [projects.koshikraj.com](projects.koshikraj.com). Replace the **line 12** in the script `double_spend_attack.py` with the following Proxy connection to connect to the remote Bitcoin node. 

```
rpc = bitcoin.rpc.Proxy(service_url="http://rpc:rpc1234@projects.koshikraj.com:18332")

```

NOTE: Exposing RPC interface of a node is not recommended. This should be only used for testing purpose.


Run the python script without any inputs. Update the attackers public address and transaction value in the script.

```
pip install -r requirements.txt

python double_spend_attack.py

```
