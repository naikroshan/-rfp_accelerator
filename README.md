# rfp_accelerator

Automated Application Security RFP response generation using a Git repository.

## Included assets

- `prompts/openai_codex_master_prompt_appsec_compliance.md`:
  A production-grade master prompt for AppSec presales RFP automation spanning:
  - Sonatype Nexus Lifecycle + SBOM
  - OpenText Fortify (SAST, DAST, SCA/DeBricked, Aviator, SSC, FoD)
  - Compliance-heavy personas for India and Sri Lanka (BFSI, public sector, private)
  - Audit- and compliance-oriented response guardrails

## Usage

Use the prompt file as a system/authoring template for:

1. Building a FastAPI or Express-based RFP automation backend.
2. Structuring RAG-based response generation with strict grounding.
3. Generating compliance traceability outputs for presales and audit reviews.
