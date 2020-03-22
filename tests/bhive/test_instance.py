from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import range
from builtins import super
import mock
import string
import unittest
import random
from parameterized import parameterized
from pprint import pprint
from bhive import Hive
from bhive.amount import Amount
from bhive.witness import Witness
from bhive.account import Account
from bhive.instance import set_shared_steem_instance, shared_steem_instance, set_shared_config
from bhive.blockchain import Blockchain
from bhive.block import Block
from bhive.market import Market
from bhive.price import Price
from bhive.comment import Comment
from bhive.vote import Vote
from bhiveapi.exceptions import RPCConnection
from bhive.wallet import Wallet
from bhive.transactionbuilder import TransactionBuilder
from bhivebase.operations import Transfer
from bhivegraphenebase.account import PasswordKey, PrivateKey, PublicKey
from bhive.utils import parse_time, formatTimedelta
from bhive.nodelist import NodeList

# Py3 compatibility
import sys

core_unit = "STM"


class Testcases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.nodelist = NodeList()
        cls.nodelist.update_nodes(steem_instance=Hive(node=cls.nodelist.get_nodes(exclude_limited=False), num_retries=10))
        hv = Hive(node=cls.nodelist.get_nodes())
        hv.config.refreshBackup()
        hv.set_default_nodes(["xyz"])
        del hv

        cls.urls = cls.nodelist.get_nodes(exclude_limited=True)
        cls.bts = Hive(
            node=cls.urls,
            nobroadcast=True,
            num_retries=10
        )
        set_shared_steem_instance(cls.bts)
        acc = Account("bhive.app", steem_instance=cls.bts)
        comment = acc.get_blog(limit=20)[-1]
        cls.authorperm = comment.authorperm
        votes = acc.get_account_votes()
        last_vote = votes[-1]
        cls.authorpermvoter = '@' + last_vote['authorperm'] + '|' + acc["name"]

    @classmethod
    def tearDownClass(cls):
        hv = Hive(node=cls.nodelist.get_nodes())
        hv.config.recover_with_latest_backup()

    @parameterized.expand([
        ("instance"),
        ("hive")
    ])
    def test_account(self, node_param):
        if node_param == "instance":
            set_shared_steem_instance(self.bts)
            acc = Account("test")
            self.assertIn(acc.hive.rpc.url, self.urls)
            self.assertIn(acc["balance"].hive.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Account("test", steem_instance=Hive(node="https://abc.d", autoconnect=False, num_retries=1))
        else:
            set_shared_steem_instance(Hive(node="https://abc.d", autoconnect=False, num_retries=1))
            hv = self.bts
            acc = Account("test", steem_instance=hv)
            self.assertIn(acc.hive.rpc.url, self.urls)
            self.assertIn(acc["balance"].hive.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Account("test")

    @parameterized.expand([
        ("instance"),
        ("hive")
    ])
    def test_amount(self, node_param):
        if node_param == "instance":
            hv = Hive(node="https://abc.d", autoconnect=False, num_retries=1)
            set_shared_steem_instance(self.bts)
            o = Amount("1 HBD")
            self.assertIn(o.hive.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Amount("1 HBD", steem_instance=hv)
        else:
            set_shared_steem_instance(Hive(node="https://abc.d", autoconnect=False, num_retries=1))
            hv = self.bts
            o = Amount("1 HBD", steem_instance=hv)
            self.assertIn(o.hive.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Amount("1 HBD")

    @parameterized.expand([
        ("instance"),
        ("hive")
    ])
    def test_block(self, node_param):
        if node_param == "instance":
            set_shared_steem_instance(self.bts)
            o = Block(1)
            self.assertIn(o.hive.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Block(1, steem_instance=Hive(node="https://abc.d", autoconnect=False, num_retries=1))
        else:
            set_shared_steem_instance(Hive(node="https://abc.d", autoconnect=False, num_retries=1))
            hv = self.bts
            o = Block(1, steem_instance=hv)
            self.assertIn(o.hive.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Block(1)

    @parameterized.expand([
        ("instance"),
        ("hive")
    ])
    def test_blockchain(self, node_param):
        if node_param == "instance":
            set_shared_steem_instance(self.bts)
            o = Blockchain()
            self.assertIn(o.hive.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Blockchain(steem_instance=Hive(node="https://abc.d", autoconnect=False, num_retries=1))
        else:
            set_shared_steem_instance(Hive(node="https://abc.d", autoconnect=False, num_retries=1))
            hv = self.bts
            o = Blockchain(steem_instance=hv)
            self.assertIn(o.hive.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Blockchain()

    @parameterized.expand([
        ("instance"),
        ("hive")
    ])
    def test_comment(self, node_param):
        if node_param == "instance":
            set_shared_steem_instance(self.bts)
            o = Comment(self.authorperm)
            self.assertIn(o.hive.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Comment(self.authorperm, steem_instance=Hive(node="https://abc.d", autoconnect=False, num_retries=1))
        else:
            set_shared_steem_instance(Hive(node="https://abc.d", autoconnect=False, num_retries=1))
            hv = self.bts
            o = Comment(self.authorperm, steem_instance=hv)
            self.assertIn(o.hive.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Comment(self.authorperm)

    @parameterized.expand([
        ("instance"),
        ("hive")
    ])
    def test_market(self, node_param):
        if node_param == "instance":
            set_shared_steem_instance(self.bts)
            o = Market()
            self.assertIn(o.hive.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Market(steem_instance=Hive(node="https://abc.d", autoconnect=False, num_retries=1))
        else:
            set_shared_steem_instance(Hive(node="https://abc.d", autoconnect=False, num_retries=1))
            hv = self.bts
            o = Market(steem_instance=hv)
            self.assertIn(o.hive.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Market()

    @parameterized.expand([
        ("instance"),
        ("hive")
    ])
    def test_price(self, node_param):
        if node_param == "instance":
            set_shared_steem_instance(self.bts)
            o = Price(10.0, "HIVE/HBD")
            self.assertIn(o.hive.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Price(10.0, "HIVE/HBD", steem_instance=Hive(node="https://abc.d", autoconnect=False, num_retries=1))
        else:
            set_shared_steem_instance(Hive(node="https://abc.d", autoconnect=False, num_retries=1))
            hv = self.bts
            o = Price(10.0, "HIVE/HBD", steem_instance=hv)
            self.assertIn(o.hive.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Price(10.0, "HIVE/HBD")

    @parameterized.expand([
        ("instance"),
        ("hive")
    ])
    def test_vote(self, node_param):
        if node_param == "instance":
            set_shared_steem_instance(self.bts)
            o = Vote(self.authorpermvoter)
            self.assertIn(o.hive.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Vote(self.authorpermvoter, steem_instance=Hive(node="https://abc.d", autoconnect=False, num_retries=1))
        else:
            set_shared_steem_instance(Hive(node="https://abc.d", autoconnect=False, num_retries=1))
            hv = self.bts
            o = Vote(self.authorpermvoter, steem_instance=hv)
            self.assertIn(o.hive.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Vote(self.authorpermvoter)

    @parameterized.expand([
        ("instance"),
        ("hive")
    ])
    def test_wallet(self, node_param):
        if node_param == "instance":
            set_shared_steem_instance(self.bts)
            o = Wallet()
            self.assertIn(o.hive.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                o = Wallet(steem_instance=Hive(node="https://abc.d", autoconnect=False, num_retries=1))
                o.hive.get_config()
        else:
            set_shared_steem_instance(Hive(node="https://abc.d", autoconnect=False, num_retries=1))
            hv = self.bts
            o = Wallet(steem_instance=hv)
            self.assertIn(o.hive.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                o = Wallet()
                o.hive.get_config()

    @parameterized.expand([
        ("instance"),
        ("hive")
    ])
    def test_witness(self, node_param):
        if node_param == "instance":
            set_shared_steem_instance(self.bts)
            o = Witness("gtg")
            self.assertIn(o.hive.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Witness("gtg", steem_instance=Hive(node="https://abc.d", autoconnect=False, num_retries=1))
        else:
            set_shared_steem_instance(Hive(node="https://abc.d", autoconnect=False, num_retries=1))
            hv = self.bts
            o = Witness("gtg", steem_instance=hv)
            self.assertIn(o.hive.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Witness("gtg")

    @parameterized.expand([
        ("instance"),
        ("hive")
    ])
    def test_transactionbuilder(self, node_param):
        if node_param == "instance":
            set_shared_steem_instance(self.bts)
            o = TransactionBuilder()
            self.assertIn(o.hive.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                o = TransactionBuilder(steem_instance=Hive(node="https://abc.d", autoconnect=False, num_retries=1))
                o.hive.get_config()
        else:
            set_shared_steem_instance(Hive(node="https://abc.d", autoconnect=False, num_retries=1))
            hv = self.bts
            o = TransactionBuilder(steem_instance=hv)
            self.assertIn(o.hive.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                o = TransactionBuilder()
                o.hive.get_config()

    @parameterized.expand([
        ("instance"),
        ("hive")
    ])
    def test_steem(self, node_param):
        if node_param == "instance":
            set_shared_steem_instance(self.bts)
            o = Hive(node=self.urls)
            o.get_config()
            self.assertIn(o.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                hv = Hive(node="https://abc.d", autoconnect=False, num_retries=1)
                hv.get_config()
        else:
            set_shared_steem_instance(Hive(node="https://abc.d", autoconnect=False, num_retries=1))
            hv = self.bts
            o = hv
            o.get_config()
            self.assertIn(o.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                hv = shared_steem_instance()
                hv.get_config()

    def test_config(self):
        set_shared_config({"node": self.urls})
        set_shared_steem_instance(None)
        o = shared_steem_instance()
        self.assertIn(o.rpc.url, self.urls)
