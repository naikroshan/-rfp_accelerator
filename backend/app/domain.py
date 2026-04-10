from __future__ import annotations

import csv
import io
from dataclasses import dataclass
from typing import Any


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


def parse_questions_csv(decoded_csv: str) -> list[str]:
    reader = csv.DictReader(io.StringIO(decoded_csv))
    if not reader.fieldnames:
        return []

    normalized_headers = [h.strip().lower() for h in reader.fieldnames if h]
    if "question" not in normalized_headers:
        return []

    questions: list[str] = []
    for row in reader:
        question_value = row.get("question") or row.get("Question")
        if question_value and question_value.strip():
            questions.append(question_value.strip())

    return questions
