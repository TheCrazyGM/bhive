from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import sys
from datetime import datetime, timedelta
import time
import io
import logging

from bhive.blockchain import Blockchain
from bhive.block import Block
from bhive.account import Account
from bhive.amount import Amount
from bhive.witness import Witness
from bhivebase import operations
from bhive.transactionbuilder import TransactionBuilder
from bhivegraphenebase.account import PasswordKey, PrivateKey, PublicKey
from bhive.hive import Hive
from bhive.utils import parse_time, formatTimedelta
from bhiveapi.exceptions import NumRetriesReached
from bhive.nodelist import NodeList
from bhivebase.transactions import getBlockParams
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# example wif
wif = "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3"


if __name__ == "__main__":
    hv_online = Hive()
    ref_block_num, ref_block_prefix = getBlockParams(hv_online)
    print("ref_block_num %d - ref_block_prefix %d" % (ref_block_num, ref_block_prefix))

    hv = Hive(offline=True)

    op = operations.Transfer({'from': 'beembot',
                              'to': 'thecrazygm',
                              'amount': "0.001 HBD",
                              'memo': ""})
    tb = TransactionBuilder(hive_instance=hv)

    tb.appendOps([op])
    tb.appendWif(wif)
    tb.constructTx(ref_block_num=ref_block_num, ref_block_prefix=ref_block_prefix)
    tx = tb.sign(reconstruct_tx=False)
    print(tx.json())
