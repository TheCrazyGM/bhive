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
from bhivebase import operations
from bhive.transactionbuilder import TransactionBuilder
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def test_post(wls):
    op1 = operations.Social_action(
        **{
            "account": "guest123",
            "social_action_comment_create": {
                "permlink": 'just-a-test-post',
                "parent_author": "",
                "parent_permlink": "test",
                "title": "just a test post",
                "body": "test post body",
                "json_metadata": '{"app":"wls_python"}'
            }
        })

    op2 = operations.Social_action(
        **{
            "account": "guest123",
            "social_action_comment_update": {
                "permlink": 'just-a-test-post',
                "title": "just a test post",
                "body": "test post body",
            }
        })

    op3 = operations.Vote(
                **{
                    'voter': 'guest123',
                    'author': 'wlsuser',
                    'permlink': 'another-test-post',
                    'weight': 10000,
                })

    privateWif = "5K..."
    tx = TransactionBuilder(use_condenser_api=True, steem_instance=wls)
    tx.appendOps(op1)
    tx.appendWif(privateWif)
    tx.sign()
    tx.broadcast()

if __name__ == "__main__":
    # `blocking=True` forces use of broadcast_transaction_synchronous
    wls = Hive(node=["https://pubrpc.whaleshares.io"], blocking=True)
    print(wls.get_blockchain_version())
    print(wls.get_config())
    test_post(wls)

