from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence


HANGUL_BASE = 0xAC00
HANGUL_LAST = 0xD7A3


@dataclass(frozen=True)
class PredictionResult:
    word: str
    selected_josa: str
    pair: tuple[str, str]
    combined_text: str
    has_batchim: bool


class JosaModel:
    """Selects the correct Korean josa for a given word and josa pair."""

    def predict(self, word: str, pair: Sequence[str] | None = None) -> PredictionResult:
        normalized_word = (word or "").strip()
        if not normalized_word:
            raise ValueError("word must be a non-empty string")

        validated_pair = self._validate_pair(pair or ("은", "는"))
        has_batchim = self._has_batchim(normalized_word[-1])
        selected = validated_pair[0] if has_batchim else validated_pair[1]

        return PredictionResult(
            word=normalized_word,
            selected_josa=selected,
            pair=validated_pair,
            combined_text=f"{normalized_word}{selected}",
            has_batchim=has_batchim,
        )

    @staticmethod
    def _validate_pair(pair: Sequence[str]) -> tuple[str, str]:
        if len(pair) != 2:
            raise ValueError("pair must contain exactly 2 josa options")
        first = (pair[0] or "").strip()
        second = (pair[1] or "").strip()
        if not first or not second:
            raise ValueError("pair values must be non-empty strings")
        return first, second

    @staticmethod
    def _has_batchim(char: str) -> bool:
        code = ord(char)
        if HANGUL_BASE <= code <= HANGUL_LAST:
            jongseong = (code - HANGUL_BASE) % 28
            return jongseong != 0
        return False
