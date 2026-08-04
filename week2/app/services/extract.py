from __future__ import annotations

import json
import os
import re
from typing import Any, List

from dotenv import load_dotenv
from ollama import chat

load_dotenv()

BULLET_PREFIX_PATTERN = re.compile(r"^\s*([-*•]|\d+\.)\s+")
KEYWORD_PREFIXES = (
    "todo:",
    "action:",
    "next:",
)
GROQ_API_KEY = (
    os.getenv("GROQ_API_KEY")
    or os.getenv("Groq-api-key")
    or os.getenv("groq-api-key")
    or os.getenv("GROQ_APIKEY")
)
GROQ_MODEL = os.getenv("GROQ_MODEL", os.getenv("Groq-model", "llama-3.1-8b-instant"))
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:8b")


def _is_action_line(line: str) -> bool:
    stripped = line.strip().lower()
    if not stripped:
        return False
    if BULLET_PREFIX_PATTERN.match(stripped):
        return True
    if any(stripped.startswith(prefix) for prefix in KEYWORD_PREFIXES):
        return True
    if "[ ]" in stripped or "[todo]" in stripped:
        return True
    return False


def _clean_item_text(item: str) -> str:
    cleaned = str(item).strip()
    cleaned = cleaned.removeprefix("[ ]").strip()
    cleaned = cleaned.removeprefix("[todo]").strip()
    cleaned = cleaned.removeprefix("todo:").strip()
    cleaned = cleaned.removeprefix("action:").strip()
    cleaned = cleaned.removeprefix("next:").strip()
    return cleaned.strip()


def _deduplicate(items: List[str]) -> List[str]:
    seen: set[str] = set()
    unique: List[str] = []
    for item in items:
        cleaned = _clean_item_text(item)
        if not cleaned:
            continue
        lowered = cleaned.lower()
        if lowered in seen:
            continue
        seen.add(lowered)
        unique.append(cleaned)
    return unique


def extract_action_items(text: str) -> List[str]:
    lines = text.splitlines()
    extracted: List[str] = []
    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue
        if _is_action_line(line):
            cleaned = BULLET_PREFIX_PATTERN.sub("", line)
            extracted.append(_clean_item_text(cleaned))
    if not extracted:
        sentences = re.split(r"(?<=[.!?])\s+", text.strip())
        for sentence in sentences:
            s = sentence.strip()
            if not s:
                continue
            if _looks_imperative(s):
                extracted.append(s)
    return _deduplicate(extracted)


def _extract_with_groq(text: str) -> List[str]:
    from openai import OpenAI

    client = OpenAI(api_key=GROQ_API_KEY, base_url="https://api.groq.com/openai/v1")
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You extract action items from notes. Return only a JSON array of strings. "
                    "Do not include commentary, markdown, or explanations."
                ),
            },
            {"role": "user", "content": text},
        ],
        response_format={"type": "json_object"},
        temperature=0,
    )
    content = response.choices[0].message.content
    payload = json.loads(content)
    if isinstance(payload, dict):
        payload = payload.get("items", payload.get("result", []))
    if isinstance(payload, list):
        return _deduplicate([str(item) for item in payload])
    raise ValueError("Unexpected response format from Groq")


def _extract_with_ollama(text: str) -> List[str]:
    response = chat(
        model=OLLAMA_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You extract action items from notes. Return only a JSON array of strings. "
                    "Do not include commentary, markdown, or explanations."
                ),
            },
            {"role": "user", "content": text},
        ],
        format="json",
    )
    content = getattr(response, "message", None)
    if content is None:
        raise RuntimeError("Missing response message from Ollama")
    payload = json.loads(content.content)
    if isinstance(payload, list):
        return _deduplicate([str(item) for item in payload])
    raise ValueError("Unexpected response format from Ollama")


def extract_action_items_llm(text: str) -> List[str]:
    cleaned_text = (text or "").strip()
    if not cleaned_text:
        return []

    try:
        if GROQ_API_KEY:
            return _extract_with_groq(cleaned_text)
    except Exception:
        pass

    try:
        return _extract_with_ollama(cleaned_text)
    except Exception:
        return extract_action_items(cleaned_text)


def _looks_imperative(sentence: str) -> bool:
    words = re.findall(r"[A-Za-z']+", sentence)
    if not words:
        return False
    first = words[0]
    imperative_starters = {
        "add",
        "create",
        "implement",
        "fix",
        "update",
        "write",
        "check",
        "verify",
        "refactor",
        "document",
        "design",
        "investigate",
    }
    return first.lower() in imperative_starters
