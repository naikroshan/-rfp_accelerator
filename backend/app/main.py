from __future__ import annotations

import csv
import io
from dataclasses import dataclass
from typing import Any

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="AppSec RFP Automation API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@dataclass
class ClassificationRule:
    keyword: str
    category: str


RULES: list[ClassificationRule] = [
    ClassificationRule(keyword="sbom", category="SBOM"),
    ClassificationRule(keyword="sast", category="SAST"),
    ClassificationRule(keyword="dast", category="DAST"),
    ClassificationRule(keyword="dependency", category="SCA"),
    ClassificationRule(keyword="open source", category="SCA"),
    ClassificationRule(keyword="software composition", category="SCA"),
]


def classify_question(question: str) -> str:
    normalized = question.lower()
    for rule in RULES:
        if rule.keyword in normalized:
            return rule.category
    return "Unknown"


def compliance_mapping(category: str) -> dict[str, str]:
    mappings = {
        "SAST": {
            "RBI": "Supports secure SDLC controls via early code-level vulnerability identification.",
            "ISO27001": "Aligns with secure development and vulnerability management practices.",
            "OWASP": "Addresses OWASP Top 10 classes through static analysis findings.",
        },
        "DAST": {
            "RBI": "Supports runtime vulnerability assessment for internet-facing applications.",
            "ISO27001": "Strengthens security testing and vulnerability remediation workflows.",
            "OWASP": "Identifies exploitable web vulnerabilities aligned to OWASP Top 10.",
        },
        "SCA": {
            "RBI": "Improves supply-chain risk visibility across third-party and open-source components.",
            "ISO27001": "Supports asset risk treatment and dependency governance controls.",
            "OWASP": "Covers dependency-related risks and known vulnerable components.",
        },
        "SBOM": {
            "RBI": "Supports software supply-chain transparency and governance expectations.",
            "ISO27001": "Enables asset inventory integrity and risk-informed control selection.",
            "OWASP": "Strengthens dependency risk management and vulnerability visibility.",
        },
    }
    return mappings.get(
        category,
        {
            "RBI": "This capability is not explicitly documented",
            "ISO27001": "This capability is not explicitly documented",
            "OWASP": "This capability is not explicitly documented",
        },
    )


def generate_answer(category: str) -> tuple[str, int]:
    responses: dict[str, tuple[str, int]] = {
        "SAST": (
            "Fortify Static Code Analyzer provides SAST by analyzing source code early in the SDLC, enabling developers to remediate vulnerabilities before deployment.",
            94,
        ),
        "DAST": (
            "Fortify WebInspect and Fortify on Demand support DAST by testing running applications to identify exploitable vulnerabilities.",
            93,
        ),
        "SCA": (
            "Sonatype Nexus Lifecycle provides software composition analysis for open-source vulnerability and license risk management, with policy-driven governance.",
            95,
        ),
        "SBOM": (
            "Sonatype SBOM capabilities support CycloneDX and SPDX-based software bill of materials workflows for supply-chain visibility and continuous monitoring.",
            95,
        ),
    }
    return responses.get(category, ("This capability is not explicitly documented", 60))


def process_question(question: str) -> dict[str, Any]:
    category = classify_question(question)
    answer, confidence = generate_answer(category)
    return {
        "question": question,
        "category": category,
        "answer": answer,
        "compliance": compliance_mapping(category),
        "confidence": confidence,
    }


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

    reader = csv.DictReader(io.StringIO(decoded))
    if not reader.fieldnames or "question" not in [h.strip().lower() for h in reader.fieldnames if h]:
        raise HTTPException(status_code=400, detail="CSV must include a 'question' column")

    results: list[dict[str, Any]] = []
    for row in reader:
        question_value = row.get("question") or row.get("Question")
        if not question_value:
            continue
        results.append(process_question(question_value.strip()))

    return {"count": len(results), "results": results}
