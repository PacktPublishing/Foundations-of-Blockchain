from Savoir import Savoir


class MultichainClient(object):
    """multichain client driver to access rpc wrapper of python"""

    def __init__(self, **kwargs):

        # replace the configs with multichain configs

        self.rpcuser = kwargs.get('rpcuser', 'multichainrpc')
        self.rpcpasswd = kwargs.get('rpcpasswd', 'HFzmag67bJg2f4YuExgVDqQK5VfnvXRS5SKrByuCgiXm')
        self.rpchost = kwargs.get('rpchost', 'localhost')
        self.rpcport = kwargs.get('rpcport', '4416')
        self.chainname = kwargs.get('chainname', 'testchain')

    def connect(self):
        """connects to rpc interface"""

        try:
            api = Savoir(self.rpcuser, self.rpcpasswd, self.rpchost,
                         self.rpcport, self.chainname)
            return api

        except Exception as e:
            return False
