# ranker.py — merges match + interest scores, sorts, and builds the final ranked output

from matcher import score_candidate
from conversation import generate_outreach, simulate_replies, classify_interest


def rank_candidates(candidates: list, parsed_jd: dict) -> list:
    """Run the full pipeline: score → outreach → replies → classify → rank."""
    results = []

    for candidate in candidates:
        match_result = score_candidate(candidate, parsed_jd)
        match_score = match_result["total"]

        outreach = generate_outreach(candidate, parsed_jd)
        replies = simulate_replies(candidate, match_score)
        interest = classify_interest(replies)

        final_score = round(match_score * 0.6 + interest["interest_score"] * 0.4, 1)

        explanation = build_explanation(candidate, match_result["breakdown"], interest)

        results.append({
            "candidate_name": candidate["name"],
            "title": candidate["title"],
            "final_score": final_score,
            "match_score": match_score,
            "interest_score": interest["interest_score"],
            "interest_level": interest["level"],
            "why_ranked": explanation,
            "matched_skills": list(dict.fromkeys(
                match_result["breakdown"]["required_skills"]["matched"]
                + match_result["breakdown"]["preferred_skills"]["matched"]
            )),
            "missed_skills": list(dict.fromkeys(
                match_result["breakdown"]["required_skills"]["missed"]
                + match_result["breakdown"]["preferred_skills"]["missed"]
            )),
            "availability": candidate["availability"],
            "outreach_message": outreach,
            "candidate_replies": replies,
        })

    # sort by final_score desc, tie-break on match_score desc
    results.sort(key=lambda r: (r["final_score"], r["match_score"]), reverse=True)

    # assign ranks after sorting
    for i, r in enumerate(results):
        r["rank"] = i + 1

    return results


def build_explanation(candidate: dict, breakdown: dict, interest: dict) -> str:
    """1-2 sentence human-readable summary of why this candidate ranked where they did."""
    name = candidate["name"].split()[0]
    req = breakdown["required_skills"]
    exp = breakdown["experience_fit"]

    skill_summary = f"matched {len(req['matched'])} of {len(req['matched']) + len(req['missed'])} required skills"
    exp_summary = f"{exp['candidate_years']}y experience (need {exp['required_years']}y)"

    interest_text = {
        "high": "showed strong interest in the role",
        "medium": "was cautiously interested",
        "low": "wasn't interested at this time",
    }[interest["level"]]

    return f"{name} {skill_summary} with {exp_summary}. {name} {interest_text}."
