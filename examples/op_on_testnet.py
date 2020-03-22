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

password = "secretPassword"
username = "bhive5"
useWallet = False
walletpassword = "123"

if __name__ == "__main__":
    testnet_node = "https://testnet.hive.vc"
    hv = Hive(node=testnet_node)
    prefix = hv.prefix
    # curl --data "username=username&password=secretPassword" https://testnet.hive.vc/create
    if useWallet:
        hv.wallet.wipe(True)
        hv.wallet.create(walletpassword)
        hv.wallet.unlock(walletpassword)
    active_key = PasswordKey(username, password, role="active", prefix=prefix)
    owner_key = PasswordKey(username, password, role="owner", prefix=prefix)
    posting_key = PasswordKey(username, password, role="posting", prefix=prefix)
    memo_key = PasswordKey(username, password, role="memo", prefix=prefix)
    active_pubkey = active_key.get_public_key()
    owner_pubkey = owner_key.get_public_key()
    posting_pubkey = posting_key.get_public_key()
    memo_pubkey = memo_key.get_public_key()
    active_privkey = active_key.get_private_key()
    posting_privkey = posting_key.get_private_key()
    owner_privkey = owner_key.get_private_key()
    memo_privkey = memo_key.get_private_key()
    if useWallet:
        hv.wallet.addPrivateKey(owner_privkey)
        hv.wallet.addPrivateKey(active_privkey)
        hv.wallet.addPrivateKey(memo_privkey)
        hv.wallet.addPrivateKey(posting_privkey)
    else:
        hv = Hive(node=testnet_node,
                    wif={'active': str(active_privkey),
                         'posting': str(posting_privkey),
                         'memo': str(memo_privkey)})
    account = Account(username, hive_instance=hv)
    if account["name"] == "bhive":
        account.disallow("bhive1", permission='posting')
        account.allow('bhive1', weight=1, permission='posting', account=None)
        account.follow("bhive1")
    elif account["name"] == "bhive5":
        account.allow('bhive4', weight=2, permission='active', account=None)
    if useWallet:
        hv.wallet.getAccountFromPrivateKey(str(active_privkey))

    # hv.create_account("bhive1", creator=account, password=password1)

    account1 = Account("bhive1", hive_instance=hv)
    b = Blockchain(hive_instance=hv)
    blocknum = b.get_current_block().identifier

    account.transfer("bhive1", 1, "SBD", "test")
    b1 = Block(blocknum, hive_instance=hv)
