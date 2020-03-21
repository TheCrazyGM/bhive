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
from bhive import Hive
from bhive.amount import Amount
from bhive.memo import Memo
from bhive.version import version as bhive_version
from bhive.wallet import Wallet
from bhive.witness import Witness
from bhive.account import Account
from bhivegraphenebase.account import PrivateKey
from bhive.instance import set_shared_hive_instance, shared_hive_instance
from bhive.nodelist import NodeList
# Py3 compatibility
import sys
core_unit = "STM"
wif = "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3"


class Testcases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        hv = shared_hive_instance()
        hv.config.refreshBackup()
        nodelist = NodeList()
        nodelist.update_nodes(hive_instance=Hive(node=nodelist.get_nodes(exclude_limited=False), num_retries=10))

        cls.hv = Hive(
            node=nodelist.get_nodes(exclude_limited=True),
            nobroadcast=True,
            # We want to bundle many operations into a single transaction
            bundle=True,
            num_retries=10
            # Overwrite wallet to use this list of wifs only
        )

        cls.hv.set_default_account("test")
        set_shared_hive_instance(cls.hv)
        # self.hv.newWallet("TestingOneTwoThree")

        cls.wallet = Wallet(hive_instance=cls.hv)
        cls.wallet.wipe(True)
        cls.wallet.newWallet(pwd="TestingOneTwoThree")
        cls.wallet.unlock(pwd="TestingOneTwoThree")
        cls.wallet.addPrivateKey(wif)

    @classmethod
    def tearDownClass(cls):
        hv = shared_hive_instance()
        hv.config.recover_with_latest_backup()

    def test_set_default_account(self):
        hv = self.hv
        hv.set_default_account("bhivebot")

        self.assertEqual(hv.config["default_account"], "bhivebot")
