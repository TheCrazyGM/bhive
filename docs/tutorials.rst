*********
Tutorials
*********

Bundle Many Operations
----------------------

With Hive, you can bundle multiple operations into a single
transactions. This can be used to do a multi-send (one sender, multiple
receivers), but it also allows to use any other kind of operation. The
advantage here is that the user can be sure that the operations are
executed in the same order as they are added to the transaction.

A block can only include one vote operation and
one comment operation from each sender.

.. code-block:: python

  from pprint import pprint
  from bhive import Hive
  from bhive.account import Account
  from bhive.comment import Comment
  from bhive.instance import set_shared_hive_instance

  # not a real working key
  wif = "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3"

  hv = Hive(
      bundle=True, # Enable bundle broadcast
      # nobroadcast=True, # Enable this for testing
      keys=[wif],
  )
  # Set hv as shared instance
  set_shared_hive_instance(hv)

  # Account and Comment will use now hv
  account = Account("test")

  # Post
  c = Comment("@gtg/witness-gtg-log")

  account.transfer("test1", 1, "STEEM")
  account.transfer("test2", 1, "STEEM")
  account.transfer("test3", 1, "SBD")
  # Upvote post with 25%
  c.upvote(25, voter=account)

  pprint(hv.broadcast())


Use nobroadcast for testing
---------------------------

When using  `nobroadcast=True` the transaction is not broadcasted but printed.

.. code-block:: python

  from pprint import pprint
  from bhive import Hive
  from bhive.account import Account
  from bhive.instance import set_shared_hive_instance

  # Only for testing not a real working key
  wif = "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3"

  # set nobroadcast always to True, when testing
  testnet = Hive(
      nobroadcast=True, # Set to false when want to go live
      keys=[wif],
  )
  # Set testnet as shared instance
  set_shared_hive_instance(testnet)

  # Account will use now testnet
  account = Account("test")

  pprint(account.transfer("test1", 1, "STEEM"))

When executing the script above, the output will be similar to the following:

.. code-block:: js

    Not broadcasting anything!
    {'expiration': '2018-05-01T16:16:57',
     'extensions': [],
     'operations': [['transfer',
                     {'amount': '1.000 HIVE',
                      'from': 'test',
                      'memo': '',
                      'to': 'test1'}]],
     'ref_block_num': 33020,
     'ref_block_prefix': 2523628005,
     'signatures': ['1f57da50f241e70c229ed67b5d61898e792175c0f18ae29df8af414c46ae91eb5729c867b5d7dcc578368e7024e414c237f644629cb0aa3ecafac3640871ffe785']}

Clear BlockchainObject Caching
------------------------------

Each BlockchainObject (Account, Comment, Vote, Witness, Amount, ...) has a glocal cache. This cache
stores all objects and could lead to increased memory consumption. The global cache can be cleared
with a `clear_cache()` call from any BlockchainObject.

.. code-block:: python

  from pprint import pprint
  from bhive.account import Account

  account = Account("test")
  pprint(str(account._cache))
  account1 = Account("test1")
  pprint(str(account._cache))
  pprint(str(account1._cache))
  account.clear_cache()
  pprint(str(account._cache))
  pprint(str(account1._cache))

Simple Sell Script
------------------

.. code-block:: python

    from bhive import Hive
    from bhive.market import Market
    from bhive.price import Price
    from bhive.amount import Amount

    # Only for testing not a real working key
    wif = "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3"

    #
    # Instantiate Hive (pick network via API node)
    #
    hive = Hive(
        nobroadcast=True,   # <<--- set this to False when you want to fire!
        keys=[wif]          # <<--- use your real keys, when going live!
    )

    #
    # This defines the market we are looking at.
    # The first asset in the first argument is the *quote*
    # Sell and buy calls always refer to the *quote*
    #
    market = Market("HBD:HIVE",
        hive_instance=hive
    )

    #
    # Sell an asset for a price with amount (quote)
    #
    print(market.sell(
        Price(100.0, "HIVE/HBD"),
        Amount("0.01 HBD")
    ))


Sell at a timely rate
---------------------

