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

> No ML models. No API keys. No external services. Pure deterministic logic — regex, scoring rules, and a clean UI.

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

**Final Score** = `(Match Score × 0.6) + (Interest Score × 0.4)`

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────┐
│                     Frontend (Vanilla JS)                │
│              static/index.html — single file             │
└──────────────────────┬───────────────────────────────────┘
                       │ POST /analyze  { jd_text: "..." }
                       ▼
┌──────────────────────────────────────────────────────────┐
│                   FastAPI Backend (main.py)               │
│                                                          │
│  ┌─────────────┐  ┌────────────┐  ┌──────────────────┐  │
│  │  jd_parser   │  │  matcher   │  │  conversation    │  │
│  │  ─────────── │  │  ──────── │  │  ──────────────  │  │
│  │  Regex NLP   │→ │  Scoring  │→ │  Outreach sim    │  │
│  │  extraction  │  │  engine   │  │  Reply classify  │  │
│  └─────────────┘  └────────────┘  └──────────────────┘  │
│                          │                               │
│                    ┌─────▼──────┐                        │
│                    │  ranker    │                        │
│                    │  ────────  │                        │
│                    │  Merge,    │                        │
│                    │  sort,     │                        │
│                    │  explain   │                        │
│                    └────────────┘                        │
└──────────────────────────────────────────────────────────┘
                       │
                       ▼
              data/candidates.py
           (12 mock candidate profiles)
```

---

## 📂 Project Structure

```
talent_agent/
├── main.py              # FastAPI app — routes, CORS, static file serving
├── jd_parser.py         # Regex-based JD parser — skills, experience, role level
├── matcher.py           # 100-point candidate scoring engine (5 components)
├── conversation.py      # Outreach message generation + reply simulation
├── ranker.py            # Score merging, ranking, and explanation builder
├── data/
│   └── candidates.py    # Mock dataset — 12 realistic candidate profiles
├── static/
│   └── index.html       # Frontend — single-file vanilla JS + CSS
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
git clone https://github.com/PATNALAMAHESHCHANDRAMOULI/talent-scout.git
cd talent-scout/talent_agent

# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn main:app --reload
```

Open **[http://localhost:8000](http://localhost:8000)** in your browser.

---

## 🔌 API Reference

### `POST /analyze`

Parse a job description and return ranked candidates with scores, outreach, and engagement signals.

**Request:**
```bash
curl -X POST http://localhost:8000/analyze \
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
      "title": "Senior Backend Engineer",
      "final_score": 85.0,
      "match_score": 85,
      "interest_score": 85,
      "interest_level": "high",
      "matched_skills": ["fastapi", "postgresql", "rest api", "python", "redis"],
      "missed_skills": ["django", "kubernetes", "event-driven"],
      "availability": "immediate",
      "why_ranked": "Priya matched 4 of 5 required skills with 6y experience (need 4y). Priya showed strong interest in the role.",
      "outreach_message": "Hey Priya — saw your background as a Senior Backend Engineer...",
      "candidate_replies": ["Hey, thanks for reaching out!...", "Sounds good to me..."]
    }
  ]
}
```

### `GET /candidates`

Return the raw candidate dataset.

```bash
curl http://localhost:8000/candidates
```

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

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|:---|:---|:---|
| **Backend** | FastAPI + Uvicorn | REST API, async server |
| **Frontend** | Vanilla JS + CSS | Single-file UI, no build step |
| **Parsing** | Python `re` (regex) | Skill extraction, experience detection |
| **Scoring** | Deterministic rules | Weighted multi-component scoring |
| **Deployment** | Render | Cloud hosting |

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

Built with ☕ for a hackathon. Ships on a laptop.

**[Try the Live Demo →](https://talent-scout-kfaa.onrender.com/)**

</div>
