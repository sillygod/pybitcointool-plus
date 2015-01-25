import unittest
import time
from bitcoin.api_manager import APIFactory
from bitcoin.api_interface import *
# must import api_interface to read the class
# definition


class TestApiManager(unittest.TestCase):

    def setUp(self):
        print('start test api manager')
        self.blockchain = APIFactory.get_class('BlockChainInfoAPI')
        self.blockr = APIFactory.get_class('BlockrAPI')
        self.insight = APIFactory.get_class('InsightAPI')

    def tearDown(self):
        pass

    def test_produce_api_class(self):
        """test whether api factory produce
        correct api class or not.
        """
        self.assertEquals(BlockChainInfoAPI, self.blockchain)
        self.assertEquals(BlockrAPI, self.blockr)
        self.assertEquals(InsightAPI, self.insight)


class TestApiImplement(unittest.TestCase):

    def setUp(self):
        print('start test api implement')
        self.address = '1MhxMbEh19LeeiSbEzBhqWFz6TcmiiYojq'

        self.blockchain = APIFactory.get_class('BlockChainInfoAPI')()
        self.blockr = APIFactory.get_class('BlockrAPI')()
        self.insight = APIFactory.get_class('InsightAPI')()

    def tearDown(self):
        pass

    def test_get_balance(self):
        """use three api to get the balance of specific address
        """

        print(self.insight.get_balance(self.address))
        print(self.blockr.get_balance(self.address))
        # print(self.blockchain.get_balance(self.address))

    def test_get_history(self):
        """here, we extract the time and tx infomation
        """

        # print(self.blockchain.history(self.address))
        blockr_data = []
        blockinfo_data = []
        insight_data = []

        temp = {'time': None, 'tx': None}

        for obj in self.blockr.history(self.address):
            temp['time'] = obj['time_utc']
            temp['tx'] = obj['tx']
            blockr_data.append(temp.copy())

        # for obj in self.blockchain.history(self.address):
        #     t = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.localtime(obj['time']))

        #     temp['time'] = t
        #     temp['tx'] = obj['output']
        #     blockinfo_data.append(temp.copy())

        for obj in self.insight.history(self.address):
            t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(obj['time']))
            temp['time'] = t
            temp['tx'] = obj['txid']
            insight_data.append(temp.copy())


        print(insight_data)
        sorted(blockinfo_data, key=lambda k: k['time'], reverse=True)
        sorted(insight_data, key=lambda k: k['time'], reverse=True)

        # # print(blockinfo_data)
        # print('=======================================================')
        print(insight_data)


