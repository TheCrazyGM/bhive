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
    hv = Hive(node=["https://testnet.hiveitdev.com"],
                custom_chains={"TESTNETHF20":
                               {'chain_assets':
                                [
                                    {"asset": "@@000000013", "symbol": "SBD", "precision": 3, "id": 0},
                                    {"asset": "@@000000021", "symbol": "STEEM", "precision": 3, "id": 1},
                                    {"asset": "@@000000037", "symbol": "VESTS", "precision": 6, "id": 2}
                                ],
                                'chain_id': '46d82ab7d8db682eb1959aed0ada039a6d49afa1602491f93dde9cac3e8e6c32',
                                'min_version': '0.20.0',
                                'prefix': 'TST'}})
    print(hv.get_blockchain_version())
    print(hv.get_config()["HIVE_CHAIN_ID"])
