"""An Interface for bitcoin api
Using Factory design pattern to accept to different api address
"""

import abc


class IBTCApi:

    """this is an interface for bitcoin api
    """

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def pushtx(tx):
        """
        """
        raise NotImplementedError

    @abc.abstractmethod
    def history(address):
        """
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_balance(address):
        """
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_currency_rate():
        """
        """
        raise NotImplementedError


class BlockChainInfoAPI(IBTCApi):

    """
    """

    def __init__(self):
        pass

    def pushtx(tx):
        pass

    def history(address):
        pass

    def get_balance(address):
        pass

    def get_currency_rate():
        pass


class BlockerAPI(IBTCApi):

    """
    """

    def __init__(self):
        pass

    def pushtx(tx):
        pass

    def history(address):
        pass

    def get_balance(address):
        pass

    def get_currency_rate():
        pass


