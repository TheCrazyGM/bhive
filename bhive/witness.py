# This Python file uses the following encoding: utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import str
import json
from bhive.instance import shared_hive_instance
from bhivegraphenebase.py23 import bytes_types, integer_types, string_types, text_type
from .account import Account
from .amount import Amount
from .exceptions import WitnessDoesNotExistsException
from .blockchainobject import BlockchainObject
from .utils import formatTimeString
from datetime import datetime, timedelta, date
from bhivebase import transactions, operations
from bhivegraphenebase.account import PrivateKey, PublicKey
import pytz
from prettytable import PrettyTable


class Witness(BlockchainObject):
    """ Read data about a witness in the chain

        :param str account_name: Name of the witness
        :param Hive hive_instance: Hive instance to use when
               accesing a RPC

        .. code-block:: python

           >>> from bhive.witness import Witness
           >>> Witness("gtg")
           <Witness gtg>

    """
    type_id = 3

    def __init__(
        self,
        owner,
        full=False,
        lazy=False,
        hive_instance=None
    ):
        self.full = full
        self.lazy = lazy
        self.hive = hive_instance or shared_hive_instance()
        if isinstance(owner, dict):
            owner = self._parse_json_data(owner)
        super(Witness, self).__init__(
            owner,
            lazy=lazy,
            full=full,
            id_item="owner",
            hive_instance=hive_instance
        )

    def refresh(self):
        if not self.identifier:
            return
        if not self.hive.is_connected():
            return
        self.hive.rpc.set_next_node_on_empty_reply(False)
        if self.hive.rpc.get_use_appbase():
            witness = self.hive.rpc.find_witnesses({'owners': [self.identifier]}, api="database")['witnesses']
            if len(witness) > 0:
                witness = witness[0]
        else:
            witness = self.hive.rpc.get_witness_by_account(self.identifier)
        if not witness:
            raise WitnessDoesNotExistsException(self.identifier)
        witness = self._parse_json_data(witness)
        super(Witness, self).__init__(witness, id_item="owner", lazy=self.lazy, full=self.full, hive_instance=self.hive)

    def _parse_json_data(self, witness):
        parse_times = [
            "created", "last_sbd_exchange_update", "hardfork_time_vote",
        ]
        for p in parse_times:
            if p in witness and isinstance(witness.get(p), string_types):
                witness[p] = formatTimeString(witness.get(p, "1970-01-01T00:00:00"))
        parse_int = [
            "votes", "virtual_last_update", "virtual_position", "virtual_scheduled_time",
        ]
        for p in parse_int:
            if p in witness and isinstance(witness.get(p), string_types):
                witness[p] = int(witness.get(p, "0"))
        return witness

    def json(self):
        output = self.copy()
        parse_times = [
            "created", "last_sbd_exchange_update", "hardfork_time_vote",
        ]
        for p in parse_times:
            if p in output:
                p_date = output.get(p, datetime(1970, 1, 1, 0, 0))
                if isinstance(p_date, (datetime, date)):
                    output[p] = formatTimeString(p_date)
                else:
                    output[p] = p_date
        parse_int = [
            "votes", "virtual_last_update", "virtual_position", "virtual_scheduled_time",
        ]
        for p in parse_int:
            if p in output and isinstance(output[p], integer_types):
                output[p] = str(output[p])
        return json.loads(str(json.dumps(output)))

    @property
    def account(self):
        return Account(self["owner"], hive_instance=self.hive)

    @property
    def is_active(self):
        return len(self['signing_key']) > 3 and self['signing_key'][3:] != '1111111111111111111111111111111114T1Anm'

    def feed_publish(self,
                     base,
                     quote=None,
                     account=None):
        """ Publish a feed price as a witness.

            :param float base: USD Price of HIVE in HBD (implied price)
            :param float quote: (optional) Quote Price. Should be 1.000 (default), unless
                we are adjusting the feed to support the peg.
            :param str account: (optional) the source account for the transfer
                if not self["owner"]
        """
        quote = quote if quote is not None else "1.000 %s" % (self.hive.steem_symbol)
        if not account:
            account = self["owner"]
        if not account:
            raise ValueError("You need to provide an account")

        account = Account(account, hive_instance=self.hive)
        if isinstance(base, Amount):
            base = Amount(base, hive_instance=self.hive)
        elif isinstance(base, string_types):
            base = Amount(base, hive_instance=self.hive)
        else:
            base = Amount(base, self.hive.sbd_symbol, hive_instance=self.hive)

        if isinstance(quote, Amount):
            quote = Amount(quote, hive_instance=self.hive)
        elif isinstance(quote, string_types):
            quote = Amount(quote, hive_instance=self.hive)
        else:
            quote = Amount(quote, self.hive.steem_symbol, hive_instance=self.hive)

        if not base.symbol == self.hive.sbd_symbol:
            raise AssertionError()
        if not quote.symbol == self.hive.steem_symbol:
            raise AssertionError()

        op = operations.Feed_publish(
            **{
                "publisher": account["name"],
                "exchange_rate": {
                    "base": base,
                    "quote": quote,
                },
                "prefix": self.hive.prefix,
            })
        return self.hive.finalizeOp(op, account, "active")

    def update(self, signing_key, url, props, account=None):
        """ Update witness

            :param str signing_key: Signing key
            :param str url: URL
            :param dict props: Properties
            :param str account: (optional) witness account name

            Properties:::

                {
                    "account_creation_fee": x,
                    "maximum_block_size": x,
                    "sbd_interest_rate": x,
                }

        """
        if not account:
            account = self["owner"]
        return self.hive.witness_update(signing_key, url, props, account=account)


