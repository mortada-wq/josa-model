from __future__ import annotations

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from josa_model import JosaModel


class PredictRequest(BaseModel):
    word: str = Field(..., min_length=1, description="Input word")
    pair: list[str] = Field(default_factory=lambda: ["은", "는"], min_length=2, max_length=2)


class PredictResponse(BaseModel):
    word: str
    selected_josa: str
    pair: list[str]
    combined_text: str
    has_batchim: bool


app = FastAPI(title="Josa Model API", version="1.0.0")
model = JosaModel()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest) -> PredictResponse:
    try:
        result = model.predict(request.word, request.pair)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return PredictResponse(
        word=result.word,
        selected_josa=result.selected_josa,
        pair=list(result.pair),
        combined_text=result.combined_text,
        has_batchim=result.has_batchim,
    )
