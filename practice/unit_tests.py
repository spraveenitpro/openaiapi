from __future__ import annotations

import types
import unittest
from functools import wraps
from unittest import mock

import stream_latency as sl


def verbose_test(test_func):
    """Decorator to announce test execution and outcome."""

    @wraps(test_func)
    def wrapper(self: unittest.TestCase, *args, **kwargs):
        test_name = f"{self.__class__.__name__}.{test_func.__name__}"
        print(f"Running {test_name}...")
        try:
            return_value = test_func(self, *args, **kwargs)
        except Exception as exc:
            print(f"{test_name} FAILED: {exc}")
            raise
        else:
            print(f"{test_name} PASSED")
            return return_value

    return wrapper


class TestComputeMetrics(unittest.TestCase):
    @verbose_test
    def test_token_count(self) -> None:
        start = 0.0
        timestamps = [0.1, 0.15, 0.3]

        metrics = sl.compute_metrics(start, timestamps)

        self.assertAlmostEqual(metrics.ttft, 0.1)
        # average of (0.05, 0.15) -> 0.1
        self.assertAlmostEqual(metrics.tbt, 0.1)
        self.assertAlmostEqual(metrics.total_latency, 0.3)
        self.assertEqual(metrics.token_count, 3)
        self.assertAlmostEqual(metrics.velocity, 10.0)  # 3 / 0.3

    @verbose_test
    def test_single_token(self) -> None:
        start = 1.0
        timestamps = [1.25]

        metrics = sl.compute_metrics(start, timestamps)

        self.assertAlmostEqual(metrics.ttft, 0.25)
        self.assertAlmostEqual(metrics.tbt, 0.0)
        self.assertAlmostEqual(metrics.total_latency, 0.25)
        self.assertEqual(metrics.token_count, 1)
        self.assertAlmostEqual(metrics.velocity, 4.0)  # 1 / 0.25

    @verbose_test
    def test_no_timestamps_raises(self) -> None:
        with self.assertRaises(ValueError):
            sl.compute_metrics(0.0, [])


class TestEstimatedTokenOutput(unittest.TestCase):
    @verbose_test
    def test_estimated_token_output_large(self) -> None:
        metrics = sl.compute_metrics(0.0, [0.1])
        self.assertTrue(metrics.estimated_token_output > 1000)


class TestMeasureLatency(unittest.TestCase):
    def _build_dummy_openai(self, iterator):
        completions = types.SimpleNamespace(create=lambda **kwargs: iterator)
        chat = types.SimpleNamespace(completions=completions)
        dummy_openai = types.SimpleNamespace(chat=chat, api_key="sk-test")
        dummy_openai.ChatCompletion = types.SimpleNamespace(create=lambda **kwargs: iterator)  # type: ignore[attr-defined]

        return dummy_openai

    @verbose_test
    def test_latency_measurement(self) -> None:
        token_chunks = [
            {"choices": [{"delta": {"content": "Hello"}}]},
            {"choices": [{"delta": {"content": "world"}}]},
        ]

        iterator = iter(token_chunks)

        dummy_openai = self._build_dummy_openai(iterator)

        perf_times = [0.0, 0.1, 0.3]

        with mock.patch.multiple(
            sl,
            openai=dummy_openai,  
            _OPENAI_AVAILABLE=True,
        ), mock.patch.object(sl.time, "perf_counter", side_effect=perf_times):

            metrics = sl.measure_latency("dummy prompt")

        self.assertEqual(metrics.token_count, 2)
        self.assertAlmostEqual(metrics.ttft, 0.1)
        self.assertAlmostEqual(metrics.tbt, 0.2)
        self.assertAlmostEqual(metrics.total_latency, 0.3)
        self.assertAlmostEqual(metrics.velocity, 2 / 0.3)


if __name__ == "__main__":
    unittest.main(verbosity=2)
