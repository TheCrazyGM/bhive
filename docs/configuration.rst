*************
Configuration
*************

The pyhive library comes with its own local configuration database
that stores information like

* API node URLs
* default account name
* the encrypted master password
* the default voting weight
* if keyring should be used for unlocking the wallet

and potentially more.

You can access those variables like a regular dictionary by using

.. code-block:: python

    from bhive import Hive
    hive = Hive()
    print(hive.config.items())

Keys can be added and changed like they are for regular dictionaries.

If you don't want to load the :class:`bhive.hive.Hive` class, you
can load the configuration directly by using:

.. code-block:: python

    from bhive.storage import configStorage as config

It is also possible to access the configuration with the commandline tool `bhivepy`:

.. code-block:: bash

    bhivepy config

API node URLs
-------------

The default node URLs which will be used when  `node` is  `None` in :class:`bhive.hive.Hive` class
is stored in `config["nodes"]` as string. The list can be get and set by:

.. code-block:: python

    from bhive import Hive
    hive = Hive()
    node_list = hive.get_default_nodes()
    node_list = node_list[1:] + [node_list[0]]
    hive.set_default_nodes(node_list)

bhivepy can also be used to set nodes:

.. code-block:: bash

        bhivepy set nodes wss://hived.privex.io
        bhivepy set nodes "['wss://hived.privex.io', 'wss://gtg.hive.house:8090']"

The default nodes can be reset to the default value. When the first node does not
answer, hive should be set to the offline mode. This can be done by:

.. code-block:: bash

        bhivepy -o set nodes ""

or

.. code-block:: python

    from bhive import Hive
    hive = Hive(offline=True)
    hive.set_default_nodes("")

Default account
---------------

The default account name is used in some functions, when no account name is given.
It is also used in  `bhivepy` for all account related functions.

.. code-block:: python

    from bhive import Hive
    hive = Hive()
    hive.set_default_account("test")
    hive.config["default_account"] = "test"

or by bhivepy with

.. code-block:: bash

        bhivepy set default_account test

Default voting weight
---------------------

The default vote weight is used for voting, when no vote weight is given.

.. code-block:: python

    from bhive import Hive
    hive = Hive()
    hive.config["default_vote_weight"] = 100

or by bhivepy with

.. code-block:: bash

        bhivepy set default_vote_weight 100


Setting password_storage
------------------------

The password_storage can be set to:

* environment, this is the default setting. The master password for the wallet can be provided in the environment variable `UNLOCK`.
* keyring (when set with bhivepy, it asks for the wallet password)

.. code-block:: bash

        bhivepy set password_storage environment
        bhivepy set password_storage keyring



Environment variable for storing the master password
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When `password_storage` is set to `environment`, the master password can be stored in `UNLOCK`
for unlocking automatically the wallet.

Keyring support for bhivepy and wallet
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In order to use keyring for storing the wallet password, the following steps are necessary:

* Install keyring: `pip install keyring`
* Change `password_storage` to `keyring` with `bhivepy` and enter the wallet password.

It also possible to change the password in the keyring by

.. code-block:: bash

    python -m keyring set bhive wallet

The stored master password can be displayed in the terminal by

.. code-block:: bash

    python -m keyring get bhive wallet

When keyring is set as `password_storage` and the stored password in the keyring
is identically to the set master password of the wallet, the wallet is automatically
unlocked everytime it is used.

Testing if unlocking works
~~~~~~~~~~~~~~~~~~~~~~~~~~

Testing if the master password is correctly provided by keyring or the `UNLOCK` variable:

.. code-block:: python

    from bhive import Hive
    hive = Hive()
    print(hive.wallet.locked())

When the output is False, automatic unlocking with keyring or the `UNLOCK` variable works.
It can also tested by bhivepy with

.. code-block:: bash

        bhivepy walletinfo --test-unlock

When no password prompt is shown, unlocking with keyring or the `UNLOCK` variable works.
