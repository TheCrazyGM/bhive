# This Python file uses the following encoding: utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import hashlib
import base64
import json
import random
import requests
import struct
from datetime import datetime
from binascii import hexlify
from .instance import shared_steem_instance
from .account import Account
from bhivegraphenebase.py23 import py23_bytes
from bhivegraphenebase.ecdsasig import sign_message
try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin


class Conveyor(object):
    """ Class to access hiveio Conveyor instances:
        https://gitlab.syncad.com/hive-group//conveyor

        Description from the official documentation:

        * Feature flags: "Feature flags allows our apps (condenser mainly) to
          hide certain features behind flags."
        * User data: "Conveyor is the central point for storing sensitive user
          data (email, phone, etc). No other services should store this data
          and should instead query for it here every time."
        * User tags: "Tagging mechanism for other services, allows defining and
          assigning tags to accounts (or other identifiers) and querying for
          them."

        Not contained in the documentation, but implemented and working:

        * Draft handling: saving, listing and removing post drafts
          consisting of a post title and a body.

        The underlying RPC authentication and request signing procedure is
        described here: https://gitlab.syncad.com/hive-group//rpc-auth

    """

    def __init__(self, url="https://conveyor.hive.blog",
                 steem_instance=None):
        """ Initialize a Conveyor instance
            :param str url: (optional) URL to the Conveyor API, defaults to
                https://conveyor.hive.blog
            :param bhive.hive.Hive steem_instance: Hive instance

        """

        self.url = url
        self.hive = steem_instance or shared_steem_instance()
        self.id = 0
        self.ENCODING = 'utf-8'
        self.TIMEFORMAT = '%Y-%m-%dT%H:%M:%S.%f'
        self.K = hashlib.sha256(py23_bytes('steem_jsonrpc_auth',
                                           self.ENCODING)).digest()

    def prehash_message(self, timestamp, account, method, params, nonce):
        """ Prepare a hash for the Conveyor API request with SHA256 according
            to https://gitlab.syncad.com/hive-group//rpc-auth
            Hashing of `second` is then done inside `ecdsasig.sign_message()`.

            :param str timestamp: valid iso8601 datetime ending in "Z"
            :param str account: valid hive blockchain account name
            :param str method: Conveyor method name to be called
            :param bytes param: base64 encoded request parameters
            :param bytes nonce: random 8 bytes

        """
        first = hashlib.sha256(py23_bytes(timestamp + account + method + params, self.ENCODING))
        return self.K + first.digest() + nonce

    def _request(self, account, method, params, key):
        """Assemble the request, hash it, sign it and send it to the Conveyor
            instance. Returns the server response as JSON.

            :param str account: account name
            :param str method: Conveyor method name to be called
            :param dict params: request parameters as `dict`
            :param str key: Hive posting key for signing

        """
        params_bytes = py23_bytes(json.dumps(params), self.ENCODING)
        params_enc = base64.b64encode(params_bytes).decode(self.ENCODING)
        timestamp = datetime.utcnow().strftime(self.TIMEFORMAT)[:-3] + "Z"
        nonce_int = random.getrandbits(64)
        nonce_bytes = struct.pack('>Q', nonce_int)  # 64bit ULL, big endian
        nonce_str = "%016x" % (nonce_int)

        message = self.prehash_message(timestamp, account, method,
                                       params_enc, nonce_bytes)
        signature = sign_message(message, key)
        signature_hex = hexlify(signature).decode(self.ENCODING)

        request = {
            "jsonrpc": "2.0",
            "id": self.id,
            "method": method,
            "params": {
                "__signed": {
                    "account": account,
                    "nonce": nonce_str,
                    "params": params_enc,
                    "signatures": [signature_hex],
                    "timestamp": timestamp
                }
            }
        }
        r = requests.post(self.url, data=json.dumps(request))
        self.id += 1
        return r.json()

    def _conveyor_method(self, account, signing_account, method, params):
        """ Wrapper function to handle account and key lookups

            :param str account: name of the addressed account
            :param str signing_account: name of the account to sign the request
            :param method: Conveyor method name to be called
            :params dict params: request parameters as `dict`

        """
        account = Account(account, steem_instance=self.hive)
        if signing_account is None:
            signer = account
        else:
            signer = Account(signing_account, steem_instance=self.hive)
        if "posting" not in signer:
            signer.refresh()
        if "posting" not in signer:
            raise AssertionError("Could not access posting permission")
        for authority in signer["posting"]["key_auths"]:
            posting_wif = self.hive.wallet.getPrivateKeyForPublicKey(
                authority[0])
        return self._request(account['name'], method, params,
                             posting_wif)

    def get_user_data(self, account, signing_account=None):
        """ Get the account's email address and phone number. The request has to be
            signed by the requested account or an admin account.

            :param str account: requested account
            :param str signing_account: (optional) account to sign the
                request. If unset, `account` is used.

            Example:

            .. code-block:: python

                from bhive import Hive
                from bhive.conveyor import Conveyor
                s = Hive(keys=["5JPOSTINGKEY"])
                c = Conveyor(steem_instance=s)
                print(c.get_user_data('accountname'))

        """
        account = Account(account, steem_instance=self.hive)
        user_data = self._conveyor_method(account, signing_account,
                                          "conveyor.get_user_data",
                                          [account['name']])
        if "result" in user_data:
            return user_data["result"]
        else:
            return user_data

    def set_user_data(self, account, params, signing_account=None):
        """ Set the account's email address and phone number. The request has to be
            signed by an admin account.

            :param str account: requested account
            :param dict param: user data to be set
            :param str signing_account: (optional) account to sign the
                request. If unset, `account` is used.

            Example:

            .. code-block:: python

                from bhive import Hive
                from bhive.conveyor import Conveyor
                s = Hive(keys=["5JADMINPOSTINGKEY"])
                c = Conveyor(steem_instance=s)
                userdata = {'email': 'foo@bar.com', 'phone':'+123456789'}
                c.set_user_data('accountname', userdata, 'adminaccountname')

        """
        return self._conveyor_method(account, signing_account,
                                     "conveyor.set_user_data",
                                     [params])

    def get_feature_flags(self, account, signing_account=None):
        """ Get the account's feature flags. The request has to be signed by the
            requested account or an admin account.

            :param str account: requested account
            :param str signing_account: (optional) account to sign the
                request. If unset, `account` is used.

            Example:

            .. code-block:: python

                from bhive import Hive
                from bhive.conveyor import Conveyor
                s = Hive(keys=["5JPOSTINGKEY"])
                c = Conveyor(steem_instance=s)
                print(c.get_feature_flags('accountname'))

        """
        account = Account(account, steem_instance=self.hive)
        feature_flags = self._conveyor_method(account, signing_account,
                                              "conveyor.get_feature_flags",
                                              [account['name']])
        if "result" in feature_flags:
            return feature_flags["result"]
        else:
            return feature_flags

    def get_feature_flag(self, account, flag, signing_account=None):
        """ Test if a specific feature flag is set for an account. The request
            has to be signed by the requested account or an admin account.

            :param str account: requested account
            :param str flag: flag to be tested
            :param str signing_account: (optional) account to sign the
                request. If unset, `account` is used.

            Example:

            .. code-block:: python

                from bhive import Hive
                from bhive.conveyor import Conveyor
                s = Hive(keys=["5JPOSTINGKEY"])
                c = Conveyor(steem_instance=s)
                print(c.get_feature_flag('accountname', 'accepted_tos'))

        """
        account = Account(account, steem_instance=self.hive)
        return self._conveyor_method(account, signing_account,
                                     "conveyor.get_feature_flag",
                                     [account['name'], flag])

    def save_draft(self, account, title, body):
        """ Save a draft in the Conveyor database

            :param str account: requested account
            :param str title: draft post title
            :param str body: draft post body

        """
        account = Account(account, steem_instance=self.hive)
        draft = {'title': title, 'body': body}
        return self._conveyor_method(account, None,
                                     "conveyor.save_draft",
                                     [account['name'], draft])

    def list_drafts(self, account):
        """ List all saved drafts from `account`

            :param str account: requested account

            Sample output:

            .. code-block:: js

                {
                    'jsonrpc': '2.0', 'id': 2, 'result': [
                        {'title': 'draft-title', 'body': 'draft-body',
                         'uuid': '06497e1e-ac30-48cb-a069-27e1672924c9'}
                    ]
                }

        """
        account = Account(account, steem_instance=self.hive)
        return self._conveyor_method(account, None,
                                     "conveyor.list_drafts",
                                     [account['name']])

    def remove_draft(self, account, uuid):
        """ Remove a draft from the Conveyor database

            :param str account: requested account
            :param str uuid: draft identifier as returned from
                `list_drafts`

        """
        account = Account(account, steem_instance=self.hive)
        return self._conveyor_method(account, None,
                                     "conveyor.remove_draft",
                                     [account['name'], uuid])

    def healthcheck(self):
        """ Get the Conveyor status

            Sample output:

            .. code-block:: js

                {
                    'ok': True, 'version': '1.1.1-4d28e36-1528725174',
                    'date': '2018-07-21T12:12:25.502Z'
                }

        """
        url = urljoin(self.url, "/.well-known/healthcheck.json")
        r = requests.get(url)
        return r.json()
