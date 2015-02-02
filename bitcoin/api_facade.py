from api_interface import *
from api_manager import APIFactory


class ApiFacade(object):

    """this class's function is to handle all api
    and to check whether api work or not. it will
    choose the one worked if other api is dead.
    """

    def __init__(self):
        """give the priority for part of apis
        """
        self._api_priority = [
            'InsightAPI',
            'BlockrAPI',
            'BlockChainInfoAPI']

    def try_api_loop(self, func_name, *args):
        """encapsulate for dynamic call
        api function
        """
        for api_name in self._api_priority:
            try:
                api = APIFactory.get_class(api_name)()
                # to get instance of api class
                result = getattr(api, func_name)(*args)
                return result
            except Exception as e:
                print(e)
                print('---try to use another api---')
                continue

    def pushtx(self, tx):
        return self.try_api_loop('pushtx', tx)

    def history(self, address):
        return self.try_api_loop('history', address)

    def get_balance(self, address):
        return self.try_api_loop('get_balance', address)

    def get_tx_confirmation(self, tx):
        return self.try_api_loop('get_tx_confirmation', tx)
