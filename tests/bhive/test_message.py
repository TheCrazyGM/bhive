from builtins import super
import unittest
import mock
from bhive import Hive
from bhive.message import Message
from bhive.account import Account
from bhive.instance import set_shared_steem_instance
from bhive.nodelist import NodeList

wif = "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3"
core_unit = "STM"


class Testcases(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        nodelist = NodeList()
        nodelist.update_nodes(steem_instance=Hive(node=nodelist.get_nodes(exclude_limited=False), num_retries=10))
        cls.bts = Hive(
            node=nodelist.get_nodes(exclude_limited=True),
            nobroadcast=True,
            keys=[wif],
            num_retries=10
        )
        set_shared_steem_instance(cls.bts)

    def test_sign_message(self):
        def new_refresh(self):
            dict.__init__(
                self, {
                "identifier": "test",
                "name": "test",
                "id_item": "name",
                "memo_key": "STM6MRyAjQq8ud7hVNYcfnVPJqcVpscN5So8BhtHuGYqET5GDW5CV"
                })

        with mock.patch(
            "bhive.account.Account.refresh",
            new=new_refresh
        ):
            account = Account("test")
            account["memo_key"] = "STM6MRyAjQq8ud7hVNYcfnVPJqcVpscN5So8BhtHuGYqET5GDW5CV"
            p = Message("message foobar").sign(account=account)
            Message(p).verify(account=account)

    def test_verify_message(self):
        def new_refresh(self):
            dict.__init__(
                self, {
                "identifier": "test",
                "name": "test",
                "id_item": "name",
                "memo_key": "STM6MRyAjQq8ud7hVNYcfnVPJqcVpscN5So8BhtHuGYqET5GDW5CV"
                })

        with mock.patch(
            "bhive.account.Account.refresh",
            new=new_refresh
        ):
            Message(
                "-----BEGIN HIVE SIGNED MESSAGE-----\n"
                "message foobar\n"
                "-----BEGIN META-----\n"
                "account=test\n"
                "memokey=STM6MRyAjQq8ud7hVNYcfnVPJqcVpscN5So8BhtHuGYqET5GDW5CV\n"
                "block=19902522\n"
                "timestamp=2018-02-15T22:00:54\n"
                "-----BEGIN SIGNATURE-----\n"
                "20093ef63f375b9aa8570188cae3aad953bf6393d43ce6f03bbbd1b429e48c6a587dc012922515f6d327158df5081ea2d595888225f9f1c6c3028781c8f9451fde\n"
                "-----END HIVE SIGNED MESSAGE-----\n"
            ).verify()

            Message(
                "-----BEGIN HIVE SIGNED MESSAGE-----"
                "message foobar\n"
                "-----BEGIN META-----"
                "account=test\n"
                "memokey=STM6MRyAjQq8ud7hVNYcfnVPJqcVpscN5So8BhtHuGYqET5GDW5CV\n"
                "block=19902522\n"
                "timestamp=2018-02-15T22:00:54\n"
                "-----BEGIN SIGNATURE-----"
                "20093ef63f375b9aa8570188cae3aad953bf6393d43ce6f03bbbd1b429e48c6a587dc012922515f6d327158df5081ea2d595888225f9f1c6c3028781c8f9451fde\n"
                "-----END HIVE SIGNED MESSAGE-----"
            ).verify()
