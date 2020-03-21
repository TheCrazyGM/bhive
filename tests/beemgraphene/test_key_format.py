# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import str
import unittest
from beemgraphenebase.account import PrivateKey, PublicKey, Address
from beemgraphenebase.bip38 import encrypt, decrypt


key = {
    "public_key": u"STM7jDPoMwyjVH5obFmqzFNp4Ffp7G2nvC7FKFkrMBpo7Sy4uq5Mj",
    "private_key": u"20991828d456b389d0768ed7fb69bf26b9bb87208dd699ef49f10481c20d3e18",
    "private_key_WIF_format": u"5J4eFhjREJA7hKG6KcvHofHMXyGQZCDpQE463PAaKo9xXY6UDPq",
    "bts_address": u"STM8DvGQqzbgCR5FHiNsFf8kotEXr8VKD3mR",
    "pts_address": u"Po3mqkgMzBL4F1VXJArwQxeWf3fWEpxUf3",
    "encrypted_private_key": u"5e1ae410919c450dce1c476ae3ed3e5fe779ad248081d85b3dcf2888e698744d0a4b60efb7e854453bec3f6883bcbd1d",
    "blockchain_address": u"4f3a560442a05e4fbb257e8dc5859b736306bace",
    "Uncompressed_BTC": u"STMLAFmEtM8as1mbmjVcj5dphLdPguXquimn",
    "Compressed_BTC": u"STMANNTSEaUviJgWLzJBersPmyFZBY4jJETY",
    "Uncompressed_PTS": u"STMEgj7RM6FBwSoccGaESJLC3Mi18785bM3T",
    "Compressed_PTS": u"STMD5rYtofD6D4UHJH6mo953P5wpBfMhdMEi",
}


class Testcases(unittest.TestCase):
    def test_public_from_private(self):
        private_key = PrivateKey(key["private_key"])
        public_key = private_key.get_public_key()
        self.assertEqual(key["public_key"], str(public_key))

    def test_short_address(self):
        public_key = PublicKey(key["public_key"])
        self.assertEqual(key["bts_address"], str(public_key.address))

    def test_blockchain_address(self):
        public_key = PublicKey(key["public_key"])
        self.assertEqual(key["blockchain_address"], repr(public_key.address))

    def test_import_export(self):
        public_key = PublicKey(key["public_key"])
        self.assertEqual(key["public_key"], str(public_key))

    def test_to_wif(self):
        private_key = PrivateKey(key["private_key"])
        self.assertEqual(key["private_key_WIF_format"], str(private_key))

    def test_calc_pub_key(self):
        private_key = PrivateKey(key["private_key"])
        public_key = private_key.pubkey
        self.assertEqual(key["bts_address"], str(public_key.address))

    def test_btc_uncompressed(self):
        public_key = PublicKey(key["public_key"])
        address = Address(address=None, pubkey=public_key.unCompressed())
        self.assertEqual(str(key["Uncompressed_BTC"]), (format(address.derive256address_with_version(0), "STM")))

    def test_btc_compressed(self):
        public_key = PublicKey(key["public_key"])
        address = Address(address=None, pubkey=repr(public_key))
        self.assertEqual(str(key["Compressed_BTC"]), (format(address.derive256address_with_version(0), "STM")))

    def test_pts_uncompressed(self):
        public_key = PublicKey(key["public_key"])
        address = Address(address=None, pubkey=public_key.unCompressed())
        self.assertEqual(str(key["Uncompressed_PTS"]), (format(address.derive256address_with_version(56), "STM")))

    def test_pts_compressed(self):
        public_key = PublicKey(key["public_key"])
        address = Address(address=None, pubkey=repr(public_key))
        self.assertEqual(str(key["Compressed_PTS"]), (format(address.derive256address_with_version(56), "STM")))
