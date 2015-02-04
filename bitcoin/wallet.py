from bitcoin import *
from api_facade import ApiFacade


class Wallet(object):

    '''a simple wallet for handling *one* private key and contain some function
    like a real world wallet. Furthermore, this can create a sigle key address or multi-sig
    address wallet.

    There are three ways to create your wallet.
    1. createWallet
    2. import_privatekey
    3. createMultisigWallet

    1 and 2 are for single key
    3 for multi-sig use

    '''

    def __init__(self):
        self._api = ApiFacade()
        self.priv = ''
        self.address = ''
        self.script = ''

    def createMultisigWallet(self):
        '''randomly create 4 priv key, and rule a 3 of 4 address
        # NOTE: situation is still not confirm..
        '''
        privkeys = [random_key() for i in range(4)]
        pubkeys = [privtopub(key) for key in privkeys]
        self.priv = privkeys

        self.script = mk_multisig_script(pubkeys, 3, 4)
        self.address = scriptaddr(self.script)

    def get_history(self):
        return self_api.history()

    def createWallet(self, brainwalletpassword):
        self.priv = sha256(brainwalletpassword)
        self.pub = privtopub(self.priv)
        self.address = pubtoaddr(self.pub)

    def import_privatekey(self, privatekey):
        '''This is for single key use..
        '''
        self.priv = privatekey
        self.address = privtoaddr(privatekey)

    def export_privatekey(self):
        return self.priv

    def get_balance(self):
        return self._api.get_balance(self.address)

    def sendBTC(self, dest, amount, fee=10000):
        '''In order to send money, we need to get the previous transaction history
        and then make an out rule, sign the transactions

        #TODO: solve below issue
        issue: if I import the key from multi-bit, I would not to be able to pushtx
        error message is An outpoint is already spent in. how to solve this
        '''
        h = history(self.address)
        out = [{'value': amount, 'address': dest}]

        if self.address[:1] != '1':
            # if not 1, this address is not multi-sig addr
            # how do I apply fee here..
            tx = mktx(h, out)
            sig1 = multisign(tx, 0, self.script, self.priv[0])
            sig2 = multisign(tx, 0, self.script, self.priv[1])
            sig3 = multisign(tx, 0, self.script, self.priv[2])
            tx2 = apply_multisignatures(tx, 0, self.script, sig1, sig2, sig3)

        else:
            # tx = mktx(h, out)
            # tx2 = sign(tx, 0, self.priv)
            # tx3 = sign(tx2, 1, self.priv)
            tx = mksend(h, out, self.address, fee) # it is really able to set fee
            tx2 = sign(tx, 0, self.priv)

        return self._api.pushtx(tx2)
