# agent_test.py
import os
import time
import json
from pathlib import Path
from typing import Optional

import requests
from dotenv import load_dotenv

# --------- Load env (.env must be next to this file) ----------
ENV_PATH = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=ENV_PATH)

FORCED = (os.getenv("PROVIDER") or "").strip().lower()

# Groq
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()
GROQ_MODEL   = os.getenv("GROQ_MODEL", "mixtral-8x7b-32768").strip()
GROQ_URL     = "https://api.groq.com/openai/v1/chat/completions"

# Hugging Face
HF_TOKEN = os.getenv("HF_TOKEN", "").strip()
HF_MODEL = os.getenv("HF_MODEL", "gpt2").strip()
HF_URL   = f"https://api-inference.huggingface.co/models/{HF_MODEL}"

# Ollama
OLLAMA_HOST  = (os.getenv("OLLAMA_HOST") or "http://localhost:11434").rstrip("/")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral").strip()
OLLAMA_GEN_URL = f"{OLLAMA_HOST}/api/generate"
OLLAMA_TAGS_URL = f"{OLLAMA_HOST}/api/tags"

JSON = {"Content-Type": "application/json"}


# ---------------- Providers ----------------
def call_groq(prompt: str) -> Optional[str]:
    if not GROQ_API_KEY:
        return None
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", **JSON}
    data = {
        "model": GROQ_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.6,
    }
    r = requests.post(GROQ_URL, headers=headers, json=data, timeout=60)
    if r.status_code != 200:
        raise RuntimeError(f"Groq {r.status_code}: {r.text[:200]}")
    js = r.json()
    return js["choices"][0]["message"]["content"]


def call_hf(prompt: str, retries: int = 6) -> Optional[str]:
    if not HF_TOKEN:
        return None
    headers = {"Authorization": f"Bearer {HF_TOKEN}", **JSON}
    payload = {"inputs": prompt, "parameters": {"max_new_tokens": 128}}
    for i in range(retries):
        r = requests.post(HF_URL, headers=headers, json=payload, timeout=60)
        if r.status_code == 200:
            data = r.json()
            # Common HF text-gen response: list of dicts with "generated_text"
            if isinstance(data, list) and data and isinstance(data[0], dict):
                return data[0].get("generated_text") or json.dumps(data)
            return json.dumps(data)
        if r.status_code in (503, 524):
            # model is loading; wait and retry
            time.sleep(2 + i)
            continue
        raise RuntimeError(f"HF {r.status_code}: {r.text[:200]}")
    raise RuntimeError("HF model still loading/unavailable after retries.")


def call_ollama(prompt: str) -> Optional[str]:
    # Check server is up
    try:
        tags = requests.get(OLLAMA_TAGS_URL, timeout=5)
        if tags.status_code != 200:
            return None
    except Exception:
        return None

    payload = {"model": OLLAMA_MODEL, "prompt": prompt, "stream": False}
    r = requests.post(OLLAMA_GEN_URL, headers=JSON, json=payload, timeout=120)
    if r.status_code != 200:
        raise RuntimeError(f"Ollama {r.status_code}: {r.text[:200]}")
    return r.json().get("response")


# ---------------- Router ----------------
def choose_order() -> list[str]:
    if FORCED in ("groq", "hf", "ollama"):
        return [FORCED]
    order = []
    if GROQ_API_KEY:
        order.append("groq")
    if HF_TOKEN:
        order.append("hf")
    order.append("ollama")  # last fallback (local)
    return order


def run(prompt: str) -> str:
    last_err = None
    for provider in choose_order():
        try:
            if provider == "groq":
                out = call_groq(prompt)
            elif provider == "hf":
                out = call_hf(prompt)
            else:
                out = call_ollama(prompt)

            if out:
                print(f"\n--- Used provider: {provider.upper()} ---\n")
                return out.strip()
        except Exception as e:
            last_err = e
            print(f"[{provider}] failed: {e}")
    raise RuntimeError(f"All providers failed. Last error: {last_err}")


# ---------------- CLI ----------------
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Try Groq / HF / Ollama with one script.")
    parser.add_argument(
        "--prompt",
        default="Give me three money-making agentic AI micro-SaaS ideas for e-commerce.",
    )
    args = parser.parse_args()

    print(run(args.prompt))
