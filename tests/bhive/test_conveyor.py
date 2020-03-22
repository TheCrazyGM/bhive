from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import unittest
from bhive import Hive
from bhive.conveyor import Conveyor
from bhive.instance import set_shared_steem_instance
from bhive.nodelist import NodeList

wif = '5Jh1Gtu2j4Yi16TfhoDmg8Qj3ULcgRi7A49JXdfUUTVPkaFaRKz'


class Testcases(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        nodelist = NodeList()
        hv = Hive(node=nodelist.get_nodes(), nobroadcast=True,
                    num_retries=10, expiration=120)
        set_shared_steem_instance(hv)

    def test_healthcheck(self):
        health = Conveyor().healthcheck()
        self.assertTrue('version' in health)
        self.assertTrue('ok' in health)
        self.assertTrue('date' in health)

if __name__ == "__main__":
    unittest.main()
