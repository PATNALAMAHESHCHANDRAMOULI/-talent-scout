# conversation.py — simulates recruiter outreach, candidate replies, and interest classification

import random

# Interest score is intentionally coarse — 3 buckets, not false precision.
INTEREST_SCORES = {"high": 85, "medium": 50, "low": 15}

POSITIVE_SIGNALS = ["interested", "tell me more", "sounds good", "when can we", "open to"]
NEUTRAL_SIGNALS = ["depends", "what's the", "could work", "maybe", "currently"]
NEGATIVE_SIGNALS = ["not looking", "happy where", "pass", "no thanks", "not a fit"]


def generate_outreach(candidate: dict, jd_summary: dict) -> str:
    """Write a short recruiter DM — no corporate fluff, just get to the point."""
    name = candidate["name"].split()[0]
    title = candidate["title"]
    skills = candidate["skills"]

    # pick up to 2 skills that actually appear in the JD requirements
    jd_skills = set(jd_summary.get("required_skills", []) + jd_summary.get("preferred_skills", []))
    overlap = [s for s in skills if s in jd_skills][:2]
    skill_mention = " and ".join(overlap) if overlap else skills[0]

    role_level = jd_summary.get("role_level", "")
    level_text = f"{role_level} " if role_level != "unknown" else ""

    msg = (
        f"Hey {name} — saw your background as a {title} and your work with {skill_mention}. "
        f"We're hiring a {level_text}backend engineer for our platform team. "
        f"The role is {jd_summary.get('location_preference', 'flexible')} and we're moving fast. "
        f"Would love to chat if you're open to it."
    )

    return msg


def simulate_replies(candidate: dict, match_score: int) -> list:
    """Generate 2 replies based on how well the candidate fits. Higher score = more enthusiasm."""
    name = candidate["name"].split()[0]

    if match_score >= 75:
        replies = [
            f"Hey, thanks for reaching out! I'm definitely interested — {name}'s been looking for exactly this kind of role. When can we set up a call?",
            f"Sounds good to me. I'm open to learning more about the team and the stack. Tell me more about the day-to-day.",
        ]
    elif match_score >= 50:
        replies = [
            f"Could work, depends on the details. What's the compensation range looking like?",
            f"Maybe — I'm currently exploring a few things. Is this fully remote or would I need to relocate?",
        ]
    else:
        replies = [
            f"Appreciate you reaching out, but I'm not looking right now. Happy where I am.",
            f"Thanks, but this doesn't seem like a fit for what I'm doing currently. No thanks.",
        ]

    return replies


def classify_interest(replies: list) -> dict:
    """Rule-based classifier — scan replies for signal keywords and bucket into high/medium/low."""
    combined = " ".join(replies).lower()

    pos_found = [s for s in POSITIVE_SIGNALS if s in combined]
    neu_found = [s for s in NEUTRAL_SIGNALS if s in combined]
    neg_found = [s for s in NEGATIVE_SIGNALS if s in combined]

    # simple priority: if any positive signals and no negatives → high
    if pos_found and not neg_found:
        level = "high"
    elif neg_found and not pos_found:
        level = "low"
    else:
        level = "medium"

    return {
        "level": level,
        "signals_found": pos_found + neu_found + neg_found,
        "interest_score": INTEREST_SCORES[level],
    }
