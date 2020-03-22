Quickstart
==========

Hive
-----
The hive object is the connection to the Hive blockchain.
By creating this object different options can be set.

.. note:: All init methods of bhive classes can be given
          the ``hive_instance=`` parameter to assure that
          all objects use the same hive object. When the
          ``hive_instance=`` parameter is not used, the 
          hive object is taken from get_shared_hive_instance().

          :func:`bhive.instance.shared_hive_instance` returns a global instance of hive.
          It can be set by :func:`bhive.instance.set_shared_hive_instance` otherwise it is created
          on the first call.

.. code-block:: python

   from bhive import Hive
   from bhive.account import Account
   hv = Hive()
   account = Account("test", hive_instance=hv)

.. code-block:: python

   from bhive import Hive
   from bhive.account import Account
   from bhive.instance import set_shared_hive_instance
   hv = Hive()
   set_shared_hive_instance(hv)
   account = Account("test")

Wallet and Keys
---------------
Each account has the following keys:

* Posting key (allows accounts to post, vote, edit, rehive and follow/mute)
* Active key (allows accounts to transfer, power up/down, voting for witness, ...)
* Memo key (Can be used to encrypt/decrypt memos)
* Owner key (The most important key, should not be used with bhive)

Outgoing operation, which will be stored in the hive blockchain, have to be
signed by a private key. E.g. Comment or Vote operation need to be signed by the posting key
of the author or upvoter. Private keys can be provided to bhive temporary or can be
stored encrypted in a sql-database (wallet).

.. note:: Before using the wallet the first time, it has to be created and a password has
          to set. The wallet content is available to bhivepy and all python scripts, which have
          access to the sql database file.

Creating a wallet
~~~~~~~~~~~~~~~~~
``hive.wallet.wipe(True)`` is only necessary when there was already an wallet created.

.. code-block:: python

   from bhive import Hive
   hive = Hive()
   hive.wallet.wipe(True)
   hive.wallet.unlock("wallet-passphrase")

Adding keys to the wallet
~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: python

   from bhive import Hive
   hive = Hive()
   hive.wallet.unlock("wallet-passphrase")
   hive.wallet.addPrivateKey("xxxxxxx")
   hive.wallet.addPrivateKey("xxxxxxx")

Using the keys in the wallet
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from bhive import Hive
   hive = Hive()
   hive.wallet.unlock("wallet-passphrase")
   account = Account("test", hive_instance=hive)
   account.transfer("<to>", "<amount>", "<asset>", "<memo>")

Private keys can also set temporary
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from bhive import Hive
   hive = Hive(keys=["xxxxxxxxx"])
   account = Account("test", hive_instance=hive)
   account.transfer("<to>", "<amount>", "<asset>", "<memo>")

Receiving information about blocks, accounts, votes, comments, market and witness
---------------------------------------------------------------------------------

Receive all Blocks from the Blockchain

.. code-block:: python

   from bhive.blockchain import Blockchain
   blockchain = Blockchain()
   for op in blockchain.stream():
       print(op)

Access one Block

.. code-block:: python

   from bhive.block import Block
   print(Block(1))

Access an account

.. code-block:: python

   from bhive.account import Account
   account = Account("test")
   print(account.balances)
   for h in account.history():
       print(h)

A single vote

.. code-block:: python

   from bhive.vote import Vote
   vote = Vote(u"@gtg/ffdhu-gtg-witness-log|gandalf")
   print(vote.json())

All votes from an account

.. code-block:: python

   from bhive.vote import AccountVotes
   allVotes = AccountVotes("gtg")

Access a post

.. code-block:: python

   from bhive.comment import Comment
   comment = Comment("@gtg/ffdhu-gtg-witness-log")
   print(comment["active_votes"])

Access the market

.. code-block:: python

   from bhive.market import Market
   market = Market("HBD:HIVE")
   print(market.ticker())

Access a witness

.. code-block:: python

   from bhive.witness import Witness
   witness = Witness("gtg")
   print(witness.is_active)

Sending transaction to the blockchain
-------------------------------------

Sending a Transfer

.. code-block:: python

   from bhive import Hive
   hive = Hive()
   hive.wallet.unlock("wallet-passphrase")
   account = Account("test", hive_instance=hive)
   account.transfer("null", 1, "HBD", "test")

Upvote a post

.. code-block:: python

   from bhive.comment import Comment
   from bhive import Hive
   hive = Hive()
   hive.wallet.unlock("wallet-passphrase")
   comment = Comment("@gtg/ffdhu-gtg-witness-log", hive_instance=hive)
   comment.upvote(weight=10, voter="test")

Publish a post to the blockchain

.. code-block:: python

   from bhive import Hive
   hive = Hive()
   hive.wallet.unlock("wallet-passphrase")
   hive.post("title", "body", author="test", tags=["a", "b", "c", "d", "e"], self_vote=True)

Sell HIVE on the market

.. code-block:: python

   from bhive.market import Market
   from bhive import Hive
   hive.wallet.unlock("wallet-passphrase")
   market = Market("HBD:HIVE", hive_instance=hive)
   print(market.ticker())
   market.hive.wallet.unlock("wallet-passphrase")
   print(market.sell(300, 100))  # sell 100 HIVE for 300 HIVE/HBD
