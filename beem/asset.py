# This Python file uses the following encoding: utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import json
from .exceptions import AssetDoesNotExistsException
from .blockchainobject import BlockchainObject


class Asset(BlockchainObject):
    """ Deals with Assets of the network.

        :param str Asset: Symbol name or object id of an asset
        :param bool lazy: Lazy loading
        :param bool full: Also obtain bitasset-data and dynamic asset dat
        :param Hive hive_instance: Hive
            instance
        :returns: All data of an asset

        .. note:: This class comes with its own caching function to reduce the
                  load on the API server. Instances of this class can be
                  refreshed with ``Asset.refresh()``.
    """
    type_id = 3

    def __init__(
        self,
        asset,
        lazy=False,
        full=False,
        hive_instance=None
    ):
        self.full = full
        super(Asset, self).__init__(
            asset,
            lazy=lazy,
            full=full,
            hive_instance=hive_instance
        )
        # self.refresh()

    def refresh(self):
        """ Refresh the data from the API server
        """
        self.chain_params = self.hive.get_network()
        if self.chain_params is None:
            from bhivegraphenebase.chains import known_chains
            self.chain_params = known_chains["HIVEAPPBASE"]
        self["asset"] = ""
        found_asset = False
        for asset in self.chain_params["chain_assets"]:
            if self.identifier in [asset["symbol"], asset["asset"], asset["id"]]:
                self["asset"] = asset["asset"]
                self["precision"] = asset["precision"]
                self["id"] = asset["id"]
                self["symbol"] = asset["symbol"]
                found_asset = True
                break
        if not found_asset:
            raise AssetDoesNotExistsException(self.identifier + " chain_assets:" + str(self.chain_params["chain_assets"]))

    @property
    def symbol(self):
        return self["symbol"]

    @property
    def asset(self):
        return self["asset"]

    @property
    def precision(self):
        return self["precision"]

    def __eq__(self, other):
        if isinstance(other, (Asset, dict)):
            return self["symbol"] == other["symbol"] and self["asset"] == other["asset"] and self["precision"] == other["precision"]
        else:
            return self["symbol"] == other

    def __ne__(self, other):
        if isinstance(other, (Asset, dict)):
            return self["symbol"] != other["symbol"] or self["asset"] != other["asset"] or self["precision"] != other["precision"]
        else:
            return self["symbol"] != other
