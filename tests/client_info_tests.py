import unittest
import time

from source.client_info import ClientInfo


class TestClientInfo(unittest.TestCase):
    def test_update_incidents_cnt(self):
        # arrange
        client_info = ClientInfo('abc', '127.0.0.1', 3)
        expected_cnt = 1

        # act
        client_info.update_incidents_cnt(expected_cnt)

        # assert
        self.assertEqual(expected_cnt, client_info.incidents_cnt)

    def test_change_time_after_update_incidents_cnt(self):
        # arrange
        client_info = ClientInfo('abc', '127.0.0.1', 3)
        previous_time = client_info.update_time

        # act
        time.sleep(1)
        client_info.update_incidents_cnt(client_info.incidents_cnt)

        # assert
        self.assertGreater(client_info.update_time, previous_time)
