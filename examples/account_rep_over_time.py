#!/usr/bin/python
import sys
import datetime as dt
from bhive.amount import Amount
from bhive.utils import parse_time, formatTimeString, addTzInfo
from bhive.instance import set_shared_hive_instance
from bhive import Hive
from bhive.snapshot import AccountSnapshot
import matplotlib as mpl
# mpl.use('Agg')
# mpl.use('TkAgg')
import matplotlib.pyplot as plt


if __name__ == "__main__":
    if len(sys.argv) != 2:
        # print("ERROR: command line parameter mismatch!")
        # print("usage: %s [account]" % (sys.argv[0]))
        account = "thecrazygm"
    else:
        account = sys.argv[1]
    acc_snapshot = AccountSnapshot(account)
    acc_snapshot.get_account_history()
    acc_snapshot.build(enable_in_votes=True)
    acc_snapshot.build_rep_arrays()
    timestamps = acc_snapshot.rep_timestamp
    rep = acc_snapshot.rep
    plt.figure(figsize=(12, 6))
    opts = {'linestyle': '-', 'marker': '.'}
    plt.plot_date(timestamps, rep, label="Reputation", **opts)
    plt.grid()
    plt.legend()
    plt.title("Reputation over time - @%s" % (account))
    plt.xlabel("Date")
    plt.ylabel("Reputation over time")
    # plt.show()
    plt.savefig("reputation-%s.png" % (account))
    print("last reputation %f" % (rep[-1]))
