from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import range
from builtins import super
import mock
import string
import time
import unittest
from parameterized import parameterized
import random
import itertools
from pprint import pprint
from bhive import Hive
from bhiveapi.hivenoderpc import HiveNodeRPC
from bhiveapi.websocket import HiveWebsocket
from bhiveapi import exceptions
from bhiveapi.exceptions import NumRetriesReached, CallRetriesReached
from bhive.instance import set_shared_steem_instance
from bhive.nodelist import NodeList
# Py3 compatibility
import sys

wif = "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3"
core_unit = "STM"


class Testcases(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        nodelist = NodeList()
        nodelist.update_nodes(steem_instance=Hive(node=nodelist.get_nodes(normal=True, appbase=True), num_retries=3))
        cls.nodes = nodelist.get_nodes()
        if "https://api.hive.blog" in cls.nodes:
            cls.nodes.remove("https://api.hive.blog")
        cls.nodes_steemit = ["https://api.hive.blog"]

        cls.appbase = Hive(
            node=cls.nodes,
            nobroadcast=True,
            keys={"active": wif, "owner": wif, "memo": wif},
            num_retries=10
        )
        cls.rpc = HiveNodeRPC(urls=cls.nodes_steemit)
        # from getpass import getpass
        # self.bts.wallet.unlock(getpass())
        set_shared_steem_instance(cls.nodes_steemit)
        cls.appbase.set_default_account("test")

    def get_reply(self, msg):
        reply = '<html>  <head><title>403 Forbidden</title></head><body bgcolor="white"><center><h1>' \
                '%s</h1></center><hr><center>nginx</center></body>    </html>' % (msg)
        return reply

    def test_appbase(self):
        bts = self.appbase
        self.assertTrue(bts.chain_params['min_version'] == '0.19.10')
        self.assertTrue(bts.rpc.get_use_appbase())
        self.assertTrue(isinstance(bts.rpc.get_config(api="database"), dict))
        with self.assertRaises(
            exceptions.NoApiWithName
        ):
            bts.rpc.get_config(api="abc")
        with self.assertRaises(
            exceptions.NoMethodWithName
        ):
            bts.rpc.get_config_abc()

    def test_connect_test_node(self):
        rpc = self.rpc
        self.assertIn(rpc.url, self.nodes + self.nodes_steemit)
        rpc.rpcclose()
        rpc.rpcconnect()
        self.assertIn(rpc.url, self.nodes + self.nodes_steemit)

    def test_connect_test_node2(self):
        rpc = self.rpc
        self.assertIn(rpc.url, self.nodes + self.nodes_steemit)
        rpc.next()
        self.assertIn(rpc.url, self.nodes + self.nodes_steemit)

    def test_connect_test_str_list(self):
        str_list = ""
        for node in self.nodes:
            str_list += node + ";"
        str_list = str_list[:-1]
        rpc = HiveNodeRPC(urls=str_list)
        self.assertIn(rpc.url, self.nodes + self.nodes_steemit)
        rpc.next()
        self.assertIn(rpc.url, self.nodes + self.nodes_steemit)

    def test_connect_test_str_list2(self):
        str_list = ""
        for node in self.nodes:
            str_list += node + ","
        str_list = str_list[:-1]
        rpc = HiveNodeRPC(urls=str_list)
        self.assertIn(rpc.url, self.nodes + self.nodes_steemit)
        rpc.next()
        self.assertIn(rpc.url, self.nodes + self.nodes_steemit)

    def test_server_error(self):
        rpc = self.rpc
        with self.assertRaises(
            exceptions.RPCErrorDoRetry
        ):
            rpc._check_for_server_error(self.get_reply("500 Internal Server Error"))
        with self.assertRaises(
            exceptions.RPCError
        ):
            rpc._check_for_server_error(self.get_reply("501 Not Implemented"))

        with self.assertRaises(
            exceptions.RPCErrorDoRetry
        ):
            rpc._check_for_server_error(self.get_reply("502 Bad Gateway"))

        with self.assertRaises(
            exceptions.RPCErrorDoRetry
        ):
            rpc._check_for_server_error(self.get_reply("503 Service Temporarily Unavailable"))

        with self.assertRaises(
            exceptions.RPCErrorDoRetry
        ):
            rpc._check_for_server_error(self.get_reply("504 Gateway Time-out"))

        with self.assertRaises(
            exceptions.RPCError
        ):
            rpc._check_for_server_error(self.get_reply("505 HTTP Version not supported"))
        with self.assertRaises(
            exceptions.RPCError
        ):
            rpc._check_for_server_error(self.get_reply("506 Variant Also Negotiates"))

        with self.assertRaises(
            exceptions.RPCError
        ):
            rpc._check_for_server_error(self.get_reply("507 Insufficient Storage"))

        with self.assertRaises(
            exceptions.RPCError
        ):
            rpc._check_for_server_error(self.get_reply("508 Loop Detected"))

        with self.assertRaises(
            exceptions.RPCError
        ):
            rpc._check_for_server_error(self.get_reply("509 Bandwidth Limit Exceeded"))
        with self.assertRaises(
            exceptions.RPCError
        ):
            rpc._check_for_server_error(self.get_reply("510 Not Extended"))

        with self.assertRaises(
            exceptions.RPCError
        ):
            rpc._check_for_server_error(self.get_reply("511 Network Authentication Required"))

    def test_num_retries(self):
        with self.assertRaises(
            NumRetriesReached
        ):
            HiveNodeRPC(urls="https://wrong.link.com", num_retries=2, timeout=1)
        with self.assertRaises(
            NumRetriesReached
        ):
            HiveNodeRPC(urls="https://wrong.link.com", num_retries=3, num_retries_call=3, timeout=1)
        nodes = ["https://httpstat.us/500", "https://httpstat.us/501", "https://httpstat.us/502", "https://httpstat.us/503",
                 "https://httpstat.us/505", "https://httpstat.us/511", "https://httpstat.us/520", "https://httpstat.us/522",
                 "https://httpstat.us/524"]
        with self.assertRaises(
            NumRetriesReached
        ):
            HiveNodeRPC(urls=nodes, num_retries=0, num_retries_call=0, timeout=1)

    def test_error_handling(self):
        rpc = HiveNodeRPC(urls=self.nodes_steemit, num_retries=2, num_retries_call=3)
        with self.assertRaises(
            exceptions.NoMethodWithName
        ):
            rpc.get_wrong_command()
        with self.assertRaises(
            exceptions.UnhandledRPCError
        ):
            rpc.get_accounts("test")

    def test_error_handling_appbase(self):
        rpc = HiveNodeRPC(urls=self.nodes_steemit, num_retries=2, num_retries_call=3)
        with self.assertRaises(
            exceptions.NoMethodWithName
        ):
            rpc.get_wrong_command()
        with self.assertRaises(
            exceptions.NoApiWithName
        ):
            rpc.get_block({"block_num": 1}, api="wrong_api")
