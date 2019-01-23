import binascii
import json as JSON

from base64 import b64encode, b64decode
from datetime import datetime
from sanic import Sanic
from sanic.response import json
from sanic_cors import CORS, cross_origin

from poe_libs import Document

port = 8000


class Server(object):

    def __init__(self):

        self.app = Sanic()
        CORS(self.app)
        self.document = Document()

        self.app.add_route(self.verify, '/verify', methods=['GET'])
        self.app.add_route(self.publish, '/publish', methods=['POST'])
        self.app.add_route(self.details, '/details', methods=['GET'])

    async def verify(self, request):
        """returns details about verified document"""

        digest = request.args.get('digest')
        verified_docs = self.document.verify(digest)
        response_data = []
        for doc in verified_docs:
            meta_data = JSON.loads(b64decode(binascii.a2b_hex(doc.get('data'))).decode())

            doc = {"digest": digest,
                   "transaction_id": doc.get('txid'),
                   "confirmations": doc.get('confirmations'),
                   "blocktime": doc.get('blocktime'),
                   "name": meta_data.get('name'),
                   "email": meta_data.get('email'),
                   "message": meta_data.get('message'),
                   "recorded_timestamp_UTC": doc.get('blocktime'),
                   "readable_time_UTC": datetime.fromtimestamp(int(doc.get('blocktime'))).
                       strftime("%c")}
            response_data.append(doc)

        return json(response_data)

    async def publish(self, request):
        """publishes document detail and returns its block info"""

        try:
            json_data = {'name': request.form.get('name'),
                         'email': request.form.get('email'),
                         'message': request.form.get('message'),
                         'digest': request.form.get('digest')}
            json_string = JSON.dumps(json_data)
            encoded = b64encode(json_string.encode('utf-8'))
            hex_encoded = binascii.b2a_hex(encoded).decode()
            tx_id = self.document.publish(json_data['digest'], hex_encoded)
            tx_info = self.document.fetch_by_txid(tx_id)

            response_data = {'long_url': None,
                             'short_url': None,
                             'digest': json_data['digest'],
                             'transaction_id': tx_id,
                             'confirmations': tx_info.get('confirmations'),
                             'blockhash': tx_info.get('blockhash'),
                             'blocktime': tx_info.get('blocktime'),
                             'name': json_data['name'],
                             'email': json_data['email'],
                             'message': json_data['message'],
                             'timestamp': datetime.now().timestamp(),
                             'status': True}
        except Exception as e:

            response_data = {'status': False}

        return json(response_data)

    async def details(self, request):
        """returns details of latest inserted documents"""

        latest_docs = self.document.fetch_latest(int(request.args.get('count')))
        return json(latest_docs)


if __name__ == '__main__':
    """main function to serve the api"""

    server = Server()
    server.app.run(host='0.0.0.0', port=port, debug=True)
