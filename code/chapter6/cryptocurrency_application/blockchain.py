from Crypto.Hash import SHA256
from datetime import datetime

from utils.logger import logger
from transaction import get_coinbase_transaction, is_valid_address, process_transactions, Transaction, UnspentTxOut, TxIn, TxOut
from transaction_pool import add_to_transaction_pool, get_transaction_pool, update_transaction_pool
from wallet import create_transaction, find_unspent_tx_outs, get_balance, get_private_from_wallet, get_public_from_wallet


max_nonce = 2 ** 32  # 4 billion

class Block(object):

    def __init__(self, index, previous_hash, timestamp, data,
                 difficulty_bits, nonce, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.difficulty_bits = difficulty_bits
        self.nonce = nonce
        self.hash = hash

    def dict(self):
        return {"data": self.data,
                "hash": self.hash,
                "index": self.index,
                "previous_hash": self.previous_hash,
                "timestamp": self.timestamp,
                "difficulty_bits": self.difficulty_bits,
                "nonce": self.nonce}


class Blockchain(object):

    def __init__(self):

        self._blockchain = [self.get_genesis_block()]
        self.difficulty_bits = 15
        self.unspent_tx_outs = process_transactions([self.genesis_transaction], [], 0)

    @property
    def blocks(self):
        return self._blockchain


    def get_unspent_tx_outs(self):
        return self.unspent_tx_outs

    def set_unspent_tx_outs(self, new_utxo):
        print('replacing unspent_tx_outs with: %s' % new_utxo)
        self.unspent_tx_outs = new_utxo

    @blocks.setter
    def blocks(self, blocks):
        self._blockchain = blocks

    # genesis_transaction = {'tx_ins': [{'signature': '', 'tx_out_id': '', 'tx_out_index': 0}],
    #     'tx_outs': [{
    #         'address': getPublicFromWallet(),
    #         'amount': 50
    #     }]
        # 'id': 'e655f6a5f26dc9b4cac6e46f52336428287759cf81ef5ff10854f69d68f43fa3'
    # }

    genesis_transaction = Transaction([TxIn('', 0, '')], [TxOut(get_public_from_wallet(), 50)])

    @classmethod
    def get_genesis_block(cls):

        # SHA256.new(data=(str(0) + "0"+ str(1465154705) +"my genesis block!!").encode()).hexdigest()

        return Block(0, "0", 1465154705, cls.genesis_transaction, 0, 0,
                     "816534932c2b7154836da6afc367695e6337db8a921823784c14378abed4f7d7")

    def generate_next_block(self, block_data):

        previous_block = self.get_latest_block()
        next_index = previous_block.index + 1
        next_timestamp = datetime.now().strftime("%s")
        next_hash, next_nonce = self.calculate_hash(next_index, previous_block.hash, next_timestamp, block_data)
        new_block = Block(next_index, previous_block.hash, next_timestamp, block_data,
                     self.difficulty_bits, next_nonce, next_hash)

        if self.add_block(new_block):
            # broadcastLatest();
            return new_block


    # gets the unspent transaction outputs owned by the wallet
    def get_my_utxos(self):
        return find_unspent_tx_outs(get_public_from_wallet(), self.get_unspent_tx_outs())

    def construct_next_block(self):
        coinbase_tx = get_coinbase_transaction(get_public_from_wallet(), self.blocks[-1].index + 1)
        block_data = [coinbase_tx] + get_transaction_pool()
        return self.generate_next_block(block_data)

    def construct_next_block_with_transaction(self, receiver_address, amount):
        if not is_valid_address(receiver_address):
            print('invalid address')
            return
        if not isinstance(amount, int):
            print('invalid amount')
            return

        coinbase_tx = get_coinbase_transaction(get_public_from_wallet(), self.blocks[-1].index + 1)
        tx = create_transaction(receiver_address, amount, get_private_from_wallet(),
                                self.get_unspent_tx_outs(), get_transaction_pool())
        if not tx:
            return False
        block_data = [coinbase_tx, tx]
        return self.generate_next_block(block_data)

    def get_account_balance(self):
        return get_balance(get_public_from_wallet(), self.get_unspent_tx_outs())

    def send_transaction(self, address, amount):
        tx = create_transaction(address, amount, get_private_from_wallet(),
                                self.get_unspent_tx_outs(), get_transaction_pool())
        add_to_transaction_pool(tx, self.get_unspent_tx_outs())
        # broadCastTransactionPool()
        return tx

    def get_latest_block(self):

        try:
            return self._blockchain[-1]
        except IndexError as e:
            return None

    def calculate_hash_for_block(self, block):

        return self.calculate_hash(block.index, block.previous_hash, block.timestamp, block.data, block.nonce)

    def calculate_hash(self, index, previous_hash, timestamp, data, nonce=None):

        if not nonce:
            header = str(index) + previous_hash + str(timestamp) + str(data) + str(self.difficulty_bits)
            return self.proof_of_work(header)
        else:
            hash_object = SHA256.new(data=(str(index) + previous_hash + str(timestamp)
                                           + str(data) + str(self.difficulty_bits) + str(nonce)).encode())
            return hash_object.hexdigest()

    def proof_of_work(self, header):
        """Calculates nonce for the block based on the difficulty bits set"""

        print("Computing nonce for the block...")
        target = 2 ** (256 - self.difficulty_bits)

        for nonce in range(max_nonce):
            hash_result = SHA256.new(data=(str(header) + str(nonce)).encode()).hexdigest()

            if int(hash_result, 16) < target:
                print("Success with nonce %d" % nonce)
                print("Hash is %s" % hash_result)
                return (hash_result, nonce)

        print("Failed after %d (max_nonce) tries" % nonce)
        return nonce

    def add_block(self, new_block):

        if self.is_valid_new_block(new_block, self.get_latest_block()):
            ret_val = process_transactions(new_block.data, self.get_unspent_tx_outs(), new_block.index)
            if ret_val is None:
                print('block is not valid in terms of transactions')
                return False
            else:
                self._blockchain.append(new_block)
                self.set_unspent_tx_outs(ret_val)
                update_transaction_pool(self.get_unspent_tx_outs())
                return True

    def is_valid_new_block(self, new_block, previous_block):

        if previous_block.index + 1 != new_block.index:
            logger.warning('invalid index')
            return False
        if previous_block.hash != new_block.previous_hash:
            logger.warning('invalid previous hash')
            return False
        if self.calculate_hash_for_block(new_block) != new_block.hash:
            logger.info(str(type(new_block.hash)) + ' ' + str(type(self.calculate_hash_for_block(new_block))))
            logger.warning('invalid hash: ' + self.calculate_hash_for_block(new_block) + ' ' + new_block.hash)
            return False

        return True

    def is_valid_chain(self, blockchain_to_validate):

        # if self.calculate_hash_for_block(Block(**blockchain_to_validate[0])) != self.get_genesis_block().hash:
        #     return False

        temp_blocks = [Block(**blockchain_to_validate[0])]
        for currentBlock in blockchain_to_validate[1:]:
            if self.is_valid_new_block(Block(**currentBlock), temp_blocks[-1]):
                temp_blocks.append(Block(**currentBlock))
            else:
                return False
        return True
