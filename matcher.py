# matcher.py — scores a candidate against a parsed JD (100-point scale)


def score_candidate(candidate: dict, parsed_jd: dict) -> dict:
    """Run all scoring components and return total + full breakdown."""
    required = _score_required_skills(candidate, parsed_jd)
    preferred = _score_preferred_skills(candidate, parsed_jd)
    experience = _score_experience(candidate, parsed_jd)
    availability = _score_availability(candidate)
    recency = _score_recency(candidate)

    total = (
        required["earned"]
        + preferred["earned"]
        + experience["earned"]
        + availability["earned"]
        + recency["earned"]
    )

    # hard cap — shouldn't exceed 100 but defensive coding
    total = min(total, 100)

    return {
        "total": total,
        "breakdown": {
            "required_skills": required,
            "preferred_skills": preferred,
            "experience_fit": experience,
            "availability": availability,
            "recency": recency,
        },
    }


def _score_required_skills(candidate: dict, parsed_jd: dict) -> dict:
    """50 pts max — proportion of required skills the candidate has."""
    required = parsed_jd.get("required_skills", [])
    if not required:
        return {"earned": 50, "max": 50, "matched": [], "missed": []}

    candidate_skills = set(candidate["skills"])
    matched = [s for s in required if s in candidate_skills]
    missed = [s for s in required if s not in candidate_skills]

    earned = round(len(matched) / len(required) * 50)

    return {"earned": earned, "max": 50, "matched": matched, "missed": missed}


def _score_preferred_skills(candidate: dict, parsed_jd: dict) -> dict:
    """15 pts max — bonus for nice-to-have skills. 0 if JD has none listed."""
    preferred = parsed_jd.get("preferred_skills", [])
    if not preferred:
        return {"earned": 0, "max": 15, "matched": [], "missed": []}

    candidate_skills = set(candidate["skills"])
    matched = [s for s in preferred if s in candidate_skills]
    missed = [s for s in preferred if s not in candidate_skills]

    earned = round(len(matched) / len(preferred) * 15)

    return {"earned": earned, "max": 15, "matched": matched, "missed": missed}


def _score_experience(candidate: dict, parsed_jd: dict) -> dict:
    """20 pts — full if meets/exceeds, half if within 1 year, 0 otherwise."""
    required_years = parsed_jd.get("min_years_experience", 0)
    candidate_years = candidate["years_experience"]

    if candidate_years >= required_years:
        earned = 20
    elif candidate_years >= required_years - 1:
        # close enough — within 1 year shortfall
        earned = 10
    else:
        earned = 0

    return {
        "earned": earned,
        "max": 20,
        "candidate_years": candidate_years,
        "required_years": required_years,
    }


def _score_availability(candidate: dict) -> dict:
    """10 pts — immediate joiners get full marks, longer notice = fewer."""
    status = candidate["availability"]
    scores = {"immediate": 10, "2 weeks": 7, "1 month": 4}
    earned = scores.get(status, 0)

    return {"earned": earned, "max": 10, "status": status}


def _score_recency(candidate: dict) -> dict:
    """5 pts — recently active candidates are more likely to respond."""
    days = candidate["last_active_days_ago"]

    if days <= 7:
        earned = 5
    elif days <= 30:
        earned = 3
    else:
        earned = 0

    return {"earned": earned, "max": 5, "days_ago": days}
