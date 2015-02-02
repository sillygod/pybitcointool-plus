"""An Interface for bitcoin api
Using Factory design pattern to accept to different api address

#DOTO: rule the history format
"""

import abc
import re
import json
from bci import history

from api_manager import APIFactory
from util import call_api
from util import satoshi_to_btc


class IBTCApi:

    """this is an interface for bitcoin api
    """

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def pushtx(self, tx):
        """push a format hex transaction
        """
        raise NotImplementedError

    @abc.abstractmethod
    def history(self, address):
        """here we need to make a specific json
        format
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_balance(self, address):
        """get the balance of the address
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_tx_confirmation(self, tx):
        """
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_currency_rate(self):
        """
        """
        raise NotImplementedError


class BlockChainInfoAPI(IBTCApi):

    """Implemnt blockchain version of bitcoin api
    interface
    """

    __metaclass__ = APIFactory

    identifier = 'BlockChainInfoAPI'

    def __init__(self):
        self._base_url = 'https://blockchain.info/'

    def pushtx(self, tx):
        """push the transaction
        """
        if not re.match('^[0-9a-fA-F]*$', tx):
            tx = tx.encode('hex')
        return call_api(self._base_url, 'pushtx', {'tx': tx})

    def unspent(self, address):
        """to get unspen of the address
        """
        result = []

        try:
            data = call_api(self._base_url, 'unspent?address='+address)
        except Exception as e:
            print(e)

        try:
            jsonobj = json.loads(data)
            for obj in jsonobj['unspent_outputs']:
                # to get tx_hash big endian
                h = obj['tx_hash_big_endian']
                result.append({
                    "output": h+':'+str(obj['tx_output_n']),
                    "value": obj['value']
                })
        except:
            raise Exception("Failed to decode data: "+data)

        return result

    def get_tx_confirmation(self, tx):
        """In block chain info, there is no api to
        get transaction confirmation
        """
        block_count = call_api(self._base_url, 'q/getblockcount')

        source = 'tx/{}?show_adv=false&format=json'.format(tx)
        data = call_api(self._base_url, source)

        try:
            jsonobj = json.loads(data)
        except:
            raise Exception("Failed to decode data: "+data)

        block_height = jsonobj['block_height']

        return int(block_count) - int(block_height) + 1

    def history(self, address):
        """call pybitcointool history function
        to get the result
        """
        h = history(address)
        return h

    def get_balance(self, address):
        """get the balance of the address in BTC
        """
        data = self.unspent(address)
        value = 0.0

        for o in data:
            value += o['value']

        return satoshi_to_btc(value)

    def get_currency_rate(self, currency_type):
        """use bitcoin api rate
        give the param currency_type to get
        correspond value
        """
        data = call_api(self._base_url, 'ticker')

        try:
            jsonobj = json.loads(data)

        except:
            raise Exception('Failed to decode data: '+data)

        try:
            rate = jsonobj[currency_type]
        except:
            raise Exception('unsupported currency')

        return rate['last']


class BlockrAPI(IBTCApi):

    """
    """

    __metaclass__ = APIFactory

    identifier = 'BlockrAPI'

    def __init__(self):
        self._base_url = 'http://btc.blockr.io/api/v1/'

    def pushtx(self, tx):
        """call blockr api to push tx
        """
        if not re.match('^[0-9a-fA-F]*$', tx):
            tx = tx.encode('hex')
        return call_api(self._base_url, 'tx/push', {'tx': tx})

    def history(self, address):
        """call api to get the tx history of this
        address
        """
        data = call_api(self._base_url, 'address/txs/{}'.format(address))

        try:
            jsonobj = json.loads(data)
        except:
            raise Exception('Failed to decode data: '+data)

        # TODO:
        # will this return a list of dict?
        return jsonobj['data']['txs']

    def get_tx_confirmation(self, tx):
        """call blockr api to get tx's confirmation
        """
        data = call_api(self._base_url, 'tx/info/{}'.format(tx))

        try:
            jsonobj = json.loads(data)
        except:
            raise Exception('Failed to decode data: '+data)

        return jsonobj['data']['confirmations']

    def get_balance(self, address):
        """call api to get the balance of address
        in BTC
        """
        data = call_api(self._base_url, 'address/balance/{}'.format(address))
        try:
            jsonobj = json.loads(data)
        except:
            raise Exception('Failed to decode data: '+data)

        return jsonobj['data']['balance']

    def get_currency_rate(self):
        pass


class InsightAPI(IBTCApi):

    """
    """

    __metaclass__ = APIFactory

    identifier = 'InsightAPI'

    def __init__(self):
        self._base_url = 'http://106.186.126.188:3000/'

    def get_tx_info(self, tx):
        """call our node's api to get the
        information of transaction
        """
        data = call_api(self._base_url, 'api/tx/{}'.format(tx))

        try:
            jsonobj = json.loads(data)
        except:
            raise Exception('Failed to decode data: '+data)

        return jsonobj

    def get_addr_info(self, address):
        """call our node's api to get the
        information of address
        """
        data = call_api(self._base_url, 'api/addr/{}'.format(address))

        try:
            jsonobj = json.loads(data)
        except:
            raise Exception('Failed to decode data: '+data)

        return jsonobj

    # above two are helper function

    def get_tx_confirmation(self, tx):
        """
        """
        jsonobj = self.get_tx_info(tx)

        return jsonobj['confirmations']

    def pushtx(self, tx):
        """
        """
        if not re.match('^[0-9a-fA-F]*$', tx):
            tx = tx.encode('hex')

        return call_api(self._base_url, 'api/tx/send', {'rawtx': tx})

    def history(self, address):
        """
        """
        data = call_api(self._base_url, 'api/txs/?address={}'.format(address))

        try:
            jsonobj = json.loads(data)
        except:
            raise Exception('Failed to decode data: '+data)

        return jsonobj['txs']

    def get_balance(self, address):
        """call our node's api to get the balance
        of address in BTC
        """
        jsonobj = self.get_addr_info(address)

        return jsonobj['balance']

    def get_currency_rate(self):
        pass
