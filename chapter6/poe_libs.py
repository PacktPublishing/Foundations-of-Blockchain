from datetime import datetime

from multichain_driver import MultichainClient


class Document(object):

    def __init__(self):
        self.client = MultichainClient().connect()
        self.stream = 'poe'

    def verify(self, digest):
        """verifies the existence of a document in blockchain"""

        return self.fetch_by_key(digest)

    def publish(self, key, value):
        """publishes the existence of a document in blockchain"""

        return self.client.publish(self.stream, key, value)

    def fetch_latest(self, count):
        """fetches the last inserted docs from blockchain"""

        latest_docs = []
        for doc in self.client.liststreamitems(self.stream)[::-1][:count]:
            blocktime = datetime.fromtimestamp(int(doc.get('blocktime'))).strftime("%Y-%m-%d %X UTC") if doc.get('blocktime') else None
            latest_docs.append({"digest": doc.get('key'),
                                "blocktime": blocktime,
                                "confirmations": doc.get('confirmations')})

        return latest_docs

    def fetch_by_key(self, key):
        """fetches the existence info of a document in blockchain"""

        return self.client.liststreamkeyitems(self.stream, key)

    def fetch_by_txid(self, tx_id):

        return self.client.getwallettransaction(tx_id)



