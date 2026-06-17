"""
teacher.py
Connectors for "teacher" models used as the knowledge source for distillation.
"""
from __future__ import annotations

import hashlib
import json
import logging
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterator, Optional

logger = logging.getLogger(__name__)

try:
    import anthropic
except ImportError:
    anthropic = None

try:
    import openai
except ImportError:
    openai = None

import requests


class RateLimiter:
    """Very small token-bucket rate limiter."""

    def __init__(self, requests_per_minute: int = 50):
        self.capacity = max(1, requests_per_minute)
        self.tokens = float(self.capacity)
        self.updated_at = time.monotonic()

    def acquire(self) -> None:
        now = time.monotonic()
        elapsed = now - self.updated_at
        refill = elapsed * (self.capacity / 60.0)
        self.tokens = min(float(self.capacity), self.tokens + refill)
        self.updated_at = now
        if self.tokens < 1:
            wait = (1 - self.tokens) * (60.0 / self.capacity)
            logger.debug("Rate limit reached, sleeping %.2fs", wait)
            time.sleep(wait)
            self.tokens = 0.0
        else:
            self.tokens -= 1


class ResponseCache:
    """Tiny JSON-file cache keyed by a hash of (provider, model, prompt, params)."""

    def __init__(self, cache_dir: str | Path = "./cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _key(self, payload: dict[str, Any]) -> str:
        blob = json.dumps(payload, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(blob.encode("utf-8")).hexdigest()

    def get(self, payload: dict[str, Any]) -> Optional[str]:
        path = self.cache_dir / f"{self._key(payload)}.json"
        if path.exists():
            try:
                return json.loads(path.read_text(encoding="utf-8"))["response"]
            except Exception:
                return None
        return None

    def set(self, payload: dict[str, Any], response: str) -> None:
        path = self.cache_dir / f"{self._key(payload)}.json"
        path.write_text(json.dumps({"response": response}, ensure_ascii=False), encoding="utf-8")


@dataclass
class TeacherConfig:
    provider: str = "anthropic"          # anthropic | openai | ollama
    model: str = "claude-3-5-sonnet-20241022"
    temperature: float = 0.7
    max_tokens: int = 1024
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    requests_per_minute: int = 50
    cache_dir: str = "./cache"
    use_cache: bool = True


class TeacherConnector:
    """Unified interface to query a teacher model from several providers."""

    def __init__(self, config: TeacherConfig | None = None, **overrides: Any):
        self.config = config or TeacherConfig()
        for key, value in overrides.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)

        self._limiter = RateLimiter(self.config.requests_per_minute)
        self._cache = ResponseCache(self.config.cache_dir) if self.config.use_cache else None
        self._client = self._build_client()

    def _build_client(self):
        provider = self.config.provider
        if provider == "anthropic":
            if anthropic is None:
                raise ImportError("anthropic package is required for provider='anthropic'")
            return anthropic.Anthropic(api_key=self.config.api_key)
        if provider == "openai":
            if openai is None:
                raise ImportError("openai package is required for provider='openai'")
            return openai.OpenAI(api_key=self.config.api_key, base_url=self.config.base_url)
        if provider == "ollama":
            return None
        raise ValueError(f"Unknown provider: {provider}")

    def complete(self, prompt: str, system: Optional[str] = None, **kwargs: Any) -> str:
        """Send a single prompt to the teacher and return the text response."""
        payload = {
            "provider": self.config.provider,
            "model": self.config.model,
            "system": system,
            "prompt": prompt,
            "temperature": kwargs.get("temperature", self.config.temperature),
            "max_tokens": kwargs.get("max_tokens", self.config.max_tokens),
        }

        if self._cache is not None:
            cached = self._cache.get(payload)
            if cached is not None:
                logger.debug("Cache hit for prompt")
                return cached

        self._limiter.acquire()

        if self.config.provider == "anthropic":
            response = self._complete_anthropic(payload, system)
        elif self.config.provider == "openai":
            response = self._complete_openai(payload, system)
        elif self.config.provider == "ollama":
            response = self._complete_ollama(payload, system)
        else:
            raise ValueError(f"Unknown provider: {self.config.provider}")

        if self._cache is not None:
            self._cache.set(payload, response)
        return response

    def _complete_anthropic(self, payload: dict[str, Any], system: Optional[str]) -> str:
        message = self._client.messages.create(
            model=self.config.model,
            max_tokens=payload["max_tokens"],
            temperature=payload["temperature"],
            system=system or "",
            messages=[{"role": "user", "content": payload["prompt"]}],
        )
        return "".join(
            block.text for block in message.content if getattr(block, "type", None) == "text"
        )

    def _complete_openai(self, payload: dict[str, Any], system: Optional[str]) -> str:
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": payload["prompt"]})
        completion = self._client.chat.completions.create(
            model=self.config.model,
            messages=messages,
            temperature=payload["temperature"],
            max_tokens=payload["max_tokens"],
        )
        return completion.choices[0].message.content or ""

    def _complete_ollama(self, payload: dict[str, Any], system: Optional[str]) -> str:
        url = (self.config.base_url or "http://localhost:11434") + "/api/generate"
        body = {
            "model": self.config.model,
            "prompt": payload["prompt"],
            "system": system or "",
            "stream": False,
            "options": {"temperature": payload["temperature"]},
        }
        resp = requests.post(url, json=body, timeout=120)
        resp.raise_for_status()
        return resp.json().get("response", "")

    def stream(self, prompt: str, system: Optional[str] = None, **kwargs: Any) -> Iterator[str]:
        """Yield response chunks as they arrive (Anthropic & OpenAI only)."""
        self._limiter.acquire()
        if self.config.provider == "anthropic":
            with self._client.messages.stream(
                model=self.config.model,
                max_tokens=kwargs.get("max_tokens", self.config.max_tokens),
                temperature=kwargs.get("temperature", self.config.temperature),
                system=system or "",
                messages=[{"role": "user", "content": prompt}],
            ) as stream:
                for text in stream.text_stream:
                    yield text
        elif self.config.provider == "openai":
            messages = []
            if system:
                messages.append({"role": "system", "content": system})
            messages.append({"role": "user", "content": prompt})
            stream = self._client.chat.completions.create(
                model=self.config.model,
                messages=messages,
                temperature=kwargs.get("temperature", self.config.temperature),
                max_tokens=kwargs.get("max_tokens", self.config.max_tokens),
                stream=True,
            )
            for chunk in stream:
                delta = chunk.choices[0].delta.content
                if delta:
                    yield delta
        else:
            yield self.complete(prompt, system=system, **kwargs)
