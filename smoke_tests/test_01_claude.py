"""
Smoke Test 1: Claude API
- Ruft Claude mit minimalem Prompt auf
- Kosten: <$0.01
"""
from _helpers import require, ok, fail


def main():
    api_key = require("ANTHROPIC_API_KEY")

    try:
        from anthropic import Anthropic
    except ImportError:
        fail("anthropic SDK not installed", ImportError("pip install -r requirements.txt"))

    try:
        client = Anthropic(api_key=api_key)
        resp = client.messages.create(
            model="claude-opus-4-7",
            max_tokens=50,
            messages=[{"role": "user", "content": "Antworte nur mit dem Wort 'OK'."}],
        )
        text = resp.content[0].text.strip()
        ok(f"Claude API erreichbar. Antwort: '{text}'")
        ok(f"Input tokens: {resp.usage.input_tokens}, Output: {resp.usage.output_tokens}")
    except Exception as e:
        fail("Claude API call failed", e)


if __name__ == "__main__":
    main()
