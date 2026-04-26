<div align="center">

# 🎯 Talent Scout

**AI-Powered Candidate Matching Agent**

Paste a job description. Get ranked candidates with match scores, simulated recruiter outreach, and engagement signals — instantly.

[![Live Demo](https://img.shields.io/badge/Live_Demo-talent--scout-5B4FE8?style=for-the-badge&logo=render&logoColor=white)](https://talent-scout-kfaa.onrender.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.135+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

</div>

---

## 🚀 Live Demo

**→ [talent-scout-kfaa.onrender.com](https://talent-scout-kfaa.onrender.com/)**

No setup required. Paste any job description and see ranked candidates in seconds.

---

## 📌 What It Does

Talent Scout is a lightweight, deterministic AI agent that automates the early-stage talent sourcing pipeline:

1. **Parses** a raw job description → extracts required skills, preferred skills, experience level, role seniority, and location preference using regex-based NLP
2. **Scores** each candidate from a mock dataset against the parsed JD on a 100-point scale across 5 weighted components
3. **Simulates** personalized recruiter outreach messages and generates realistic candidate replies
4. **Classifies** candidate interest level (high / medium / low) from simulated replies using keyword signal detection
5. **Ranks** all candidates by a weighted final score: `(Match Score × 0.6) + (Interest Score × 0.4)`
6. **Profile Panel** — click any candidate card to open a detailed slide-over with score donut chart, skill breakdown grid, and verdict badge
7. **Recruiter Chat** — real-time chat simulator inside the profile panel with keyword-matched replies, typing indicator, and quick-reply chips

> No ML models. No API keys. No external services. Pure deterministic logic — regex, scoring rules, and a clean UI.

---

## ✨ Features

| Feature | Description |
|:---|:---|
| **🔍 JD Parser** | Extracts required skills, preferred skills, experience threshold, role level, and location from raw text using regex and keyword matching |
| **📊 Match Scoring** | Scores each candidate on a 100-point scale across 5 components: skill overlap, experience fit, availability, and recency |
| **💬 Interest Simulation** | Generates personalized recruiter outreach, simulates candidate replies, classifies interest as High/Medium/Low |
| **🏆 Candidate Ranking** | Merges match and interest scores with configurable weights (60/40), sorts, and generates human-readable explanations |
| **👤 Profile Panel** | Click any card to open a slide-over with CSS donut chart, skill assessment grid with dot bars, and full outreach history |
| **💭 Recruiter Chat** | Real-time chat inside the profile panel — keyword-matched deterministic replies with typing indicator and quick-reply chips |
| **⚡ Zero Dependencies** | No ML models, no API keys, no database, no CSS framework, no build step. Two pip packages: `fastapi` and `uvicorn` |

---

## 🧠 How Scoring Works

Each candidate is evaluated on a **100-point scale** across five components:

| Component | Max Points | Logic |
|:---|:---:|:---|
| **Required Skills** | 50 | `matched / total × 50` |
| **Preferred Skills** | 15 | `matched / total × 15` (0 if none listed in JD) |
| **Experience Fit** | 20 | Meets requirement = 20, within 1 year = 10, below = 0 |
| **Availability** | 10 | Immediate = 10, 2 weeks = 7, 1 month = 4 |
| **Recency** | 5 | Active ≤7 days = 5, ≤30 days = 3, older = 0 |

**Interest scoring** uses simulated outreach replies classified into three buckets:

| Interest Level | Score | Signal Keywords |
|:---|:---:|:---|
| 🟢 High | 85 | "interested", "tell me more", "sounds good" |
| 🟡 Medium | 50 | "depends", "could work", "maybe" |
| 🔴 Low | 15 | "not looking", "pass", "no thanks" |

### Final Score

```
Final Score = (Match Score × 0.6) + (Interest Score × 0.4)
```

Three fixed buckets instead of a continuous score is intentional — false precision on simulated data is worse than honest approximation. A candidate either showed interest signals, was neutral, or wasn't interested.

---

## 🏗️ Architecture

```
Browser
  │
  ├── GET /           → static/index.html (full UI + profile panel + chat)
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

---

## 📂 Project Structure

```
talent_agent/
├── main.py              # FastAPI app — 2 routes, CORS, static file serving
├── jd_parser.py         # Regex-based JD parser — skills, experience, role level
├── matcher.py           # 100-point scoring engine (5 weighted components)
├── conversation.py      # Outreach generator + reply simulator + interest classifier
├── ranker.py            # Score merger, sorter, and explanation builder
├── data/
│   └── candidates.py    # 12 mock candidate profiles with skills, experience, salary
├── static/
│   └── index.html       # Complete UI — cards, profile slide-over, donut chart, chat
├── requirements.txt     # Python dependencies (fastapi, uvicorn)
└── README.md
```

---

## ⚡ Quick Start

### Prerequisites

- Python 3.10+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/PATNALAMAHESHCHANDRAMOULI/-talent-scout.git
cd -talent-scout

# Install dependencies
pip install -r requirements.txt

# Start the server
python -m uvicorn main:app --reload
```

Open **[http://localhost:8000](http://localhost:8000)** in your browser.

No `.env` file. No API keys. No database setup.

---

## 🧪 Sample Job Description

Try pasting this into the app:

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

### Sample Output (Rank 1)

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
  "outreach_message": "Hey Priya — saw your background as a Senior Backend Engineer...",
  "candidate_replies": [
    "Hey, thanks for reaching out! I'm definitely interested...",
    "Sounds good to me. I'm open to learning more about the team."
  ]
}
```

---

## 🔌 API Reference

### `POST /analyze`

Parse a job description and return ranked candidates with scores, outreach, and engagement signals.

**Request:**

```bash
curl -X POST https://talent-scout-kfaa.onrender.com/analyze \
  -H "Content-Type: application/json" \
  -d '{"jd_text": "We need a senior Python developer with 5+ years..."}'
```

**Response:**

```json
{
  "parsed_jd": {
    "required_skills": ["python", "fastapi", "postgresql", "rest api"],
    "preferred_skills": ["kubernetes", "docker", "redis", "event-driven"],
    "min_years_experience": 4,
    "role_level": "senior",
    "location_preference": "remote"
  },
  "ranked_candidates": [
    {
      "rank": 1,
      "candidate_name": "Priya Sharma",
      "final_score": 85,
      "match_score": 85,
      "interest_score": 85,
      "interest_level": "high",
      "matched_skills": ["fastapi", "postgresql", "rest api", "python", "redis"],
      "missed_skills": ["django", "kubernetes", "event-driven"],
      "availability": "immediate",
      "why_ranked": "...",
      "outreach_message": "...",
      "candidate_replies": ["...", "..."]
    }
  ]
}
```

### `GET /candidates`

Returns the raw list of 12 mock candidate profiles with skills, experience, location, salary expectation, and availability.

```bash
curl https://talent-scout-kfaa.onrender.com/candidates
```

---

## 🛠️ Tech Stack

| Layer | Technology | Why |
|:---|:---|:---|
| **Backend** | FastAPI + Uvicorn | Async-native, auto-generates OpenAPI docs, minimal boilerplate |
| **Frontend** | Vanilla JS + CSS | Single HTML file, no build step, instant deployment |
| **Scoring** | Python `dict` math | Transparent arithmetic — every point traceable to a rule in `matcher.py` |
| **NLP** | Python `re` (regex) | Pattern matching is sufficient for structured JD text |
| **Deployment** | Render.com | Git-push deploys, free tier, zero config |
| **Charts** | CSS `conic-gradient` | Donut chart in 4 lines of CSS — no Chart.js, no canvas |

**Deliberately not used:** scikit-learn, TensorFlow, OpenAI API, LangChain, any database, any CSS framework (Tailwind/Bootstrap), any JS framework (React/Vue), any charting library.

---

## 💡 Why This Approach

Black-box recruitment AI has a trust problem. When a tool says "this candidate scores 73" and can't explain why, recruiters either blindly trust it or ignore it entirely. The moment you can't trace a score back to specific rules, you've built a liability disguised as a feature.

Every point in Talent Scout maps to a line in `matcher.py`. The `score_candidate` function returns a `breakdown` dict that shows exactly which skills matched, which were missed, how experience was evaluated, and what each component contributed. The interest classifier uses 3 explicit keyword lists — positive, neutral, negative — and the signals that fired are included in the response. Nothing is hidden.

This matters in a real recruiting workflow. A hiring manager will ask "why is candidate A ranked above candidate B?" If the answer is "the model said so," the tool gets abandoned. If the answer is "A matched 4 of 5 required skills and showed high interest; B matched 3 and was neutral," the tool becomes part of the process. Explainability isn't a feature — it's the reason the tool gets used.

---

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

<div align="center">

**Built with intent. No magic, no black boxes.**

**[Try the Live Demo →](https://talent-scout-kfaa.onrender.com/)**

</div>
