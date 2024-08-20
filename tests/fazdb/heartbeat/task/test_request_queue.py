from datetime import datetime as dt
import unittest

from fazdb.heartbeat.task import RequestQueue


class TestRequestList(unittest.TestCase):

    def setUp(self) -> None:
        self.request_list = RequestQueue()

    async def mock_coro(self, arg: str) -> str:
        return arg

    def test_enqueue_and_dequeue(self) -> None:
        # sourcery skip: class-extract-method
        # PREPARE
        test_coro1 = self.mock_coro("foo")
        test_req_ts1 = dt.now().timestamp() - 100

        # ACT
        self.request_list.enqueue(test_req_ts1, test_coro1)

        # ASSERT
        # NOTE: Assert that the request is enqueued properly
        self.assertEqual(len(self.request_list._list), 1)
        self.assertEqual(self.request_list._list[0].coro, test_coro1)
        self.assertEqual(self.request_list._list[0]._req_ts, test_req_ts1)

        # ACT
        result = self.request_list.dequeue(1)

        # ASSERT
        # NOTE: Assert that the correct request is dequeued
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], test_coro1)

    def test_dequeue_with_request_ts(self) -> None:
        # PREPARE
        test_coro1 = self.mock_coro("foo")
        test_coro2 = self.mock_coro("bar")
        test_req_ts1 = dt.now().timestamp() - 100
        test_req_ts2 = dt.now().timestamp() - 200  # earlier timestamp

        self.request_list.enqueue(test_req_ts1, test_coro1)
        self.request_list.enqueue(test_req_ts2, test_coro2)

        # ACT
        result = self.request_list.dequeue(1)

        # ASSERT
        # NOTE: Assert that the request with the earliest timestamp is dequeued first
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], test_coro2)
        remaining_item = self.request_list._list.pop()
        # NOTE: Assert that the remaining item is the one with the later timestamp
        self.assertEqual(remaining_item.coro, test_coro1)
        self.assertEqual(remaining_item._req_ts, test_req_ts1)

    def test_dequeue_with_priority(self) -> None:
        # PREPARE
        test_coro1 = self.mock_coro("foo")
        test_coro2 = self.mock_coro("bar")
        test_req_ts1 = dt.now().timestamp() - 100
        test_req_ts2 = (
            dt.now().timestamp() - 50
        )  # should still return higher priority
        self.request_list.enqueue(test_req_ts1, test_coro1, priority=100)
        self.request_list.enqueue(
            test_req_ts2, test_coro2, priority=200
        )  # higher priority

        # ACT
        result = self.request_list.dequeue(1)

        # ASSERT
        self.assertEqual(len(result), 1)
        self.assertEqual(result.pop(), test_coro2)

    def test_dequeue_equal_all(self) -> None:
        # PREPARE
        test_coros = [self.mock_coro(str(i)) for i in range(100)]
        test_req_ts = 0
        for coro in test_coros:
            self.request_list.enqueue(test_req_ts, coro)

        # ACT
        result = self.request_list.dequeue(15)

        # ASSERT
        self.assertEqual(len(result), 15)
        for coro in result:
            self.assertTrue(coro in test_coros)

    def test_request_item_is_eligible(self) -> None:
        # PREPARE
        test_coro1 = self.mock_coro("foo")
        test_req_ts1 = dt.now().timestamp() - 1  # Past timestamp
        request_item = RequestQueue.RequestItem(test_coro1, 100, test_req_ts1)

        # ASSERT
        self.assertTrue(request_item.is_eligible())

    def test_request_item_is_not_eligible(self) -> None:
        # PREPARE
        test_coro1 = self.mock_coro("foo")
        test_req_ts1 = dt.now().timestamp() + 1000  # Future timestamp
        request_item = RequestQueue.RequestItem(test_coro1, 100, test_req_ts1)

        # ASSERT
        # NOTE: Assert that request item is not eligible
        self.assertFalse(request_item.is_eligible())

    def test_request_item_comparison(self) -> None:
        # PREPARE
        test_coro1 = self.mock_coro("foo")
        test_coro2 = self.mock_coro("bar")
        request_item1 = RequestQueue.RequestItem(test_coro1, 100, 0)
        request_item2 = RequestQueue.RequestItem(test_coro2, 200, 0)

        # ASSERT
        self.assertLess(request_item2, request_item1)

    def test_request_item_equality(self) -> None:
        # PREPARE
        test_coro1 = self.mock_coro("foo")
        test_coro2 = self.mock_coro("foo")
        request_ts = dt.now().timestamp()
        request_item1 = RequestQueue.RequestItem(test_coro1, 100, request_ts)
        request_item2 = RequestQueue.RequestItem(test_coro2, 100, request_ts)

        # ASSERT
        self.assertEqual(request_item1, request_item2)

    def tearDown(self) -> None:
        pass
