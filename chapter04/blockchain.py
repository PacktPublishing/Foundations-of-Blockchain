from Crypto.Hash import SHA256
from datetime import datetime

from utils.logger import logger

class Block(object):

    def __init__(self, index, previous_hash, timestamp, data, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash

    def dict(self):
        return {"data": self.data,
                "hash": self.hash,
                "index": self.index,
                "previous_hash": self.previous_hash,
                "timestamp": self.timestamp}


class Blockchain(object):

    def __init__(self):

        self._blockchain = [self.get_genesis_block()]

    @property
    def blocks(self):
        return self._blockchain

    @blocks.setter
    def blocks(self, blocks):
        self._blockchain = blocks

    @staticmethod
    def get_genesis_block():

        # SHA256.new(data=(str(0) + "0"+ str(1465154705) +"my genesis block!!").encode()).hexdigest()

        return Block(0, "0", 1465154705, "my genesis block!!",
                     "816534932c2b7154836da6afc367695e6337db8a921823784c14378abed4f7d7")

    def generate_next_block(self, block_data):

        previous_block = self.get_latest_block()
        next_index = previous_block.index + 1
        next_timestamp = int(datetime.now().timestamp())
        next_hash = self.calculate_hash(next_index, previous_block.hash, next_timestamp, block_data)
        return Block(next_index, previous_block.hash, next_timestamp, block_data, next_hash)

    def get_latest_block(self):

        try:
            return self._blockchain[-1]
        except IndexError as e:
            return None

    @classmethod
    def calculate_hash_for_block(cls, block):

        return cls.calculate_hash(block.index, block.previous_hash, block.timestamp, block.data)

    @staticmethod
    def calculate_hash(index, previous_hash, timestamp, data):

        hash_object = SHA256.new(data=(str(index) + previous_hash + str(timestamp) + data).encode())
        return hash_object.hexdigest()

    def add_block(self, new_block):

        if self.is_valid_new_block(new_block, self.get_latest_block()):
            self._blockchain.append(new_block)

    def is_valid_new_block(self, new_block, previous_block):

        if previous_block.index + 1 != new_block.index:
            logger.warning('invalid index')
            return False
        if previous_block.hash != new_block.previous_hash:
            logger.warning('invalid previous hash')
            return False
        if self.calculate_hash_for_block(new_block) != new_block.hash:
            logger.info(type(new_block.hash) + ' ' + type(self.calculate_hash_for_block(new_block)))
            logger.warning('invalid hash: ' + self.calculate_hash_for_block(new_block) + ' ' + new_block.hash)
            return False

        return True

    def is_valid_chain(self, blockchain_to_validate):

        if self.calculate_hash_for_block(Block(**blockchain_to_validate[0])) != self.get_genesis_block().hash:
            return False

        temp_blocks = [Block(**blockchain_to_validate[0])]
        for currentBlock in blockchain_to_validate[1:]:
            if self.is_valid_new_block(Block(**currentBlock), temp_blocks[-1]):
                temp_blocks.append(Block(**currentBlock))
            else:
                return False
        return True
