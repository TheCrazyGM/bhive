from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import range
from builtins import super
import mock
import string
import unittest
from parameterized import parameterized
import random
import json
from pprint import pprint
from bhive import Hive, exceptions
from bhive.amount import Amount
from bhive.memo import Memo
from bhive.version import version as bsteem_version
from bhive.wallet import Wallet
from bhive.witness import Witness
from bhive.account import Account
from bhivegraphenebase.account import PrivateKey
from bhive.instance import set_shared_steem_instance
from bhive.nodelist import NodeList
from bhive.hiveconnect import HiveConnect
# Py3 compatibility
import sys
core_unit = "STM"


class Testcases(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        nodelist = NodeList()
        nodelist.update_nodes(steem_instance=Hive(node=nodelist.get_nodes(exclude_limited=False), num_retries=10))
        cls.bts = Hive(
            node=nodelist.get_nodes(exclude_limited=True),
            nobroadcast=True,
            unsigned=True,
            data_refresh_time_seconds=900,
            num_retries=10)

        cls.account = Account("test", full=True, steem_instance=cls.bts)

    def test_transfer(self):
        bts = self.bts
        acc = self.account
        acc.hive.txbuffer.clear()
        tx = acc.transfer(
            "test1", 1.000, "HIVE", memo="test")
        sc2 = HiveConnect(steem_instance=bts)
        url = sc2.url_from_tx(tx)
        url_test = 'https://hiveconnect.com/sign/transfer?from=test&to=test1&amount=1.000+HIVE&memo=test'
        self.assertEqual(len(url), len(url_test))
        self.assertEqual(len(url.split('?')), 2)
        self.assertEqual(url.split('?')[0], url_test.split('?')[0])

        url_parts = (url.split('?')[1]).split('&')
        url_test_parts = (url_test.split('?')[1]).split('&')

        self.assertEqual(len(url_parts), 4)
        self.assertEqual(len(list(set(url_parts).intersection(set(url_test_parts)))), 4)

    def test_login_url(self):
        bts = self.bts
        sc2 = HiveConnect(steem_instance=bts)
        url = sc2.get_login_url("localhost", scope="login,vote")
        url_test = 'https://hiveconnect.com/oauth2/authorize?client_id=None&redirect_uri=localhost&scope=login,vote'
        self.assertEqual(len(url), len(url_test))
        self.assertEqual(len(url.split('?')), 2)
        self.assertEqual(url.split('?')[0], url_test.split('?')[0])

        url_parts = (url.split('?')[1]).split('&')
        url_test_parts = (url_test.split('?')[1]).split('&')

        self.assertEqual(len(url_parts), 3)
        self.assertEqual(len(list(set(url_parts).intersection(set(url_test_parts)))), 3)
