import sys
import time
from dataclasses import dataclass
from typing import Iterable, List, Sequence

from dotenv import load_dotenv

try:  # pragma: no cover - import guard exercised via unit tests
    import openai

    _OPENAI_AVAILABLE = True
except ImportError:  # pragma: no cover - exercised only when package missing
    openai = None  # type: ignore[assignment]
    _OPENAI_AVAILABLE = False


@dataclass
class LatencyMetrics:
    ttft: float
    tbt: float
    velocity: float
    total_latency: float
    token_count: int

    @property
    def estimated_token_output(self) -> float:
        """Project token output for a two-minute window."""

        return self.velocity * 120.0


load_dotenv(override=True)


def compute_metrics(start: float, timestamps: Sequence[float]) -> LatencyMetrics:
    if not timestamps:
        raise ValueError("timestamps must include at least one token arrival")

    token_count = len(timestamps)
    total_latency = timestamps[-1] - start
    ttft = timestamps[0] - start

    if token_count > 1:
        gaps = [curr - prev for prev, curr in zip(timestamps[:-1], timestamps[1:])]
        tbt = sum(gaps) / len(gaps)
    else:
        tbt = 0.0

    velocity = (token_count / total_latency) if total_latency > 0 else 0.0

    return LatencyMetrics(
        ttft=ttft,
        tbt=tbt,
        velocity=velocity,
        total_latency=total_latency,
        token_count=token_count,
    )


def _stream_chat(prompt: str, model: str) -> Iterable[object]:
    if not _OPENAI_AVAILABLE or openai is None:  # pragma: no cover - defensive path
        raise RuntimeError("openai package is not available")

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt},
    ]

    if hasattr(openai, "chat") and hasattr(openai.chat, "completions"):
        return openai.chat.completions.create(model=model, messages=messages, stream=True)

    if hasattr(openai, "ChatCompletion"):
        return openai.ChatCompletion.create(model=model, messages=messages, stream=True)

    raise RuntimeError("No compatible chat completion interface found")


def _extract_token(chunk: object) -> str:
    choice = getattr(chunk, "choices", None) or chunk.get("choices")  # type: ignore[union-attr]
    if not choice:
        return ""

    delta = choice[0].get("delta") if isinstance(choice[0], dict) else getattr(choice[0], "delta", None)
    if not delta:
        return ""

    content = delta.get("content") if isinstance(delta, dict) else getattr(delta, "content", None)
    return content or ""


def measure_latency(prompt: str, *, model: str = "gpt-4o-mini") -> LatencyMetrics:
    t_start = time.perf_counter()
    timestamps: List[float] = []

    for chunk in _stream_chat(prompt, model):
        now = time.perf_counter()
        token = _extract_token(chunk)
        if token:
            timestamps.append(now)
            print(token, end="", flush=True)

    print()

    metrics = compute_metrics(t_start, timestamps)
    print(metrics)
    return metrics


if __name__ == "__main__":
    prompt = sys.argv[1] if len(sys.argv) > 1 else "What is the capital of France?"
    metrics = measure_latency(prompt)

    print(f"Time to first token: {metrics.ttft:.3f}s")
    print(f"Average time between tokens: {metrics.tbt:.3f}s")
    print(f"Token velocity: {metrics.velocity:.2f} tokens/s")
    print(f"Total latency: {metrics.total_latency:.3f}s")
    print(f"Token count: {metrics.token_count}")
