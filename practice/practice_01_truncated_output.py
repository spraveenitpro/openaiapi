"""
Scenario
--------
Customer: "The summary cuts off halfway through!"
Focus: Token budgeting, finish_reason, `max_tokens`.
Debug Path: Inspect `response.choices[0].finish_reason`, adjust `max_tokens`,
            and surface a gentle explanation about context limits.
"""

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()


def reproduce_issue() -> None:
    """Mimics the customer request that truncates due to an aggressive max_tokens."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Summarize this meeting in detail."},
            {
                "role": "user",
                "content": (
                    "The team discussed quarterly goals, revenue targets, hiring plans, "
                    "partnership risks, migration blockers, and product launches."
                ),
            },
        ],
        max_completion_tokens=500,  # Intentional bug: budget is too small for a full summary
    )
    print("finish_reason:", response.choices[0].finish_reason)
    print("partial_summary:", response.choices[0].message.content)
    print(
        "Coaching Tip: increase max_tokens or trim input to avoid finish_reason=='length'."
    )


if __name__ == "__main__":
    reproduce_issue()
