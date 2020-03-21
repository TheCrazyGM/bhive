bhiveapi\.websocket
==================

This class allows subscribe to push notifications from the Hive
node.

.. code-block:: python

    from pprint import pprint
    from bhiveapi.websocket import HiveWebsocket

    ws = HiveWebsocket(
        "wss://gtg.hive.house:8090",
        accounts=["test"],
        on_block=print,
    )

    ws.run_forever()


.. autoclass:: bhiveapi.websocket.HiveWebsocket
    :members:
    :undoc-members:
    :private-members:
    :special-members:


