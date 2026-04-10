# rfp_accelerator

AI-assisted AppSec RFP automation MVP for Fortify + Sonatype with compliance-aligned output.

## What is included

- **Backend (FastAPI)**: CSV upload, keyword classification (SAST/DAST/SCA/SBOM), answer generation, and compliance mapping.
- **Frontend (React + Vite)**: CSV upload UI, results table, confidence display, and CSV export.
- **Deployment artifacts**: Dockerfiles for backend/frontend and `docker-compose.yml`.
- **Sample dataset**: `data/sample_questions.csv`.
- **Master prompt asset**: `prompts/openai_codex_master_prompt_appsec_compliance.md`.

## Project structure

- `backend/app/main.py` – API endpoints and processing pipeline.
- `backend/requirements.txt` – Python dependencies.
- `backend/Dockerfile` – backend container build.
- `frontend/src/App.jsx` – Upload flow and results rendering.
- `frontend/src/api.js` – Axios API client.
- `frontend/src/styles.css` – Basic UI styling.
- `frontend/Dockerfile` – frontend container build.
- `frontend/nginx.conf` – static app serving config.
- `docker-compose.yml` – multi-service deployment.
- `data/sample_questions.csv` – Demo questions.

## Run locally (without Docker)

### 1) Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Health check:

```bash
curl http://localhost:8000/health
```

### 2) Frontend

```bash
cd frontend
npm install
npm run dev
```

Open the URL shown by Vite (usually `http://localhost:5173`).

## Deploy with Docker Compose

```bash
docker compose up --build -d
```

- Frontend: `http://localhost:5173`
- Backend API: `http://localhost:8000`

Stop deployment:

```bash
docker compose down
```

## CSV format

Upload a CSV with a required `question` column:

```csv
question
Does your solution support SBOM generation?
Do you provide SAST capabilities?
How do you manage open source vulnerabilities?
Do you support DAST testing?
```

## API contract

### `POST /upload`

- **Input**: multipart/form-data with a CSV file.
- **Output**:

```json
{
  "count": 1,
  "results": [
    {
      "question": "Does your solution support SBOM generation?",
      "category": "SBOM",
      "answer": "...",
      "compliance": {
        "RBI": "...",
        "ISO27001": "...",
        "OWASP": "..."
      },
      "confidence": 95
    }
  ]
}
```

## Notes and guardrails

- This MVP uses deterministic keyword rules for classification.
- Unknown capability requests return: **"This capability is not explicitly documented"**.
- Answers are constrained to the scoped Fortify/Sonatype capabilities in this repository's prompt and code.
