from __future__ import annotations

import runpod

from josa_model import JosaModel


model = JosaModel()


def handler(job: dict) -> dict:
    payload = job.get("input", {})
    word = payload.get("word", "")
    pair = payload.get("pair", ["은", "는"])

    result = model.predict(word, pair)
    return {
        "word": result.word,
        "selected_josa": result.selected_josa,
        "pair": list(result.pair),
        "combined_text": result.combined_text,
        "has_batchim": result.has_batchim,
    }


if __name__ == "__main__":
    runpod.serverless.start({"handler": handler})
