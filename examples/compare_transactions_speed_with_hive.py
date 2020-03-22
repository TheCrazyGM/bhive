from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import bytes
from builtins import chr
from builtins import range
from builtins import super
import random
from pprint import pprint
from binascii import hexlify
from collections import OrderedDict

from bhivebase import (
    transactions,
    memo,
    operations,
    objects
)
from bhivebase.objects import Operation
from bhivebase.signedtransactions import Signed_Transaction
from bhivegraphenebase.account import PrivateKey
from bhivegraphenebase import account
from bhivebase.operationids import getOperationNameForId
from bhivegraphenebase.py23 import py23_bytes, bytes_types
from bhive.amount import Amount
from bhive.asset import Asset
from bhive.hive import Hive
import time

from hive import Hive as hiveHive
from hivebase.account import PrivateKey as hivePrivateKey
from hivebase.transactions import SignedTransaction as hiveSignedTransaction
from hivebase import operations as hiveOperations
from timeit import default_timer as timer


class BhiveTest(object):

    def setup(self):
        self.prefix = u"STEEM"
        self.default_prefix = u"STM"
        self.wif = "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3"
        self.ref_block_num = 34294
        self.ref_block_prefix = 3707022213
        self.expiration = "2016-04-06T08:29:27"
        self.hv = Hive(offline=True)

    def doit(self, printWire=False, ops=None):
        ops = [Operation(ops)]
        tx = Signed_Transaction(ref_block_num=self.ref_block_num,
                                ref_block_prefix=self.ref_block_prefix,
                                expiration=self.expiration,
                                operations=ops)
        start = timer()
        tx = tx.sign([self.wif], chain=self.prefix)
        end1 = timer()
        tx.verify([PrivateKey(self.wif, prefix=u"STM").pubkey], self.prefix)
        end2 = timer()
        return end2 - end1, end1 - start


class HiveTest(object):

    def setup(self):
        self.prefix = u"STEEM"
        self.default_prefix = u"STM"
        self.wif = "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3"
        self.ref_block_num = 34294
        self.ref_block_prefix = 3707022213
        self.expiration = "2016-04-06T08:29:27"

    def doit(self, printWire=False, ops=None):
        ops = [hiveOperations.Operation(ops)]
        tx = hiveSignedTransaction(ref_block_num=self.ref_block_num,
                                    ref_block_prefix=self.ref_block_prefix,
                                    expiration=self.expiration,
                                    operations=ops)
        start = timer()
        tx = tx.sign([self.wif], chain=self.prefix)
        end1 = timer()
        tx.verify([hivePrivateKey(self.wif, prefix=u"STM").pubkey], self.prefix)
        end2 = timer()
        return end2 - end1, end1 - start


if __name__ == "__main__":
    steem_test = HiveTest()
    bsteem_test = BhiveTest()
    steem_test.setup()
    bsteem_test.setup()
    steem_times = []
    bsteem_times = []
    loops = 50
    for i in range(0, loops):
        print(i)
        opHive = hiveOperations.Transfer(**{
            "from": "foo",
            "to": "baar",
            "amount": "111.110 HIVE",
            "memo": "Fooo"
        })
        opBhive = operations.Transfer(**{
            "from": "foo",
            "to": "baar",
            "amount": Amount("111.110 HIVE", hive_instance=Hive(offline=True)),
            "memo": "Fooo"
        })

        t_s, t_v = steem_test.doit(ops=opHive)
        steem_times.append([t_s, t_v])

        t_s, t_v = bsteem_test.doit(ops=opBhive)
        bsteem_times.append([t_s, t_v])

    steem_dt = [0, 0]
    bsteem_dt = [0, 0]
    for i in range(0, loops):
        steem_dt[0] += steem_times[i][0]
        steem_dt[1] += steem_times[i][1]
        bsteem_dt[0] += bsteem_times[i][0]
        bsteem_dt[1] += bsteem_times[i][1]
    print("hive vs bhive:\n")
    print("hive: sign: %.2f s, verification %.2f s" % (steem_dt[0] / loops, steem_dt[1] / loops))
    print("bhive:  sign: %.2f s, verification %.2f s" % (bsteem_dt[0] / loops, bsteem_dt[1] / loops))
    print("------------------------------------")
    print("bhive is %.2f %% (sign) and %.2f %% (verify) faster than hive" %
          (steem_dt[0] / bsteem_dt[0] * 100, steem_dt[1] / bsteem_dt[1] * 100))
