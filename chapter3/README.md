#Chapter 3, Cryptography in Blockchain
This chapter explains how blockchain technology makes use of few of the cryptographic primitives such as hash functions and digital signatures.


## quick start

## Blockchain example

### Using package

Find the python package which has the all the functions bundled together.

``pip install justblockchain``

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

### Using script

* ``pip install -r requirements.txt``

* ``python blockchain_example.py``

## Hash none example

```python hash_nonce_example.py```

## Proof-of-work example

```python proof_of_work_example.py```

## Digital signature example

```python digital_signature_example.py```
