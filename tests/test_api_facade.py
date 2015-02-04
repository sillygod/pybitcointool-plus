import unittest
from bitcoin.api_facade import ApiFacade


class TestApiFacade(unittest.TestCase):

    """test the api_facade class's functions.
    below, test each class method independent
    """

    def setUp(self):
        self.api = ApiFacade()
        self.transaction = '7e1e97f2a0ae26a289945187212a680e663060cbcc96c5ede000b6925c5c9774'
        self.address = '1MhxMbEh19LeeiSbEzBhqWFz6TcmiiYojq'

    def tearDown(self):
        pass

    def test_push(self):
        """well, this test need a real bitcoin coin
        to test...
        """
        pass

    def test_history(self):
        print(self.api.history(self.address))

    def test_get_balance(self):
        print(self.api.get_balance(self.address))

    def test_tx_confirmation(self):
        print(self.api.get_tx_confirmation(self.transaction))
