"""Before run this test, remember to run the json rpc server
"""


import unittest
import requests
import json


class TestRPC(unittest.TestCase):

    """
    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testSendCreateWallet(self):

        url = 'http://localhost:8778'
        data = {'method': 'createWallet', 'id':1, 'param': ''}

        r = requests.post(url, data=json.dumps(data))
        print(r.json()['result'])
