from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import str
from builtins import super
import unittest
from parameterized import parameterized
from bhive import Hive
from bhive.asset import Asset
from bhive.instance import set_shared_steem_instance
from bhive.exceptions import AssetDoesNotExistsException
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
        cls.bhive.app = Hive(
            node="https://api.hive.blog",
            nobroadcast=True,
            num_retries=10
        )
        set_shared_steem_instance(cls.bts)

    @parameterized.expand([
        ("normal"),
        ("bhive.app"),
    ])
    def test_assert(self, node_param):
        if node_param == "normal":
            hv = self.bts
        else:
            hv = self.hiveio
        with self.assertRaises(AssetDoesNotExistsException):
            Asset("FOObarNonExisting", full=False, steem_instance=hv)

    @parameterized.expand([
        ("normal", "HBD", "HBD", 3, "@@000000013"),
        ("normal", "HIVE", "HIVE", 3, "@@000000021"),
        ("normal", "VESTS", "VESTS", 6, "@@000000037"),
        ("normal", "@@000000013", "HBD", 3, "@@000000013"),
        ("normal", "@@000000021", "HIVE", 3, "@@000000021"),
        ("normal", "@@000000037", "VESTS", 6, "@@000000037"),
    ])
    def test_properties(self, node_param, data, symbol_str, precision, asset_str):
        if node_param == "normal":
            hv = self.bts
        else:
            hv = self.testnet
        asset = Asset(data, full=False, steem_instance=hv)
        self.assertEqual(asset.symbol, symbol_str)
        self.assertEqual(asset.precision, precision)
        self.assertEqual(asset.asset, asset_str)

    @parameterized.expand([
        ("normal"),
        ("hiveio"),
    ])
    def test_assert_equal(self, node_param):
        if node_param == "normal":
            hv = self.bts
        else:
            hv = self.hiveio
        asset1 = Asset("HBD", full=False, steem_instance=hv)
        asset2 = Asset("HBD", full=False, steem_instance=hv)
        self.assertTrue(asset1 == asset2)
        self.assertTrue(asset1 == "HBD")
        self.assertTrue(asset2 == "HBD")
        asset3 = Asset("HIVE", full=False, steem_instance=hv)
        self.assertTrue(asset1 != asset3)
        self.assertTrue(asset3 != "HBD")
        self.assertTrue(asset1 != "HIVE")

        a = {'asset': '@@000000021', 'precision': 3, 'id': 'HIVE', 'symbol': 'HIVE'}
        b = {'asset': '@@000000021', 'precision': 3, 'id': '@@000000021', 'symbol': 'HIVE'}
        self.assertTrue(Asset(a, steem_instance=hv) == Asset(b, steem_instance=hv))

    """
    # Mocker comes from pytest-mock, providing an easy way to have patched objects
    # for the life of the test.
    def test_calls(mocker):
        asset = Asset("USD", lazy=True, steem_instance=Hive(offline=True))
        method = mocker.patch.object(Asset, 'get_call_orders')
        asset.calls
        method.assert_called_with(10)
    """
