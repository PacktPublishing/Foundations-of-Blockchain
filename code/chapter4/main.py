import json as JSON
import os
import websockets

from sanic import Sanic
from sanic.response import json
from websockets.exceptions import ConnectionClosed

from blockchain import Block, Blockchain
from utils.logger import logger


QUERY_LATEST = 0
QUERY_ALL = 1
RESPONSE_BLOCKCHAIN = 2

try:
    port = int(os.environ['PORT'])
except KeyError as e:
    port = 3001

try:
    initialPeers = os.environ['PEERS'].split(",")
except Exception as e:
    initialPeers = []


class Server(object):

    def __init__(self):

        self.app = Sanic()
        self.blockchain = Blockchain()
        self.sockets = []
        self.app.add_route(self.blocks, '/blocks', methods=['GET'])
        self.app.add_route(self.mine_block, '/mineBlock', methods=['POST'])
        self.app.add_route(self.peers, '/peers', methods=['GET'])
        self.app.add_route(self.add_peer, '/addPeer', methods=['POST'])
        self.app.add_websocket_route(self.p2p_handler, '/')

    async def blocks(self, request):
        return json(self.blockchain.blocks)

    async def mine_block(self, request):

        try:
            newBlock = self.blockchain.generate_next_block(request.json["data"])
        except KeyError as e:
            return json({"status": False, "message": "pass value in data key"})
        self.blockchain.add_block(newBlock)
        await self.broadcast(self.response_latest_msg())
        return json(newBlock)

    async def peers(self, request):
        peers = map(lambda x: "{}:{}".format(x.remote_address[0], x.remote_address[1])
                    , self.sockets)
        return json(peers)

    async def add_peer(self, request):
        import asyncio
        asyncio.ensure_future(self.connect_to_peers([request.json["peer"]]),
                                             loop=asyncio.get_event_loop())
        return json({"status": True})

    async def connect_to_peers(self, newPeers):
        for peer in newPeers:
            logger.info(peer)
            try:
                ws = await websockets.connect(peer)

                await self.init_connection(ws)
            except Exception as e:
                logger.info(str(e))

    # initP2PServer WebSocket server
    async def p2p_handler(self, request, ws):
        logger.info('listening websocket p2p port on: %d' % port)


        try:
            await self.init_connection(ws)
        except (ConnectionClosed):
            await self.connection_closed(ws)

    async def connection_closed(self, ws):

        logger.critical("connection failed to peer")
        self.sockets.remove(ws)

    async def init_connection(self, ws):

        self.sockets.append(ws)
        await ws.send(JSON.dumps(self.query_chain_length_msg()))

        while True:
            await self.init_message_handler(ws)

    async def init_message_handler(self, ws):
        data = await ws.recv()
        message = JSON.loads(data)
        logger.info('Received message: {}'.format(data))

        await {
            QUERY_LATEST: self.send_latest_msg,
            QUERY_ALL: self.send_chain_msg,
            RESPONSE_BLOCKCHAIN: self.handle_blockchain_response
        }[message["type"]](ws, message)

    async def send_latest_msg(self, ws, *args):
        await ws.send(JSON.dumps(self.response_latest_msg()))

    async def send_chain_msg(self, ws, *args):

        await ws.send(JSON.dumps(self.response_chain_msg()))

    def response_chain_msg(self):
        return {
            'type': RESPONSE_BLOCKCHAIN,
            'data': JSON.dumps([block.dict() for block in self.blockchain.blocks])
        }

    def response_latest_msg(self):

        return {
            'type': RESPONSE_BLOCKCHAIN,
            'data': JSON.dumps([self.blockchain.get_latest_block().dict()])
        }

    async def handle_blockchain_response(self, ws, message):

        received_blocks = sorted(JSON.loads(message["data"]), key=lambda k: k['index'])
        logger.info(received_blocks)
        latest_block_received = received_blocks[-1]
        latest_block_held = self.blockchain.get_latest_block()
        if latest_block_received["index"] > latest_block_held.index:
            logger.info('blockchain possibly behind. We got: ' + str(latest_block_held.index)
                  + ' Peer got: ' + str(latest_block_received["index"]))
            if latest_block_held.hash == latest_block_received["previous_hash"]:
                logger.info("We can append the received block to our chain")

                self.blockchain.blocks.append(Block(**latest_block_received))
                await self.broadcast(self.response_latest_msg())
            elif len(received_blocks) == 1:
                logger.info("We have to query the chain from our peer")
                await self.broadcast(self.query_all_msg())
            else:
                logger.info("Received blockchain is longer than current blockchain")
                await self.replace_chain(received_blocks)
        else:
            logger.info('received blockchain is not longer than current blockchain. Do nothing')

    async def replace_chain(self, newBlocks):

        try:

            if self.blockchain.is_valid_chain(newBlocks) and len(newBlocks) > len(self.blockchain.blocks):
                logger.info('Received blockchain is valid. Replacing current blockchain with '
                            'received blockchain')
                self.blockchain.blocks = [Block(**block) for block in newBlocks]
                await self.broadcast(self.response_latest_msg())
            else:
                logger.info('Received blockchain invalid')
        except Exception as e:
            logger.info("Error in replace chain" + str(e))



    def query_chain_length_msg(self):

        return {'type': QUERY_LATEST}

    def query_all_msg(self):

        return {'type': QUERY_ALL}

    async def broadcast(self, message):

        for socket in self.sockets:
            logger.info(socket)
            await socket.send(JSON.dumps(message))


if __name__ == '__main__':

    server = Server()
    server.app.add_task(server.connect_to_peers(initialPeers))
    server.app.run(host='0.0.0.0', port=port, debug=True)
