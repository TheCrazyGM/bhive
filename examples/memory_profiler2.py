from __future__ import print_function
from memory_profiler import profile
import sys
from bhive.hive import Hive
from bhive.account import Account
from bhive.blockchain import Blockchain
from bhive.instance import set_shared_hive_instance, clear_cache
from bhive.storage import configStorage as config
from bhiveapi.graphenerpc import GrapheneRPC
import logging
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@profile
def profiling(node, name_list, shared_instance=True, clear_acc_cache=False, clear_all_cache=True):
    print("shared_instance %d clear_acc_cache %d clear_all_cache %d" %
          (shared_instance, clear_acc_cache, clear_all_cache))
    if not shared_instance:
        hv = Hive(node=node)
        print(str(hv))
    else:
        hv = None
    acc_dict = {}
    for name in name_list:
        acc = Account(name, hive_instance=hv)
        acc_dict[name] = acc
        if clear_acc_cache:
            acc.clear_cache()
        acc_dict = {}
    if clear_all_cache:
        clear_cache()
    if not shared_instance:
        del hv.rpc


if __name__ == "__main__":
    hv = Hive()
    print("Shared instance: " + str(hv))
    set_shared_hive_instance(hv)
    b = Blockchain()
    account_list = []
    for a in b.get_all_accounts(limit=500):
        account_list.append(a)
    shared_instance = False
    clear_acc_cache = False
    clear_all_cache = False
    node = "https://api.hive.blog"
    n = 3
    for i in range(1, n + 1):
        print("%d of %d" % (i, n))
        profiling(node, account_list, shared_instance=shared_instance, clear_acc_cache=clear_acc_cache, clear_all_cache=clear_all_cache)
