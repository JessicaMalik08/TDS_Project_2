# LLM Analysis Quiz — Solver Service

## Overview
This project implements a Flask webhook `/api/quiz` that accepts POST requests with:
{
  "email": "your email",
  "secret": "your secret",
  "url": "https://example.com/quiz-834"
}

On receiving the request (and after verifying the secret), the service uses a Playwright-based solver
to visit the URL, extract the task, compute an answer and POST the answer to the submit URL included in the quiz page.

## Quick start (local)
1. Create and activate venv:
   python -m venv venv
   source venv/bin/activate   # or venv\\Scripts\\activate on Windows

2. Install deps:
   pip install -r requirements.txt
   playwright install

3. Set environment variable for secret:
   export QUIZ_SECRET="mysecret"    # Linux / macOS
   set QUIZ_SECRET=mysecret         # Windows CMD
   $env:QUIZ_SECRET="mysecret"      # PowerShell

4. Run the Flask service:
   python app.py

5. Test with the provided demo:
   curl -X POST "http://localhost:8080/api/quiz" -H "Content-Type: application/json" \
    -d '{"email":"you@example.com","secret":"mysecret","url":"https://tds-llm-analysis.s-anand.net/demo"}'

## Docker
Build:
  docker build -t llm-quiz:latest .

Run:
  docker run -e QUIZ_SECRET="mysecret" -p 8080:8080 llm-quiz:latest

## Notes
- The solver script enforces a time budget and attempts several heuristics (HTML tables, CSV, PDF parsing).
- Extend `quiz_solver.py` to include OCR, advanced parsing, LLM assistance, or domain-specific logic.
- Keep payloads under 1 MB when submitting answers.

