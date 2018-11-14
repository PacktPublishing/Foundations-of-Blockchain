#!/usr/bin/env python
# example of proof-of-work algorithm

import json

from Crypto.Hash import SHA256
from datetime import datetime

max_nonce = 2 ** 32  # 4 billion


class Block(object):
    """A class representing the block for the blockchain"""

    def __init__(self, index, previous_hash, timestamp, data,
                 difficulty_bits, nonce, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.difficulty_bits = difficulty_bits
        self.nonce = nonce
        self.hash = hash


class Blockchain(object):
    """A class representing list of blocks"""

    def __init__(self):

        self._chain = [self.get_genesis_block()]
        self.timestamp = datetime.now().strftime("%s")
        self.difficulty_bits = 0

    @property
    def chain(self):
        """created a dict containing list of block objects to view"""

        return self.dict(self._chain)

    def dict(self, chain):
        """converts list of block objects to dictionary"""

        return json.loads(json.dumps(chain, default=lambda o: o.__dict__))

    def reset(self):
        """resets the blockchain blocks except genesis block"""

        self._chain = [self._chain[0]]

    def get_genesis_block(self):
        """creates first block of the chain"""

        # SHA256.new(data=(str(0) + "0"+ str(1465154705) +"my genesis block!!"+"0").encode()).hexdigest()
        return Block(0, "0", 1465154705, "my genesis block!!", 0, 0,
                     "f6b3fd6d417048423692c275deeaa010d4174bd680635d3e3cb0050aa46401cb")

    def add_block(self, data):
        """appends a new block to the blockchain"""

        self._chain.append(self.create_block(data))

    def create_block(self, block_data):
        """creates a new block with the given block data"""

        previous_block = self.get_latest_block()
        next_index = previous_block.index + 1
        next_timestamp = self.timestamp
        next_hash, next_nonce = self.calculate_hash(next_index, previous_block.hash, next_timestamp, block_data)
        return Block(next_index, previous_block.hash, next_timestamp, block_data, self.difficulty_bits, next_nonce, next_hash)

    def get_latest_block(self):
        """gets the last block from the blockchain"""

        try:
            return self._chain[-1]
        except IndexError as e:
            return None

    def calculate_hash(self, index, previous_hash, timestamp, data):
        """calculates SHA256 hash value by solving hash puzzle"""

        header = str(index) + previous_hash + str(timestamp) + data + str(self.difficulty_bits)

        hash_value, nonce = self.proof_of_work(header)
        return hash_value, nonce

    def proof_of_work(self, header):

        target = 2 ** (256 - difficulty_bits)

        for nonce in range(max_nonce):
            hash_result = SHA256.new(data=(str(header) + str(nonce)).encode()).hexdigest()

            if int(hash_result, 16) < target:
                print("Success with nonce %d" % nonce)
                print("Hash is %s" % hash_result)
                return (hash_result, nonce)

        print("Failed after %d (max_nonce) tries" % nonce)
        return nonce


if __name__ == '__main__':

    new_chain = Blockchain()

    for difficulty_bits in range(32):
        difficulty = 2 ** difficulty_bits
        new_chain.difficulty_bits = difficulty_bits
        print("Difficulty: %ld (%d bits)" % (difficulty, difficulty_bits))
        print("Starting search...")

        start_time = datetime.now()

        new_block_data = 'test block with transactions'
        new_chain.add_block(data=new_block_data)


        end_time = datetime.now()

        elapsed_time = (end_time - start_time).total_seconds()
        print("Elapsed Time: %.4f seconds" % elapsed_time)

        if elapsed_time > 0:

            hash_power = float(int(new_chain.chain[-1].get("nonce")) / elapsed_time)
            print("Hashing Power: %ld hashes per second" % hash_power)
