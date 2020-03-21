from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import super
import unittest
from parameterized import parameterized
from bhive import Hive
from bhive.instance import set_shared_hive_instance
from bhive.transactionbuilder import TransactionBuilder
from bhivebase.signedtransactions import Signed_Transaction
from bhivebase.operations import Transfer
from bhive.account import Account
from bhive.block import Block
from bhivegraphenebase.base58 import Base58
from bhive.amount import Amount
from bhive.exceptions import (
    InsufficientAuthorityError,
    MissingKeyError,
    InvalidWifError,
    WalletLocked
)
from bhiveapi import exceptions
from bhive.wallet import Wallet
from bhive.utils import formatTimeFromNow
from bhive.nodelist import NodeList
wif = "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3"


class Testcases(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        nodelist = NodeList()
        nodelist.update_nodes(hive_instance=Hive(node=nodelist.get_nodes(exclude_limited=False), num_retries=10))
        node_list = nodelist.get_nodes(exclude_limited=True)
        cls.hv = Hive(
            node=node_list,
            keys={"active": wif, "owner": wif, "memo": wif},
            nobroadcast=True,
            num_retries=10
        )
        cls.hiveio = Hive(
            node="https://api.hive.blog",
            nobroadcast=True,
            keys={"active": wif, "owner": wif, "memo": wif},
            num_retries=10
        )
        set_shared_hive_instance(cls.hv)
        cls.hv.set_default_account("test")

    def test_emptyTransaction(self):
        hv = self.hv
        tx = TransactionBuilder(hive_instance=hv)
        self.assertTrue(tx.is_empty())
        self.assertTrue(tx["ref_block_num"] is not None)

    def test_verify_transaction(self):
        hv = self.hv
        block = Block(22005665, hive_instance=hv)
        trx = block.transactions[28]
        signed_tx = Signed_Transaction(trx)
        key = signed_tx.verify(chain=hv.chain_params, recover_parameter=False)
        public_key = format(Base58(key[0]), hv.prefix)
        self.assertEqual(public_key, "STM4tzr1wjmuov9ftXR6QNv7qDWsbShMBPQpuwatZsfSc5pKjRDfq")
