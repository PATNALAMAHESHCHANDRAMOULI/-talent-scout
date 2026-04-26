<div align="center">

# Talent Scout

**Paste a job description. Get a ranked shortlist with scores you can actually explain.**

[![Live Demo](https://img.shields.io/badge/Live_Demo-talent--scout-5B4FE8?style=for-the-badge&logo=render&logoColor=white)](https://talent-scout-kfaa.onrender.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.135+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)

### **[→ talent-scout-kfaa.onrender.com](https://talent-scout-kfaa.onrender.com/)**

</div>

---

## What is Talent Scout?

Most recruitment tools either hide their logic behind ML models nobody audits, or dump raw keyword matches that miss the point entirely. Recruiters end up trusting scores they can't explain and rejecting candidates for reasons they can't articulate. The pipeline between "we need a backend engineer" and "here are your top 5" is a black box that everyone pretends is fine.

Talent Scout takes a different approach. You paste a raw job description, the system parses it for skills and requirements using regex-based extraction, scores each candidate on a transparent 100-point scale across five weighted components, simulates recruiter outreach and candidate replies, classifies interest levels, and returns a ranked shortlist. Every score has a breakdown. Every ranking has an explanation. Click any candidate card to open a detailed profile panel with a donut chart, skill grid, and a live chat simulator. The entire system is deterministic — same input, same output, every time.

## Live Demo

**[https://talent-scout-kfaa.onrender.com](https://talent-scout-kfaa.onrender.com/)**

Paste this sample JD and click **Find Candidates**:

```
We're looking for a Senior Backend Engineer.
Requirements: 4+ years Python, FastAPI or Django, PostgreSQL, REST API design, remote-first.
Nice to have: Kubernetes, Docker, Redis, prior startup experience.
```

## Features

| Feature                | What It Does                                                                                       |
|:-----------------------|:---------------------------------------------------------------------------------------------------|
| JD Parser              | Extracts required skills, preferred skills, experience threshold, role level, and location from raw text using regex and keyword matching |
| Match Scoring          | Scores each candidate on a 100-point scale across 5 components: skill overlap, experience fit, availability, and recency               |
| Interest Simulation    | Generates personalized recruiter outreach, simulates candidate replies, classifies interest as High/Medium/Low                          |
| Candidate Ranking      | Merges match and interest scores with configurable weights (60/40), sorts, and generates human-readable explanations                    |
| Profile Panel          | Click any card to open a slide-over with CSS donut chart, skill assessment grid with dot bars, verdict badge, and full outreach history |
| Recruiter Chat         | Real-time chat inside the profile panel — keyword-matched deterministic replies with typing indicator and quick-reply chips             |
| Zero Dependencies      | No ML models, no API keys, no database, no CSS framework, no build step. Two pip packages: `fastapi` and `uvicorn`                     |

## Scoring System

### Match Score (100 points)

| Component          | Max Points | Formula                                                        |
|:-------------------|:----------:|:---------------------------------------------------------------|
| Required Skills    |     50     | `matched / total × 50`                                        |
| Preferred Skills   |     15     | `matched / total × 15` (0 if JD lists none)                   |
| Experience Fit     |     20     | Meets bar = 20, within 1 year = 10, below = 0                 |
| Availability       |     10     | Immediate = 10, 2 weeks = 7, 1 month = 4                      |
| Recency            |      5     | Active ≤7 days = 5, ≤30 days = 3, older = 0                   |

### Interest Score (3 buckets)

| Level  | Score | Signal Keywords                                    |
|:-------|:-----:|:---------------------------------------------------|
| High   |  85   | "interested", "tell me more", "sounds good"        |
| Medium |  50   | "depends", "could work", "maybe"                   |
| Low    |  15   | "not looking", "pass", "no thanks"                 |

### Final Score

```
Final Score = (Match Score × 0.6) + (Interest Score × 0.4)
```

Three fixed buckets instead of a continuous score is intentional. False precision on simulated data is worse than honest approximation — a candidate either showed interest signals, was neutral, or wasn't interested. Pretending we can distinguish between 47% and 52% interest on generated replies would be dishonest.

## Architecture

```
Browser
  │
  ├── GET /           → static/index.html (full UI)
  │
  └── POST /analyze   → main.py
                          │
                          ├── jd_parser.py ──────── regex extraction
                          │                          (skills, experience, role level, location)
                          │
                          ├── matcher.py ─────────── 5-component scoring
                          │       ↑
                          │   candidates.py ──────── 12 mock profiles
                          │
                          ├── conversation.py ────── outreach + reply simulation + classification
                          │
                          └── ranker.py ─────────── merge scores, sort, explain
                                  │
                                  ▼
                            JSON response
                                  │
                                  ▼
                          UI renders ranked cards
                          (click → profile panel + chat)
```

## Project Structure

```
talent_agent/
├── main.py              # FastAPI app — 2 routes, CORS, static file serving
├── jd_parser.py         # Regex-based JD parser — skills, experience, role level, location
├── matcher.py           # 100-point scoring engine — 5 weighted components with full breakdown
├── conversation.py      # Outreach message generator + reply simulator + interest classifier
├── ranker.py            # Score merger, sorter, and human-readable explanation builder
├── data/
│   └── candidates.py    # 12 mock candidate profiles with skills, experience, salary, location
├── static/
│   └── index.html       # Complete UI — cards, profile slide-over, donut chart, chat panel
├── requirements.txt     # Two packages: fastapi, uvicorn
└── README.md
```

## Run Locally

```bash
git clone https://github.com/PATNALAMAHESHCHANDRAMOULI/-talent-scout.git
cd -talent-scout
pip install -r requirements.txt
python -m uvicorn main:app --reload
```

Open [http://localhost:8000](http://localhost:8000) in your browser.

No `.env` file. No API keys. No database setup.

## Sample Output

A rank 1 candidate from the sample JD above:

```json
{
  "rank": 1,
  "candidate_name": "Priya Sharma",
  "title": "Senior Backend Engineer",
  "final_score": 85,
  "match_score": 85,
  "interest_score": 85,
  "interest_level": "high",
  "matched_skills": ["fastapi", "postgresql", "rest api", "python", "redis"],
  "missed_skills": ["django", "kubernetes", "event-driven"],
  "availability": "immediate",
  "why_ranked": "Priya matched 4 of 5 required skills with 6y experience (need 4y). Priya showed strong interest in the role.",
  "outreach_message": "Hey Priya — saw your background as a Senior Backend Engineer and your work with python and fastapi...",
  "candidate_replies": [
    "Hey, thanks for reaching out! I'm definitely interested — Priya's been looking for exactly this kind of role.",
    "Sounds good to me. I'm open to learning more about the team and the stack."
  ]
}
```

## Tech Stack

| Layer      | Technology         | Why                                                                     |
|:-----------|:-------------------|:------------------------------------------------------------------------|
| Backend    | FastAPI + Uvicorn  | Async-native, auto-generates OpenAPI docs, minimal boilerplate          |
| Frontend   | Vanilla JS + CSS   | Single HTML file, no build step, instant deployment                     |
| Scoring    | Python `dict` math | Transparent arithmetic — every point traceable to a rule in `matcher.py`|
| NLP        | Python `re` (regex)| Pattern matching is sufficient for structured JD text, no model needed  |
| Deployment | Render.com         | Git-push deploys, free tier, zero config                                |
| Charts     | CSS `conic-gradient` | Donut chart in 4 lines of CSS — no Chart.js, no canvas, no library   |

**Deliberately not used:** scikit-learn, TensorFlow, OpenAI API, LangChain, any database, any CSS framework (Tailwind/Bootstrap), any JS framework (React/Vue), any charting library.

## Why This Approach

Black-box recruitment AI has a trust problem. When a tool says "this candidate scores 73" and can't explain why, recruiters either blindly trust it (bad) or ignore it entirely (wasteful). The moment you can't trace a score back to specific rules, you've built a liability disguised as a feature.

Every point in Talent Scout maps to a line in `matcher.py`. The `score_candidate` function returns a `breakdown` dict that shows exactly which skills matched, which were missed, how experience was evaluated, and what each component contributed. If a candidate scored 10/20 on experience, you can see it's because they had 3 years and the JD asked for 4. The interest classifier uses 3 explicit keyword lists — positive, neutral, negative — and the signals that fired are included in the response. Nothing is hidden.

This matters beyond demos. In a real recruiting workflow, a hiring manager will ask "why is candidate A ranked above candidate B?" If the answer is "the model said so," the tool gets abandoned within a week. If the answer is "A matched 4 of 5 required skills and showed high interest; B matched 3 and was neutral," the tool becomes part of the process. Explainability isn't a feature — it's the reason the tool gets used.

## API Reference

### `POST /analyze`

Parses a job description and returns ranked candidates with scores, outreach, and engagement signals.

**Request:**

```json
{
  "jd_text": "We need a senior Python developer with 5+ years..."
}
```

**Response:**

```json
{
  "parsed_jd": {
    "required_skills": ["python", "fastapi", "postgresql", "rest api"],
    "preferred_skills": ["kubernetes", "docker", "redis"],
    "min_years_experience": 4,
    "role_level": "senior",
    "location_preference": "remote"
  },
  "ranked_candidates": [
    {
      "rank": 1,
      "candidate_name": "...",
      "final_score": 85,
      "match_score": 85,
      "interest_score": 85,
      "interest_level": "high",
      "matched_skills": [],
      "missed_skills": [],
      "availability": "immediate",
      "why_ranked": "...",
      "outreach_message": "...",
      "candidate_replies": []
    }
  ]
}
```

### `GET /candidates`

Returns the raw list of 12 mock candidate profiles with skills, experience, location, salary expectation, and availability.

## License

MIT — use it, fork it, ship it.

---

<div align="center">

**Built with intent. No magic, no black boxes.**

[talent-scout-kfaa.onrender.com](https://talent-scout-kfaa.onrender.com/)

</div>
