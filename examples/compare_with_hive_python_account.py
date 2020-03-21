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
    bhive_acc = Account("thecrazygm", hive_instance=hv)
    hv2 = hiveHive(nodes=["https://api.hive.blog"])
    hive_acc = hiveAccount("thecrazygm", hived_instance=hv2)

    # profile
    print("bhive_acc.profile  {}".format(bhive_acc.profile))
    print("hive_acc.profile {}".format(hive_acc.profile))
    # hp
    print("bhive_acc.hp  {}".format(bhive_acc.hp))
    print("hive_acc.hp {}".format(hive_acc.hp))
    # rep
    print("bhive_acc.rep  {}".format(bhive_acc.rep))
    print("hive_acc.rep {}".format(hive_acc.rep))
    # balances
    print("bhive_acc.balances  {}".format(bhive_acc.balances))
    print("hive_acc.balances {}".format(hive_acc.balances))
    # get_balances()
    print("bhive_acc.get_balances()  {}".format(bhive_acc.get_balances()))
    print("hive_acc.get_balances() {}".format(hive_acc.get_balances()))
    # reputation()
    print("bhive_acc.get_reputation()  {}".format(bhive_acc.get_reputation()))
    print("hive_acc.reputation() {}".format(hive_acc.reputation()))
    # voting_power()
    print("bhive_acc.get_voting_power()  {}".format(bhive_acc.get_voting_power()))
    print("hive_acc.voting_power() {}".format(hive_acc.voting_power()))
    # get_followers()
    print("bhive_acc.get_followers()  {}".format(bhive_acc.get_followers()))
    print("hive_acc.get_followers() {}".format(hive_acc.get_followers()))
    # get_following()
    print("bhive_acc.get_following()  {}".format(bhive_acc.get_following()))
    print("hive_acc.get_following() {}".format(hive_acc.get_following()))
    # has_voted()
    print("bhive_acc.has_voted()  {}".format(bhive_acc.has_voted("@thecrazygm/api-methods-list-for-appbase")))
    print("hive_acc.has_voted() {}".format(hive_acc.has_voted(hivePost("@thecrazygm/api-methods-list-for-appbase"))))
    # curation_stats()
    print("bhive_acc.curation_stats()  {}".format(bhive_acc.curation_stats()))
    print("hive_acc.curation_stats() {}".format(hive_acc.curation_stats()))
    # virtual_op_count
    print("bhive_acc.virtual_op_count()  {}".format(bhive_acc.virtual_op_count()))
    print("hive_acc.virtual_op_count() {}".format(hive_acc.virtual_op_count()))
    # get_account_votes
    print("bhive_acc.get_account_votes()  {}".format(bhive_acc.get_account_votes()))
    print("hive_acc.get_account_votes() {}".format(hive_acc.get_account_votes()))
    # get_withdraw_routes
    print("bhive_acc.get_withdraw_routes()  {}".format(bhive_acc.get_withdraw_routes()))
    print("hive_acc.get_withdraw_routes() {}".format(hive_acc.get_withdraw_routes()))
    # get_conversion_requests
    print("bhive_acc.get_conversion_requests()  {}".format(bhive_acc.get_conversion_requests()))
    print("hive_acc.get_conversion_requests() {}".format(hive_acc.get_conversion_requests()))
    # export
    # history
    bhive_hist = []
    for h in bhive_acc.history(only_ops=["transfer"]):
        bhive_hist.append(h)
        if len(bhive_hist) >= 10:
            break
    hive_hist = []
    for h in hive_acc.history(filter_by="transfer", start=0):
        hive_hist.append(h)
        if len(hive_hist) >= 10:
            break
    print("bhive_acc.history()  {}".format(bhive_hist))
    print("hive_acc.history() {}".format(hive_hist))
    # history_reverse
    bhive_hist = []
    for h in bhive_acc.history_reverse(only_ops=["transfer"]):
        bhive_hist.append(h)
        if len(bhive_hist) >= 10:
            break
    hive_hist = []
    for h in hive_acc.history_reverse(filter_by="transfer"):
        hive_hist.append(h)
        if len(hive_hist) >= 10:
            break
    print("bhive_acc.history_reverse()  {}".format(bhive_hist))
    print("hive_acc.history_reverse() {}".format(hive_hist))
