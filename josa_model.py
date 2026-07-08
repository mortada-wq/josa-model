"""Utilities for selecting common Korean josa pairs."""

from __future__ import annotations

from typing import Iterable

_HANGUL_BASE = 0xAC00
_HANGUL_LAST = 0xD7A3
_JONGSEONG_COUNT = 28
_RIEUL_JONGSEONG = 8
_SUPPORTED_PAIRS = {
    ("은", "는"),
    ("이", "가"),
    ("을", "를"),
    ("과", "와"),
    ("으로", "로"),
}


def _normalize_pair(pair: str | Iterable[str]) -> tuple[str, str]:
    if isinstance(pair, str):
        if "/" not in pair:
            raise ValueError("pair must include '/' between the two josa forms")
        first, second = (part.strip() for part in pair.split("/", 1))
    else:
        first, second = tuple(pair)

    normalized = (first, second)
    if normalized not in _SUPPORTED_PAIRS:
        raise ValueError(f"unsupported josa pair: {first}/{second}")

    return normalized


def _last_relevant_char(text: str) -> str:
    for character in reversed(text.strip()):
        if character.isalnum() or _HANGUL_BASE <= ord(character) <= _HANGUL_LAST:
            return character
    raise ValueError("text must contain at least one letter, number, or Hangul syllable")


def _jongseong_index(character: str) -> int | None:
    code_point = ord(character)
    if _HANGUL_BASE <= code_point <= _HANGUL_LAST:
        return (code_point - _HANGUL_BASE) % _JONGSEONG_COUNT
    return None


def has_batchim(text: str) -> bool:
    """Return True when the last relevant Hangul syllable ends with a batchim."""

    jongseong = _jongseong_index(_last_relevant_char(text))
    return bool(jongseong)


def pick_josa(text: str, pair: str | Iterable[str]) -> str:
    """Choose the correct josa for *text* from a supported pair."""

    first, second = _normalize_pair(pair)
    last_char = _last_relevant_char(text)
    jongseong = _jongseong_index(last_char)

    if jongseong is None:
        return second

    if (first, second) == ("으로", "로"):
        return second if jongseong in (0, _RIEUL_JONGSEONG) else first

    return first if jongseong else second


def select_josa(text: str, pair: str | Iterable[str]) -> str:
    """Alias for :func:`pick_josa`."""

    return pick_josa(text, pair)


def append_josa(text: str, pair: str | Iterable[str]) -> str:
    """Append the selected josa to *text*."""

    return f"{text}{pick_josa(text, pair)}"


def attach_josa(text: str, pair: str | Iterable[str]) -> str:
    """Alias for :func:`append_josa`."""

    return append_josa(text, pair)