.. code-block:: python

    import threading
    from bhive import Hive
    from bhive.market import Market
    from bhive.price import Price
    from bhive.amount import Amount

    # Only for testing not a real working key
    wif = "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3"

    def sell():
        """ Sell an asset for a price with amount (quote)
        """
        print(market.sell(
            Price(100.0, "HBD/HIVE"),
            Amount("0.01 HIVE")
        ))

        threading.Timer(60, sell).start()


    if __name__ == "__main__":
        #
        # Instantiate Hive (pick network via API node)
        #
        hive = Hive(
            nobroadcast=True,   # <<--- set this to False when you want to fire!
            keys=[wif]          # <<--- use your real keys, when going live!
        )

        #
        # This defines the market we are looking at.
        # The first asset in the first argument is the *quote*
        # Sell and buy calls always refer to the *quote*
        #
        market = Market("HIVE:HBD",
            hive_instance=hive
        )

        sell()

Batch api calls on AppBase
--------------------------

Batch api calls are possible with AppBase RPC nodes.
If you call a Api-Call with add_to_queue=True it is not submitted but stored in rpc_queue.
When a call with add_to_queue=False (default setting) is started,
the complete queue is sended at once to the node. The result is a list with replies.

.. code-block:: python

    from bhive import Hive
    hv = Hive("https://api.hive.blog")
    hv.rpc.get_config(add_to_queue=True)
    hv.rpc.rpc_queue

.. code-block:: python

    [{'method': 'condenser_api.get_config', 'jsonrpc': '2.0', 'params': [], 'id': 6}]

.. code-block:: python

    result = hv.rpc.get_block({"block_num":1}, api="block", add_to_queue=False)
    len(result)

.. code-block:: python

    2


Account history
---------------
Lets calculate the curation reward from the last 7 days:

.. code-block:: python

    from datetime import datetime, timedelta
    from bhive.account import Account
    from bhive.amount import Amount

    acc = Account("gtg")
    stop = datetime.utcnow() - timedelta(days=7)
    reward_vests = Amount("0 VESTS")
    for reward in acc.history_reverse(stop=stop, only_ops=["curation_reward"]):
                reward_vests += Amount(reward['reward'])
    curation_rewards_HP = acc.hive.vests_to_hp(reward_vests.amount)
    print("Rewards are %.3f HP" % curation_rewards_HP)

Lets display all Posts from an account:

.. code-block:: python

    from bhive.account import Account
    from bhive.comment import Comment
    from bhive.exceptions import ContentDoesNotExistsException
    account = Account("thecrazygm")
    c_list = {}
    for c in map(Comment, account.history(only_ops=["comment"])):
        if c.permlink in c_list:
          continue
        try:
             c.refresh()
        except ContentDoesNotExistsException:
             continue
        c_list[c.permlink] = 1
        if not c.is_comment():
            print("%s " % c.title)

Transactionbuilder
------------------
Sign transactions with bhive without using the wallet and build the transaction by hand.
Example with one operation with and without the wallet:

.. code-block:: python

    from bhive import Hive
    from bhive.transactionbuilder import TransactionBuilder
    from bhivebase import operations
    hv = Hive()
    # Uncomment the following when using a wallet:
    # hv.wallet.unlock("secret_password")
    tx = TransactionBuilder(hive_instance=hv)
    op = operations.Transfer(**{"from": 'user_a',
                                "to": 'user_b',
                                "amount": '1.000 HBD',
                                "memo": 'test 2'}))
    tx.appendOps(op)
    # Comment appendWif out and uncomment appendSigner when using a stored key from the wallet
    tx.appendWif('5.....') # `user_a`
    # tx.appendSigner('user_a', 'active')
    tx.sign()
    tx.broadcast()

Example with signing and broadcasting two operations:

.. code-block:: python

    from bhive import Hive
    from bhive.transactionbuilder import TransactionBuilder
    from bhivebase import operations
    hv = Hive()
    # Uncomment the following when using a wallet:
    # hv.wallet.unlock("secret_password")
    tx = TransactionBuilder(hive_instance=hv)
    ops = []
    op = operations.Transfer(**{"from": 'user_a',
                                "to": 'user_b',
                                "amount": '1.000 HBD',
                                "memo": 'test 2'}))
    ops.append(op)
    op = operations.Vote(**{"voter": v,
                            "author": author,
                            "permlink": permlink,
                            "weight": int(percent * 100)})
    ops.append(op)
    tx.appendOps(ops)
    # Comment appendWif out and uncomment appendSigner when using a stored key from the wallet
    tx.appendWif('5.....') # `user_a`
    # tx.appendSigner('user_a', 'active')
    tx.sign()
    tx.broadcast()
