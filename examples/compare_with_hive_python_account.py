from __future__ import print_function
import sys
from datetime import timedelta
import time
import io
from bhive import Hive
from bhive.account import Account
from bhive.amount import Amount
from bhive.utils import parse_time
from hive.account import Account as hiveAccount
from hive.post import Post as hivePost
from hive import Hive as hiveHive
import logging
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


if __name__ == "__main__":
    hv = Hive("https://api.hive.blog")
    bsteem_acc = Account("thecrazygm", hive_instance=hv)
    hv2 = hiveHive(nodes=["https://api.hive.blog"])
    steem_acc = hiveAccount("thecrazygm", hived_instance=hv2)

    # profile
    print("bsteem_acc.profile  {}".format(bsteem_acc.profile))
    print("steem_acc.profile {}".format(steem_acc.profile))
    # hp
    print("bsteem_acc.hp  {}".format(bsteem_acc.hp))
    print("steem_acc.hp {}".format(steem_acc.hp))
    # rep
    print("bsteem_acc.rep  {}".format(bsteem_acc.rep))
    print("steem_acc.rep {}".format(steem_acc.rep))
    # balances
    print("bsteem_acc.balances  {}".format(bsteem_acc.balances))
    print("steem_acc.balances {}".format(steem_acc.balances))
    # get_balances()
    print("bsteem_acc.get_balances()  {}".format(bsteem_acc.get_balances()))
    print("steem_acc.get_balances() {}".format(steem_acc.get_balances()))
    # reputation()
    print("bsteem_acc.get_reputation()  {}".format(bsteem_acc.get_reputation()))
    print("steem_acc.reputation() {}".format(steem_acc.reputation()))
    # voting_power()
    print("bsteem_acc.get_voting_power()  {}".format(bsteem_acc.get_voting_power()))
    print("steem_acc.voting_power() {}".format(steem_acc.voting_power()))
    # get_followers()
    print("bsteem_acc.get_followers()  {}".format(bsteem_acc.get_followers()))
    print("steem_acc.get_followers() {}".format(steem_acc.get_followers()))
    # get_following()
    print("bsteem_acc.get_following()  {}".format(bsteem_acc.get_following()))
    print("steem_acc.get_following() {}".format(steem_acc.get_following()))
    # has_voted()
    print("bsteem_acc.has_voted()  {}".format(bsteem_acc.has_voted("@thecrazygm/api-methods-list-for-appbase")))
    print("steem_acc.has_voted() {}".format(steem_acc.has_voted(hivePost("@thecrazygm/api-methods-list-for-appbase"))))
    # curation_stats()
    print("bsteem_acc.curation_stats()  {}".format(bsteem_acc.curation_stats()))
    print("steem_acc.curation_stats() {}".format(steem_acc.curation_stats()))
    # virtual_op_count
    print("bsteem_acc.virtual_op_count()  {}".format(bsteem_acc.virtual_op_count()))
    print("steem_acc.virtual_op_count() {}".format(steem_acc.virtual_op_count()))
    # get_account_votes
    print("bsteem_acc.get_account_votes()  {}".format(bsteem_acc.get_account_votes()))
    print("steem_acc.get_account_votes() {}".format(steem_acc.get_account_votes()))
    # get_withdraw_routes
    print("bsteem_acc.get_withdraw_routes()  {}".format(bsteem_acc.get_withdraw_routes()))
    print("steem_acc.get_withdraw_routes() {}".format(steem_acc.get_withdraw_routes()))
    # get_conversion_requests
    print("bsteem_acc.get_conversion_requests()  {}".format(bsteem_acc.get_conversion_requests()))
    print("steem_acc.get_conversion_requests() {}".format(steem_acc.get_conversion_requests()))
    # export
    # history
    bsteem_hist = []
    for h in bsteem_acc.history(only_ops=["transfer"]):
        bsteem_hist.append(h)
        if len(bsteem_hist) >= 10:
            break
    steem_hist = []
    for h in steem_acc.history(filter_by="transfer", start=0):
        steem_hist.append(h)
        if len(steem_hist) >= 10:
            break
    print("bsteem_acc.history()  {}".format(bsteem_hist))
    print("steem_acc.history() {}".format(steem_hist))
    # history_reverse
    bsteem_hist = []
    for h in bsteem_acc.history_reverse(only_ops=["transfer"]):
        bsteem_hist.append(h)
        if len(bsteem_hist) >= 10:
            break
    steem_hist = []
    for h in steem_acc.history_reverse(filter_by="transfer"):
        steem_hist.append(h)
        if len(steem_hist) >= 10:
            break
    print("bsteem_acc.history_reverse()  {}".format(bsteem_hist))
    print("steem_acc.history_reverse() {}".format(steem_hist))
