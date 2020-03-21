from __future__ import absolute_import
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
from bhivegraphenebase.account import PasswordKey, PrivateKey, PublicKey
from bhive.hive import Hive
from bhive.utils import parse_time, formatTimedelta
from bhiveapi.exceptions import NumRetriesReached
from bhive.nodelist import NodeList
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


if __name__ == "__main__":
    # hv = Hive(node="https://testnet.timcliff.com/")
    # hv = Hive(node="https://testnet.hiveitdev.com")
    hv = Hive(node="https://api.hive.blog")
    hv.wallet.unlock(pwd="pwd123")

    account = Account("bhivebot", hive_instance=hv)
    print(account.get_voting_power())

    account.transfer("thecrazygm", 0.001, "HBD", "test")
