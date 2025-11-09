# Repository Guidelines

## Project Structure & Module Organization
- `chatcompletion/`: primary Python package with reusable helpers (retry logic, rate-limit mitigation, schema validation). Treat this as the source of truth for production-grade agents.
- `response/`: HTTP-focused examples (`responses_with_file.py`, `simpleresponse.py`) that demonstrate streaming headers and payload shaping; keep experimental endpoints here.
- Root-level scripts (`retry_simple.py`, `tokens.py`, `test.py`) are runnable snippets; mirror this layout when adding new entry points.
- `practice/` is sandbox space for rapid prototyping—avoid importing from it in shipping code. House tests in `tests/`, matching the module path (`tests/chatcompletion/test_ratelimit.py`, etc.).

## Build, Test, and Development Commands
- `uv sync`: install Python 3.13 dependencies as locked in `uv.lock`.
- `uv run python chatcompletion/chatcompletions.py`: run the end-to-end chat completion example using the current virtual environment.
- `uv run python response/simpleresponse.py`: exercise the lightweight response API sample; useful for manual smoke checks.
- `uv run python -m pytest tests`: execute the test suite; add `-k <pattern>` for focused runs.

## Coding Style & Naming Conventions
- Follow PEP 8 with 4-space indentation, snake_case for functions/variables, PascalCase for Pydantic models, and SCREAMING_SNAKE_CASE for env-based constants (e.g., `OPENAI_API_KEY`).
- Prefer explicit type hints and `pydantic.BaseModel` schemas for every payload that crosses the network boundary.
- Keep modules focused (one major responsibility) and co-locate retry/backoff helpers under `chatcompletion/` rather than duplicating them.

## Testing Guidelines
- Use pytest; name files `test_<module>.py` and functions `test_<behavior>`.
- Stub OpenAI responses by injecting fixtures or lightweight adapters; never hit the real API in CI.
- Target high-level behaviors (rate-limit retries, streaming chunk assembly, token accounting). Fail tests if logging emits warnings.

## Commit & Pull Request Guidelines
- Match the concise, imperative history (`Add rate retry example`, `Add initial scaffold...`). Use one topic per commit and reference issues with `(#123)` when applicable.
- Pull requests should explain intent, describe validation (`uv run python ...`, `pytest`), and include screenshots or sample payloads for response-layer changes.
- Keep diffs small, request review for protocol changes, and link to any updated documentation (including this file).

## Security & Configuration Tips
- Store API keys in `.env`; load with `python-dotenv` as shown in existing scripts. Never commit secrets or personal tokens.
- When sharing command snippets, redact request/response bodies that may include customer data.
