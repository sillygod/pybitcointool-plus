from util import btc_to_satoshi
from util import satoshi_to_btc
from bitcoin import *
from api_facade import ApiFacade


def get_balance(unspent):
    balance = 0

    for u in unspent:
        balance += u['value']
    return balance


def simple_tx_inputs_outputs(from_addr, from_addr_unspent, to_addr, amount_to_send, txfee):

    selected_unspent = select(from_addr_unspent, amount_to_send + txfee)
    selected_unspent_bal = get_balance(selected_unspent)
    changeval = selected_unspent_bal - amount_to_send - txfee

    if to_addr[0] == 'v' or to_addr[0] == 'w':
        # stealth
        ephem_privkey = bc.random_key()
        nonce = int(bc.random_key()[:8], 16)
        if to_addr[0] == 'v':
            # network = 'btc'
            raise Exception(
                'Stealth address payments only supported on testnet at this time.')
        else:
            network = 'testnet'

        tx_outs = bc.mk_stealth_tx_outputs(
            to_addr, amount_to_send, ephem_privkey, nonce, network)
    else:
        tx_outs = [{'value': amount_to_send, 'address': to_addr}]

    if changeval > 0:
        tx_outs.append({'value': changeval, 'address': from_addr})

    return selected_unspent, tx_outs


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

    def sign_tx(self, to_address, amount, txfee):
        # if self.send_amount + self.txfee > self.balance:
        #     raise LowBalanceError("Insufficient funds to send {0} + {1} BTC.".format(
        #         satoshi_to_btc(self.send_amount), satoshi_to_btc(self.txfee)))
        unspent_tx = unspent(self.address)

        tx_ins, tx_outs = simple_tx_inputs_outputs(
            self.address, unspent_tx, to_address, amount, txfee)

        tx = mktx(tx_ins, tx_outs)
        # Sign transaction
        for i in range(len(tx_ins)):
            tx = sign(tx, i, self.priv)

        return tx_ins, tx_outs, tx, deserialize(tx)

    def get_history(self):
        return self._api.history(self.address)

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

        # TODO: solve below issue
        issue: if I import the key from multi-bit, I would not to be able to pushtx
        error message is An outpoint is already spent in. how to solve this
        '''
        h = history(self.address)
        # h = self._api.history(self.address)
        outs = [{'value': amount, 'address': dest}]

        if self.address[:1] != '1':
            # if not 1, this address is not multi-sig addr
            # how do I apply fee here..
            tx = mktx(h, outs)
            sig1 = multisign(tx, 0, self.script, self.priv[0])
            sig2 = multisign(tx, 0, self.script, self.priv[1])
            sig3 = multisign(tx, 0, self.script, self.priv[2])
            tx2 = apply_multisignatures(tx, 0, self.script, sig1, sig2, sig3)
            return self._api.pushtx(tx2)

        else:
            tx = self.sign_tx(dest, amount, fee)[2]
            return self._api.pushtx(tx)
