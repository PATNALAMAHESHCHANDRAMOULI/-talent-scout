# Talent Scout — AI-Powered Candidate Matching Agent

Paste a job description → get ranked candidates with match scores, simulated outreach, and engagement signals.

No ML models. No API keys. Just regex, scoring rules, and a clean UI.

## Quick Start

```bash
cd talent_agent
pip install -r requirements.txt
uvicorn main:app --reload
```

Open [http://localhost:8000](http://localhost:8000) in your browser.

## API

**POST /analyze** — parse a JD and return ranked candidates

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"jd_text": "We need a senior Python developer with 5+ years..."}'
```

**GET /candidates** — return raw candidate list

```bash
curl http://localhost:8000/candidates
```

## How Scoring Works

| Component          | Max Points | How                                                    |
|--------------------|-----------|--------------------------------------------------------|
| Required skills    | 50        | matched / total × 50                                  |
| Preferred skills   | 15        | matched / total × 15 (0 if none in JD)               |
| Experience fit     | 20        | meets = 20, within 1yr = 10, below = 0               |
| Availability       | 10        | immediate = 10, 2 weeks = 7, 1 month = 4             |
| Recency            | 5         | ≤7 days = 5, ≤30 days = 3, older = 0                 |

**Final Score** = (Match Score × 0.6) + (Interest Score × 0.4)

Interest score comes from simulated outreach replies classified as high (85), medium (50), or low (15).

## Sample JD

```
We're looking for a Senior Backend Engineer to join our platform team.
You'll own core API development and help us scale to 10M users.

Requirements:
  - 4+ years of backend engineering experience
  - Strong Python skills (FastAPI or Django)
  - PostgreSQL — you should be able to write a join without Googling it
  - Experience with REST API design
  - Comfortable working in a remote-first team

Nice to have:
  - Kubernetes or Docker in production
  - Redis caching experience
  - Prior startup experience
  - Familiarity with event-driven systems

We're based in Berlin but fully remote. Competitive salary, async culture.
```

## Project Structure

```
talent_agent/
├── main.py              ← FastAPI app, routes, startup
├── jd_parser.py         ← extracts skills/role/exp from raw JD text
├── matcher.py           ← scores candidates against parsed JD
├── conversation.py      ← simulates outreach + reply classification
├── ranker.py            ← merges scores, sorts, builds output
├── data/
│   └── candidates.py    ← mock candidate profiles (list of dicts)
├── static/
│   └── index.html       ← UI: paste JD → click → see ranked list
├── requirements.txt
└── README.md
```

## Stack

- **Backend**: FastAPI + Uvicorn
- **Frontend**: Single HTML file, vanilla JS, no build step
- **ML**: None. All logic is deterministic regex + scoring rules.

Built for a hackathon. Ships on a laptop.
