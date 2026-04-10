from __future__ import annotations

from typing import Any

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from app.domain import parse_questions_csv, process_question

app = FastAPI(title="AppSec RFP Automation API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/upload")
async def upload(file: UploadFile = File(...)) -> dict[str, Any]:
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV uploads are supported")

    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="CSV file is empty")

    try:
        decoded = content.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise HTTPException(status_code=400, detail="CSV must be UTF-8 encoded") from exc

    questions = parse_questions_csv(decoded)
    if not questions:
        raise HTTPException(status_code=400, detail="CSV must include a 'question' column")

    results = [process_question(question) for question in questions]
    return {"count": len(results), "results": results}
