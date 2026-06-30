import os
import time
import threading
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()


class _RateLimiter:
    """
    Thread-safe rate limiter for Gemini API calls.
    """

    def __init__(self, min_interval: float = 1.0):
        self._lock = threading.Lock()
        self._last_call = 0.0
        self._min_interval = min_interval

    def wait(self):
        with self._lock:
            elapsed = time.monotonic() - self._last_call
            if elapsed < self._min_interval:
                time.sleep(self._min_interval - elapsed)
            self._last_call = time.monotonic()


_limiter = _RateLimiter(min_interval=1.0)


def _sanitize(value) -> int:
    """
    Converts input to safe integer.
    """
    try:
        return max(0, min(int(float(str(value))), 10_000_000))
    except (ValueError, TypeError):
        return 0


def _call_gemini(prompt: str) -> str:
    """
    Calls Gemini API safely.
    """

    _limiter.wait()

    client = genai.Client(
        api_key=os.getenv("GEMINI_API_KEY")
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt[:500],
        config=types.GenerateContentConfig(
            max_output_tokens=1000
        ),
    )

    # FIX 1 → removed html.escape()
    return response.text.strip()


def get_recovery_advice(income, debt, expenses) -> str:
    """
    Financial recovery advice.
    """

    prompt = (
        "You are a professional financial advisor. "
        f"Client income is ${_sanitize(income)}, "
        f"debt is ${_sanitize(debt)}, "
        f"expenses are ${_sanitize(expenses)}. "
        "Give financial recovery advice in exactly 2 sentences. "
        "Be direct and encouraging."
    )

    try:
        return _call_gemini(prompt)

    except Exception as e:
        print("RECOVERY ERROR:", e)

        return (
            "Reduce unnecessary spending and focus on clearing debt first. "
            "Create a monthly repayment plan to improve financial stability."
        )


def get_negotiation_strategy(income, debt, expenses) -> str:
    """
    Debt negotiation advice.
    """

    prompt = (
        "You are a debt negotiation expert. "
        f"Client income is ${_sanitize(income)}, "
        f"debt is ${_sanitize(debt)}, "
        f"expenses are ${_sanitize(expenses)}. "
        "Give debt negotiation strategy in exactly 2 sentences. "
        "Be realistic and specific."
    )

    try:
        return _call_gemini(prompt)

    except Exception as e:
        print("NEGOTIATION ERROR:", e)

        return (
            "Contact creditors and request lower interest rates or settlement options. "
            "Negotiate a repayment schedule that matches your monthly budget."
        )


def get_ai_advice(income, debt, expenses) -> str:
    """
    Combines both advice outputs.
    """

    recovery = get_recovery_advice(income, debt, expenses)
    negotiation = get_negotiation_strategy(income, debt, expenses)

    # FIX 2 → removed html.escape()
    return f"{recovery}\n\n{negotiation}"