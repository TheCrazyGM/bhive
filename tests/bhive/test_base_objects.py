from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import super
import unittest
from bhive import Hive, exceptions
from bhive.instance import set_shared_steem_instance
from bhive.account import Account
from bhive.witness import Witness
from bhive.nodelist import NodeList


class Testcases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        nodelist = NodeList()
        nodelist.update_nodes(steem_instance=Hive(node=nodelist.get_nodes(exclude_limited=False), num_retries=10))
        cls.bts = Hive(
            node=nodelist.get_nodes(exclude_limited=True),
            nobroadcast=True,
            num_retries=10
        )
        set_shared_steem_instance(cls.bts)

    def test_Account(self):
        with self.assertRaises(
            exceptions.AccountDoesNotExistsException
        ):
            Account("FOObarNonExisting")

        c = Account("test")
        self.assertEqual(c["name"], "test")
        self.assertIsInstance(c, Account)

    def test_Witness(self):
        with self.assertRaises(
            exceptions.WitnessDoesNotExistsException
        ):
            Witness("FOObarNonExisting")

        c = Witness("jesta")
        self.assertEqual(c["owner"], "jesta")
        self.assertIsInstance(c.account, Account)
