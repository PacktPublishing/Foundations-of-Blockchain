# Chapter 3

Find the python package which has the all the functions bundled together.

## Installtion

``pip install justblockchain``

## quick start

```
    >>> from justblockchain import justblockchain
    
    >>> blockchain = justblockchain.Blockchain()
    
    >>> blockchain.add_block("some block content")

    #display the blockchain
    >>> blockchain.chain
    [{'previous_hash': '0', 'hash':
    '816534932c2b7154836da6afc367695e6337db8a921823784c14378abed4f7d7',
    'timestamp': 1465154705, 'index': 0, 'data': 'my genesis block!!'},
    {'previous_hash':
    '816534932c2b7154836da6afc367695e6337db8a921823784c14378abed4f7d7', 'hash':
    'a046e0b31d2374d171a6bf62f15261f8bb1f71e6351aab2ce7ce6d550506d9ee',
    'timestamp': '1521013680', 'index': 1, 'data': 'some block content'}]

```