class WitnessesObject(list):
    def printAsTable(self, sort_key="votes", reverse=True, return_str=False, **kwargs):
        utc = pytz.timezone('UTC')
        no_feed = False
        if len(self) > 0 and "sbd_exchange_rate" not in self[0]:
            table_header = ["Name", "Votes [PV]", "Disabled", "Missed", "Fee", "Size", "Version"]
            no_feed = True
        else:
            table_header = ["Name", "Votes [PV]", "Disabled", "Missed", "Feed base", "Feed quote", "Feed update", "Fee", "Size", "Interest", "Version"]
        t = PrettyTable(table_header)
        t.align = "l"
        if sort_key == 'base':
            sortedList = sorted(self, key=lambda self: self['sbd_exchange_rate']['base'], reverse=reverse)
        elif sort_key == 'quote':
            sortedList = sorted(self, key=lambda self: self['sbd_exchange_rate']['quote'], reverse=reverse)
        elif sort_key == 'last_sbd_exchange_update':
            sortedList = sorted(self, key=lambda self: (utc.localize(datetime.utcnow()) - self['last_sbd_exchange_update']).total_seconds(), reverse=reverse)
        elif sort_key == 'account_creation_fee':
            sortedList = sorted(self, key=lambda self: self['props']['account_creation_fee'], reverse=reverse)
        elif sort_key == 'sbd_interest_rate':
            sortedList = sorted(self, key=lambda self: self['props']['sbd_interest_rate'], reverse=reverse)
        elif sort_key == 'maximum_block_size':
            sortedList = sorted(self, key=lambda self: self['props']['maximum_block_size'], reverse=reverse)
        elif sort_key == 'votes':
            sortedList = sorted(self, key=lambda self: int(self[sort_key]), reverse=reverse)
        else:
            sortedList = sorted(self, key=lambda self: self[sort_key], reverse=reverse)
        for witness in sortedList:
            disabled = ""
            if not witness.is_active:
                disabled = "yes"

            if no_feed:
                t.add_row([witness['owner'],
                           str(round(int(witness['votes']) / 1e15, 2)),
                           disabled,
                           str(witness['total_missed']),
                           str(witness['props']['account_creation_fee']),
                           str(witness['props']['maximum_block_size']),
                           witness['running_version']])
            else:
                td = utc.localize(datetime.utcnow()) - witness['last_sbd_exchange_update']
                t.add_row([witness['owner'],
                           str(round(int(witness['votes']) / 1e15, 2)),
                           disabled,
                           str(witness['total_missed']),
                           str(Amount(witness['sbd_exchange_rate']['base'], hive_instance=self.hive)),
                           str(Amount(witness['sbd_exchange_rate']['quote'], hive_instance=self.hive)),
                           str(td.days) + " days " + str(td.seconds // 3600) + ":" + str((td.seconds // 60) % 60),
                           str(witness['props']['account_creation_fee']),
                           str(witness['props']['maximum_block_size']),
                           str(witness['props']['sbd_interest_rate'] / 100) + " %",
                           witness['running_version']])
        if return_str:
            return t.get_string(**kwargs)
        else:
            print(t.get_string(**kwargs))

    def get_votes_sum(self):
        vote_sum = 0
        for witness in self:
            vote_sum += int(witness['votes'])
        return vote_sum

    def __contains__(self, item):
        from .account import Account
        if isinstance(item, Account):
            name = item["name"]
        elif self.hive:
            account = Account(item, hive_instance=self.hive)
            name = account["name"]

        return (
            any([name == x["owner"] for x in self])
        )

    def __str__(self):
        return self.printAsTable(return_str=True)

    def __repr__(self):
        return "<%s %s>" % (
            self.__class__.__name__, str(self.identifier))


class GetWitnesses(WitnessesObject):
    """ Obtain a list of witnesses

        :param list name_list: list of witneses to fetch
        :param int batch_limit: (optional) maximum number of witnesses
            to fetch per call, defaults to 100
        :param Hive hive_instance: Hive() instance to use when
            accessing a RPCcreator = Witness(creator, hive_instance=self)

        .. code-block:: python

            from bhive.witness import GetWitnesses
            w = GetWitnesses(["gtg", "jesta"])
            print(w[0].json())
            print(w[1].json())

    """
    def __init__(self, name_list, batch_limit=100, lazy=False, full=True, hive_instance=None):
        self.hive = hive_instance or shared_hive_instance()
        if not self.hive.is_connected():
            return
        witnesses = []
        name_cnt = 0
        if self.hive.rpc.get_use_appbase():
            while name_cnt < len(name_list):
                self.hive.rpc.set_next_node_on_empty_reply(False)
                witnesses += self.hive.rpc.find_witnesses({'owners': name_list[name_cnt:batch_limit + name_cnt]}, api="database")["witnesses"]
                name_cnt += batch_limit
        else:
            for witness in name_list:
                witnesses.append(self.hive.rpc.get_witness_by_account(witness))
        self.identifier = ""
        super(GetWitnesses, self).__init__(
            [
                Witness(x, lazy=lazy, full=full, hive_instance=self.hive)
                for x in witnesses
            ]
        )


class Witnesses(WitnessesObject):
    """ Obtain a list of **active** witnesses and the current schedule

        :param Hive hive_instance: Hive instance to use when
            accesing a RPC

        .. code-block:: python

           >>> from bhive.witness import Witnesses
           >>> Witnesses()
           <Witnesses >

    """
    def __init__(self, lazy=False, full=True, hive_instance=None):
        self.hive = hive_instance or shared_hive_instance()
        self.lazy = lazy
        self.full = full
        self.refresh()

    def refresh(self):
        self.hive.rpc.set_next_node_on_empty_reply(False)
        if self.hive.rpc.get_use_appbase():
            self.active_witnessess = self.hive.rpc.get_active_witnesses(api="database")['witnesses']
            self.schedule = self.hive.rpc.get_witness_schedule(api="database")
            self.witness_count = self.hive.rpc.get_witness_count(api="condenser")
        else:
            self.active_witnessess = self.hive.rpc.get_active_witnesses()
            self.schedule = self.hive.rpc.get_witness_schedule()
            self.witness_count = self.hive.rpc.get_witness_count()
        self.current_witness = self.hive.get_dynamic_global_properties(use_stored_data=False)["current_witness"]
        self.identifier = ""
        super(Witnesses, self).__init__(
            [
                Witness(x, lazy=self.lazy, full=self.full, hive_instance=self.hive)
                for x in self.active_witnessess
            ]
        )


class WitnessesVotedByAccount(WitnessesObject):
    """ Obtain a list of witnesses which have been voted by an account

        :param str account: Account name
        :param Hive hive_instance: Hive instance to use when
            accesing a RPC

        .. code-block:: python

           >>> from bhive.witness import WitnessesVotedByAccount
           >>> WitnessesVotedByAccount("gtg")
           <WitnessesVotedByAccount gtg>

    """
    def __init__(self, account, lazy=False, full=True, hive_instance=None):
        self.hive = hive_instance or shared_hive_instance()
        self.account = Account(account, full=True, hive_instance=self.hive)
        account_name = self.account["name"]
        self.identifier = account_name
        self.hive.rpc.set_next_node_on_empty_reply(False)
        if self.hive.rpc.get_use_appbase():
            if "witnesses_voted_for" not in self.account:
                return
            limit = self.account["witnesses_voted_for"]
            witnessess_dict = self.hive.rpc.list_witness_votes({'start': [account_name], 'limit': limit, 'order': 'by_account_witness'}, api="database")['votes']
            witnessess = []
            for w in witnessess_dict:
                witnessess.append(w["witness"])
        else:
            if "witness_votes" not in self.account:
                return
            witnessess = self.account["witness_votes"]

        super(WitnessesVotedByAccount, self).__init__(
            [
                Witness(x, lazy=lazy, full=full, hive_instance=self.hive)
                for x in witnessess
            ]
        )


class WitnessesRankedByVote(WitnessesObject):
    """ Obtain a list of witnesses ranked by Vote

        :param str from_account: Witness name from which the lists starts (default = "")
        :param int limit: Limits the number of shown witnesses (default = 100)
        :param Hive hive_instance: Hive instance to use when
            accesing a RPC

        .. code-block:: python

           >>> from bhive.witness import WitnessesRankedByVote
           >>> WitnessesRankedByVote(limit=100)
           <WitnessesRankedByVote >

    """
    def __init__(self, from_account="", limit=100, lazy=False, full=False, hive_instance=None):
        self.hive = hive_instance or shared_hive_instance()
        witnessList = []
        last_limit = limit
        self.identifier = ""
        use_condenser = True
        self.hive.rpc.set_next_node_on_empty_reply(False)
        if self.hive.rpc.get_use_appbase() and not use_condenser:
            query_limit = 1000
        else:
            query_limit = 100
        if self.hive.rpc.get_use_appbase() and not use_condenser and from_account == "":
            last_account = None
        elif self.hive.rpc.get_use_appbase() and not use_condenser:
            last_account = Witness(from_account, hive_instance=self.hive)["votes"]
        else:
            last_account = from_account
        if limit > query_limit:
            while last_limit > query_limit:
                tmpList = WitnessesRankedByVote(last_account, query_limit)
                if (last_limit < limit):
                    witnessList.extend(tmpList[1:])
                    last_limit -= query_limit - 1
                else:
                    witnessList.extend(tmpList)
                    last_limit -= query_limit
                if self.hive.rpc.get_use_appbase():
                    last_account = witnessList[-1]["votes"]
                else:
                    last_account = witnessList[-1]["owner"]
        if (last_limit < limit):
            last_limit += 1
        if self.hive.rpc.get_use_appbase() and not use_condenser:
            witnessess = self.hive.rpc.list_witnesses({'start': [last_account], 'limit': last_limit, 'order': 'by_vote_name'}, api="database")['witnesses']
        elif self.hive.rpc.get_use_appbase() and use_condenser:
            witnessess = self.hive.rpc.get_witnesses_by_vote(last_account, last_limit, api="condenser")
        else:
            witnessess = self.hive.rpc.get_witnesses_by_vote(last_account, last_limit)
        # self.witness_count = len(self.voted_witnessess)
        if (last_limit < limit):
            witnessess = witnessess[1:]
        if len(witnessess) > 0:
            for x in witnessess:
                witnessList.append(Witness(x, lazy=lazy, full=full, hive_instance=self.hive))
        if len(witnessList) == 0:
            return
        super(WitnessesRankedByVote, self).__init__(witnessList)


class ListWitnesses(WitnessesObject):
    """ List witnesses ranked by name

        :param str from_account: Witness name from which the lists starts (default = "")
        :param int limit: Limits the number of shown witnesses (default = 100)
        :param Hive hive_instance: Hive instance to use when
            accesing a RPC

        .. code-block:: python

           >>> from bhive.witness import ListWitnesses
           >>> ListWitnesses(from_account="gtg", limit=100)
           <ListWitnesses gtg>

    """
    def __init__(self, from_account="", limit=100, lazy=False, full=False, hive_instance=None):
        self.hive = hive_instance or shared_hive_instance()
        self.identifier = from_account
        self.hive.rpc.set_next_node_on_empty_reply(False)
        if self.hive.rpc.get_use_appbase():
            witnessess = self.hive.rpc.list_witnesses({'start': from_account, 'limit': limit, 'order': 'by_name'}, api="database")['witnesses']
        else:
            witnessess = self.hive.rpc.lookup_witness_accounts(from_account, limit)
        if len(witnessess) == 0:
            return
        super(ListWitnesses, self).__init__(
            [
                Witness(x, lazy=lazy, full=full, hive_instance=self.hive)
                for x in witnessess
            ]
        )
