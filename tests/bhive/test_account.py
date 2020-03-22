from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import str
from builtins import super
import unittest
import mock
import pytz
from datetime import datetime, timedelta
from parameterized import parameterized
from pprint import pprint
from bhive import Hive, exceptions
from bhive.account import Account
from bhive.block import Block
from bhive.amount import Amount
from bhive.asset import Asset
from bhive.utils import formatTimeString
from bhive.nodelist import NodeList
from bhive.instance import set_shared_hive_instance

wif = "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3"


class Testcases(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        nodelist = NodeList()
        nodelist.update_nodes(hive_instance=Hive(node=nodelist.get_nodes(exclude_limited=False), num_retries=10))
        node_list = nodelist.get_nodes(exclude_limited=True)
      
        cls.bts = Hive(
            node=node_list,
            nobroadcast=True,
            bundle=False,
            unsigned=True,
            # Overwrite wallet to use this list of wifs only
            keys={"active": wif},
            num_retries=10
        )
        cls.account = Account("bhive.app", hive_instance=cls.bts)
        set_shared_hive_instance(cls.bts)

    def test_account(self):
        hv = self.bts
        account = self.account
        Account("bhive.app", hive_instance=hv)
        with self.assertRaises(
            exceptions.AccountDoesNotExistsException
        ):
            Account("DoesNotExistsXXX", hive_instance=hv)
        # asset = Asset("1.3.0")
        # symbol = asset["symbol"]
        self.assertEqual(account.name, "bhive.app")
        self.assertEqual(account["name"], account.name)
        self.assertIsInstance(account.get_balance("available", "SBD"), Amount)
        account.print_info()
        # self.assertIsInstance(account.balance({"symbol": symbol}), Amount)
        self.assertIsInstance(account.available_balances, list)
        self.assertTrue(account.virtual_op_count() > 0)

        # BlockchainObjects method
        account.cached = False
        self.assertTrue(list(account.items()))
        account.cached = False
        self.assertIn("id", account)
        account.cached = False
        # self.assertEqual(account["id"], "1.2.1")
        self.assertEqual(str(account), "<Account bhive.app>")
        self.assertIsInstance(Account(account), Account)

    def test_history(self):
        account = self.account
        zero_element = 0
        h_all_raw = []
        for h in account.history_reverse(raw_output=True):
            h_all_raw.append(h)
        # h_all_raw = h_all_raw[zero_element:]
        zero_element = h_all_raw[-1][0]
        h_list = []
        for h in account.history(stop=10, use_block_num=False, batch_size=10, raw_output=True):
            h_list.append(h)
        # self.assertEqual(h_list[0][0], zero_element)
        self.assertEqual(h_list[-1][0], 10)
        self.assertEqual(h_list[0][1]['block'], h_all_raw[-1][1]['block'])
        self.assertEqual(h_list[-1][1]['block'], h_all_raw[-11 + zero_element][1]['block'])
        h_list = []
        for h in account.history(start=1, stop=9, use_block_num=False, batch_size=10, raw_output=True):
            h_list.append(h)
        self.assertEqual(h_list[0][0], 1)
        self.assertEqual(h_list[-1][0], 9)
        self.assertEqual(h_list[0][1]['block'], h_all_raw[-2 + zero_element][1]['block'])
        self.assertEqual(h_list[-1][1]['block'], h_all_raw[-10 + zero_element][1]['block'])
        start = formatTimeString(h_list[0][1]["timestamp"])
        stop = formatTimeString(h_list[-1][1]["timestamp"])
        h_list = []
        for h in account.history(start=start, stop=stop, use_block_num=False, batch_size=10, raw_output=True):
            h_list.append(h)
        self.assertEqual(h_list[0][0], 1)
        self.assertEqual(h_list[-1][0], 9)
        self.assertEqual(h_list[0][1]['block'], h_all_raw[-2 + zero_element][1]['block'])
        self.assertEqual(h_list[-1][1]['block'], h_all_raw[-10 + zero_element][1]['block'])
        h_list = []
        for h in account.history_reverse(start=10, stop=0, use_block_num=False, batch_size=10, raw_output=False):
            h_list.append(h)
        # zero_element = h_list[-1]['index']
        self.assertEqual(h_list[0]['index'], 10)
        # self.assertEqual(h_list[-1]['index'], zero_element)
        self.assertEqual(h_list[0]['block'], h_all_raw[-11 + zero_element][1]['block'])
        self.assertEqual(h_list[-1]['block'], h_all_raw[-1][1]['block'])
        h_list = []
        for h in account.history_reverse(start=9, stop=1, use_block_num=False, batch_size=10, raw_output=True):
            h_list.append(h)
        self.assertEqual(h_list[0][0], 9)
        self.assertEqual(h_list[-1][0], 1)
        self.assertEqual(h_list[0][1]['block'], h_all_raw[-10 + zero_element][1]['block'])
        self.assertEqual(h_list[-1][1]['block'], h_all_raw[-2 + zero_element][1]['block'])
        start = formatTimeString(h_list[0][1]["timestamp"])
        stop = formatTimeString(h_list[-1][1]["timestamp"])
        h_list = []
        for h in account.history_reverse(start=start, stop=stop, use_block_num=False, batch_size=10, raw_output=True):
            h_list.append(h)
        self.assertEqual(h_list[0][0], 9)
        self.assertEqual(h_list[-1][0], 1)
        self.assertEqual(h_list[0][1]['block'], h_all_raw[-10 + zero_element][1]['block'])
        self.assertEqual(h_list[-1][1]['block'], h_all_raw[-2 + zero_element][1]['block'])
        h_list = []
        for h in account.get_account_history(10, 10, use_block_num=False, order=1, raw_output=True):
            h_list.append(h)
        # self.assertEqual(h_list[0][0], zero_element)
        self.assertEqual(h_list[-1][0], 10)
        self.assertEqual(h_list[0][1]['block'], h_all_raw[-1][1]['block'])
        self.assertEqual(h_list[-1][1]['block'], h_all_raw[-11 + zero_element][1]['block'])
        h_list = []
        for h in account.get_account_history(10, 10, use_block_num=False, start=1, stop=9, order=1, raw_output=True):
            h_list.append(h)
        self.assertEqual(h_list[0][0], 1)
        self.assertEqual(h_list[-1][0], 9)
        self.assertEqual(h_list[0][1]['block'], h_all_raw[-2 + zero_element][1]['block'])
        self.assertEqual(h_list[-1][1]['block'], h_all_raw[-10 + zero_element][1]['block'])
        start = formatTimeString(h_list[0][1]["timestamp"])
        stop = formatTimeString(h_list[-1][1]["timestamp"])
        h_list = []
        for h in account.get_account_history(10, 10, use_block_num=False, start=start, stop=stop, order=1, raw_output=True):
            h_list.append(h)
        self.assertEqual(h_list[0][0], 1)
        self.assertEqual(h_list[-1][0], 9)
        self.assertEqual(h_list[0][1]['block'], h_all_raw[-2 + zero_element][1]['block'])
        self.assertEqual(h_list[-1][1]['block'], h_all_raw[-10 + zero_element][1]['block'])
        h_list = []
        for h in account.get_account_history(10, 10, use_block_num=False, order=-1, raw_output=True):
            h_list.append(h)
        self.assertEqual(h_list[0][0], 10)
        # self.assertEqual(h_list[-1][0], zero_element)
        self.assertEqual(h_list[0][1]['block'], h_all_raw[-11 + zero_element][1]['block'])
        self.assertEqual(h_list[-1][1]['block'], h_all_raw[-1][1]['block'])
        h_list = []
        for h in account.get_account_history(10, 10, use_block_num=False, start=9, stop=1, order=-1, raw_output=True):
            h_list.append(h)
        self.assertEqual(h_list[0][0], 9)
        self.assertEqual(h_list[-1][0], 1)
        self.assertEqual(h_list[0][1]['block'], h_all_raw[-10 + zero_element][1]['block'])
        self.assertEqual(h_list[-1][1]['block'], h_all_raw[-2 + zero_element][1]['block'])
        start = formatTimeString(h_list[0][1]["timestamp"])
        stop = formatTimeString(h_list[-1][1]["timestamp"])
        h_list = []
        for h in account.get_account_history(10, 10, start=start, stop=stop, order=-1, raw_output=True):
            h_list.append(h)
        self.assertEqual(h_list[0][0], 9)
        self.assertEqual(h_list[-1][0], 1)
        self.assertEqual(h_list[0][1]['block'], h_all_raw[-10 + zero_element][1]['block'])
        self.assertEqual(h_list[-1][1]['block'], h_all_raw[-2 + zero_element][1]['block'])

    def test_history2(self):
        hv = self.bts
        account = Account("bhive.app", hive_instance=hv)
        h_list = []
        max_index = account.virtual_op_count()
        for h in account.history(start=max_index - 4, stop=max_index, use_block_num=False, batch_size=2, raw_output=False):
            h_list.append(h)
        self.assertEqual(len(h_list), 5)
        for i in range(1, 5):
            self.assertEqual(h_list[i]["index"] - h_list[i - 1]["index"], 1)

        h_list = []
        for h in account.history(start=max_index - 4, stop=max_index, use_block_num=False, batch_size=6, raw_output=False):
            h_list.append(h)
        self.assertEqual(len(h_list), 5)
        for i in range(1, 5):
            self.assertEqual(h_list[i]["index"] - h_list[i - 1]["index"], 1)

        h_list = []
        for h in account.history(start=max_index - 4, stop=max_index, use_block_num=False, batch_size=2, raw_output=True):
            h_list.append(h)
        self.assertEqual(len(h_list), 5)
        for i in range(1, 5):
            self.assertEqual(h_list[i][0] - h_list[i - 1][0], 1)

        h_list = []
        for h in account.history(start=max_index - 4, stop=max_index, use_block_num=False, batch_size=6, raw_output=True):
            h_list.append(h)
        self.assertEqual(len(h_list), 5)
        for i in range(1, 5):
            self.assertEqual(h_list[i][0] - h_list[i - 1][0], 1)

    def test_history_reverse2(self):
        hv = self.bts
        account = Account("bhive.app", hive_instance=hv)
        h_list = []
        max_index = account.virtual_op_count()
        for h in account.history_reverse(start=max_index, stop=max_index - 4, use_block_num=False, batch_size=2, raw_output=False):
            h_list.append(h)
        self.assertEqual(len(h_list), 5)
        for i in range(1, 5):
            self.assertEqual(h_list[i]["index"] - h_list[i - 1]["index"], -1)

        h_list = []
        for h in account.history_reverse(start=max_index, stop=max_index - 4, use_block_num=False, batch_size=6, raw_output=False):
            h_list.append(h)
        self.assertEqual(len(h_list), 5)
        for i in range(1, 5):
            self.assertEqual(h_list[i]["index"] - h_list[i - 1]["index"], -1)

        h_list = []
        for h in account.history_reverse(start=max_index, stop=max_index - 4, use_block_num=False, batch_size=6, raw_output=True):
            h_list.append(h)
        self.assertEqual(len(h_list), 5)
        for i in range(1, 5):
            self.assertEqual(h_list[i][0] - h_list[i - 1][0], -1)

        h_list = []
        for h in account.history_reverse(start=max_index, stop=max_index - 4, use_block_num=False, batch_size=2, raw_output=True):
            h_list.append(h)
        self.assertEqual(len(h_list), 5)
        for i in range(1, 5):
            self.assertEqual(h_list[i][0] - h_list[i - 1][0], -1)

    def test_history_block_num(self):
        hv = self.bts
        zero_element = 0
        account = Account("fullnodeupdate", hive_instance=hv)
        h_all_raw = []
        for h in account.history_reverse(raw_output=True):
            h_all_raw.append(h)
        h_list = []
        for h in account.history(start=h_all_raw[-1][1]["block"], stop=h_all_raw[-11 + zero_element][1]["block"], use_block_num=True, batch_size=10, raw_output=True):
            h_list.append(h)
        self.assertEqual(h_list[0][0], zero_element)
        self.assertEqual(h_list[-1][0], 10)
        self.assertEqual(h_list[0][1]['block'], h_all_raw[-1][1]['block'])
        self.assertEqual(h_list[-1][1]['block'], h_all_raw[-11 + zero_element][1]['block'])
        h_list = []
        for h in account.history_reverse(start=h_all_raw[-11 + zero_element][1]["block"], stop=h_all_raw[-1][1]["block"], use_block_num=True, batch_size=10, raw_output=True):
            h_list.append(h)
        self.assertEqual(h_list[0][0], 10)
        self.assertEqual(h_list[-1][0], zero_element)
        self.assertEqual(h_list[0][1]['block'], h_all_raw[-11 + zero_element][1]['block'])
        self.assertEqual(h_list[-1][1]['block'], h_all_raw[-1][1]['block'])
        h_list = []
        for h in account.get_account_history(10, 10, use_block_num=True, start=h_all_raw[-2 + zero_element][1]["block"], stop=h_all_raw[-10 + zero_element][1]["block"], order=1, raw_output=True):
            h_list.append(h)
        self.assertEqual(h_list[0][0], 1)
        self.assertEqual(h_list[-1][0], 9)
        self.assertEqual(h_list[0][1]['block'], h_all_raw[-2 + zero_element][1]['block'])
        self.assertEqual(h_list[-1][1]['block'], h_all_raw[-10 + zero_element][1]['block'])
        h_list = []
        for h in account.get_account_history(10, 10, use_block_num=True, start=h_all_raw[-10 + zero_element][1]["block"], stop=h_all_raw[-2 + zero_element][1]["block"], order=-1, raw_output=True):
            h_list.append(h)
        self.assertEqual(h_list[0][0], 9)
        self.assertEqual(h_list[-1][0], 1)
        self.assertEqual(h_list[0][1]['block'], h_all_raw[-10 + zero_element][1]['block'])
        self.assertEqual(h_list[-1][1]['block'], h_all_raw[-2 + zero_element][1]['block'])

    def test_account_props(self):
        account = self.account
        rep = account.get_reputation()
        self.assertTrue(isinstance(rep, float))
        vp = account.get_voting_power()
        self.assertTrue(vp >= 0)
        self.assertTrue(vp <= 100)
        sp = account.get_steem_power()
        self.assertTrue(hp >= 0)
        vv = account.get_voting_value_HBD()
        self.assertTrue(vv >= 0)
        bw = account.get_bandwidth()
        # self.assertTrue(bw['used'] <= bw['allocated'])
        followers = account.get_followers()
        self.assertTrue(isinstance(followers, list))
        following = account.get_following()
        self.assertTrue(isinstance(following, list))
        count = account.get_follow_count()
        self.assertEqual(count['follower_count'], len(followers))
        self.assertEqual(count['following_count'], len(following))

    def test_MissingKeyError(self):
        w = self.account
        w.hive.txbuffer.clear()
        tx = w.convert("1 HBD")
        with self.assertRaises(
            exceptions.MissingKeyError
        ):
            tx.sign()

    def test_withdraw_vesting(self):
        w = self.account
        w.hive.txbuffer.clear()
        tx = w.withdraw_vesting("100 VESTS")
        self.assertEqual(
            (tx["operations"][0][0]),
            "withdraw_vesting"
        )
        op = tx["operations"][0][1]
        self.assertIn(
            "bhive.app",
            op["account"])

    def test_delegate_vesting_shares(self):
        w = self.account
        w.hive.txbuffer.clear()
        tx = w.delegate_vesting_shares("test1", "100 VESTS")
        self.assertEqual(
            (tx["operations"][0][0]),
            "delegate_vesting_shares"
        )
        op = tx["operations"][0][1]
        self.assertIn(
            "bhive.app",
            op["delegator"])

    def test_claim_reward_balance(self):
        w = self.account
        w.hive.txbuffer.clear()
        tx = w.claim_reward_balance()
        self.assertEqual(
            (tx["operations"][0][0]),
            "claim_reward_balance"
        )
        op = tx["operations"][0][1]
        self.assertIn(
            "bhive.app",
            op["account"])

    def test_cancel_transfer_from_savings(self):
        w = self.account
        w.hive.txbuffer.clear()
        tx = w.cancel_transfer_from_savings(0)
        self.assertEqual(
            (tx["operations"][0][0]),
            "cancel_transfer_from_savings"
        )
        op = tx["operations"][0][1]
        self.assertIn(
            "bhive.app",
            op["from"])

    def test_transfer_from_savings(self):
        w = self.account
        w.hive.txbuffer.clear()
        tx = w.transfer_from_savings(1, "STEEM", "")
        self.assertEqual(
            (tx["operations"][0][0]),
            "transfer_from_savings"
        )
        op = tx["operations"][0][1]
        self.assertIn(
            "bhive.app",
            op["from"])

    def test_transfer_to_savings(self):
        w = self.account
        w.hive.txbuffer.clear()
        tx = w.transfer_to_savings(1, "STEEM", "")
        self.assertEqual(
            (tx["operations"][0][0]),
            "transfer_to_savings"
        )
        op = tx["operations"][0][1]
        self.assertIn(
            "bhive.app",
            op["from"])

    def test_convert(self):
        w = self.account
        w.hive.txbuffer.clear()
        tx = w.convert("1 HBD")
        self.assertEqual(
            (tx["operations"][0][0]),
            "convert"
        )
        op = tx["operations"][0][1]
        self.assertIn(
            "bhive.app",
            op["owner"])

    def test_transfer_to_vesting(self):
        w = self.account
        w.hive.txbuffer.clear()
        tx = w.transfer_to_vesting("1 HIVE")
        self.assertEqual(
            (tx["operations"][0][0]),
            "transfer_to_vesting"
        )
        op = tx["operations"][0][1]
        self.assertIn(
            "bhive.app",
            op["from"])

    def test_json_export(self):
        account = Account("bhive.app", hive_instance=self.bts)
        if account.hive.rpc.get_use_appbase():
            content = self.bts.rpc.find_accounts({'accounts': [account["name"]]}, api="database")["accounts"][0]
        else:
            content = self.bts.rpc.get_accounts([account["name"]])[0]
        keys = list(content.keys())
        json_content = account.json()
        exclude_list = ['owner_challenged', 'average_bandwidth']  # ['json_metadata', 'reputation', 'active_votes', 'savings_sbd_seconds']
        for k in keys:
            if k not in exclude_list:
                if isinstance(content[k], dict) and isinstance(json_content[k], list):
                    content_list = [content[k]["amount"], content[k]["precision"], content[k]["nai"]]
                    self.assertEqual(content_list, json_content[k])
                else:
                    self.assertEqual(content[k], json_content[k])

    def test_estimate_virtual_op_num(self):
        hv = self.bts
        account = Account("gtg", hive_instance=hv)
        block_num = 21248120
        block = Block(block_num, hive_instance=hv)
        op_num1 = account.estimate_virtual_op_num(block.time(), stop_diff=1, max_count=100)
        op_num2 = account.estimate_virtual_op_num(block_num, stop_diff=1, max_count=100)
        op_num3 = account.estimate_virtual_op_num(block_num, stop_diff=100, max_count=100)
        op_num4 = account.estimate_virtual_op_num(block_num, stop_diff=0.00001, max_count=100)
        self.assertTrue(abs(op_num1 - op_num2) < 2)
        self.assertTrue(abs(op_num1 - op_num4) < 2)
        self.assertTrue(abs(op_num1 - op_num3) < 200)
        block_diff1 = 0
        block_diff2 = 0
        for h in account.get_account_history(op_num4 - 1, 0):
            block_diff1 = (block_num - h["block"])
        for h in account.get_account_history(op_num4 + 1, 0):
            block_diff2 = (block_num - h["block"])
        self.assertTrue(block_diff1 > 0)
        self.assertTrue(block_diff2 <= 0)

    def test_estimate_virtual_op_num2(self):
        account = self.account
        h_all_raw = []
        for h in account.history(raw_output=False):
            h_all_raw.append(h)
        last_block = h_all_raw[0]["block"]
        i = 1
        for op in h_all_raw[1:5]:
            new_block = op["block"]
            block_num = last_block + int((new_block - last_block) / 2)
            op_num = account.estimate_virtual_op_num(block_num, stop_diff=0.1, max_count=100)
            if op_num > 0:
                op_num -= 1
            self.assertTrue(op_num <= i)
            i += 1
            last_block = new_block

    def test_history_votes(self):
        hv = self.bts
        account = Account("gtg", hive_instance=hv)
        utc = pytz.timezone('UTC')
        limit_time = utc.localize(datetime.utcnow()) - timedelta(days=2)
        votes_list = []
        for v in account.history(start=limit_time, only_ops=["vote"]):
            votes_list.append(v)
        start_num = votes_list[0]["block"]
        votes_list2 = []
        for v in account.history(start=start_num, only_ops=["vote"]):
            votes_list2.append(v)
        self.assertTrue(abs(len(votes_list) - len(votes_list2)) < 2)

    def test_comment_history(self):
        account = self.account
        comments = []
        for c in account.comment_history(limit=1):
            comments.append(c)
        self.assertEqual(len(comments), 1)
        self.assertEqual(comments[0]["author"], account["name"])
        self.assertTrue(comments[0].is_comment())
        self.assertTrue(comments[0].depth > 0)

    def test_blog_history(self):
        account = Account("bhive.app", hive_instance=self.bts)
        posts = []
        for p in account.blog_history(limit=5):
            if p["author"] != account["name"]:
                continue
            posts.append(p)
        self.assertTrue(len(posts) >= 1)
        self.assertEqual(posts[0]["author"], account["name"])
        self.assertTrue(posts[0].is_main_post())
        self.assertTrue(posts[0].depth == 0)

    def test_reply_history(self):
        account = self.account
        replies = []
        for r in account.reply_history(limit=1):
            replies.append(r)
        self.assertEqual(len(replies), 1)
        self.assertTrue(replies[0].is_comment())
        self.assertTrue(replies[0].depth > 0)

    def test_get_vote_pct_for_HBD(self):
        account = self.account
        for vote_pwr in range(5, 100, 5):
            self.assertTrue(9900 <= account.get_vote_pct_for_HBD(account.get_voting_value_HBD(voting_power=vote_pwr), voting_power=vote_pwr) <= 11000)
