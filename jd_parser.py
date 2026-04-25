# jd_parser.py — extracts skills, role level, experience from raw JD text

import re

# skills we know how to normalize — maps common variations to canonical names
SKILL_ALIASES = {
    "react.js": "react", "reactjs": "react", "react js": "react",
    "node.js": "node", "nodejs": "node", "node js": "node",
    "fastapi": "fastapi", "fast api": "fastapi",
    "postgresql": "postgresql", "postgres": "postgresql", "psql": "postgresql",
    "rest api": "rest api", "restful": "rest api", "rest apis": "rest api",
    "kubernetes": "kubernetes", "k8s": "kubernetes",
    "docker": "docker", "containers": "docker",
    "redis": "redis",
    "python": "python",
    "django": "django",
    "flask": "flask",
    "typescript": "typescript", "ts": "typescript",
    "javascript": "javascript", "js": "javascript",
    "aws": "aws", "amazon web services": "aws",
    "gcp": "gcp", "google cloud": "gcp",
    "terraform": "terraform",
    "event-driven": "event-driven", "event driven": "event-driven",
    "spark": "spark", "apache spark": "spark",
    "airflow": "airflow",
    "graphql": "graphql",
    "mongodb": "mongodb", "mongo": "mongodb",
    "mysql": "mysql",
    "sqlite": "sqlite",
    "html": "html", "css": "css",
}

# role-level keywords — matched against the full JD text
ROLE_LEVELS = {
    "lead": ["lead", "principal", "staff", "head of", "architect"],
    "senior": ["senior", "sr.", "sr ", "experienced"],
    "mid": ["mid-level", "mid level", "intermediate"],
    "junior": ["junior", "jr.", "jr ", "entry-level", "entry level", "associate"],
}


def parse_jd(raw_text: str) -> dict:
    text_lower = raw_text.lower()

    required_skills = _extract_skills_from_section(raw_text, is_required=True)
    preferred_skills = _extract_skills_from_section(raw_text, is_required=False)
    min_years = _extract_min_years(text_lower)
    role_level = _detect_role_level(text_lower)
    location = _detect_location_preference(text_lower)

    return {
        "required_skills": required_skills,
        "preferred_skills": preferred_skills,
        "min_years_experience": min_years,
        "role_level": role_level,
        "location_preference": location,
    }


def _extract_skills_from_section(raw_text: str, is_required: bool) -> list:
    """Pull skills from either the requirements or nice-to-have section."""
    text_lower = raw_text.lower()

    if is_required:
        # grab text between "requirements"/"required" and the next section header or "nice to have"
        pattern = r"(?:requirements?|required|must have)[:\s]*\n(.*?)(?=\n\s*(?:nice to have|preferred|bonus|we offer|about|$))"
    else:
        # grab text after "nice to have"/"preferred"/"bonus"
        pattern = r"(?:nice to have|preferred|bonus|good to have)[:\s]*\n(.*?)(?=\n\s*(?:we |about|$))"

    match = re.search(pattern, text_lower, re.DOTALL)
    section_text = match.group(1) if match else text_lower

    found = []
    for alias, canonical in SKILL_ALIASES.items():
        # word-boundary match so "react" doesn't match inside "reactionary"
        if re.search(r'\b' + re.escape(alias) + r'\b', section_text):
            if canonical not in found:
                found.append(canonical)

    return found


def _extract_min_years(text_lower: str) -> int:
    """Look for patterns like '4+ years', '3-5 years', 'at least 5 years'."""

    # "4+ years" or "4 + years"
    match = re.search(r'(\d+)\s*\+?\s*years', text_lower)
    if match:
        return int(match.group(1))

    # "at least N years"
    match = re.search(r'at least\s+(\d+)\s+years', text_lower)
    if match:
        return int(match.group(1))

    # if no min_years found, assume entry-level is fine
    return 0


def _detect_role_level(text_lower: str) -> str:
    """Check for role-level keywords in descending seniority order."""
    for level, keywords in ROLE_LEVELS.items():
        for kw in keywords:
            if kw in text_lower:
                return level
    return "unknown"


def _detect_location_preference(text_lower: str) -> str:
    """Figure out if the role is remote, onsite, or location-specific."""

    # explicit remote signals
    if re.search(r'\b(fully remote|remote[- ]first|100% remote|remote friendly)\b', text_lower):
        return "remote"

    # explicit onsite signals
    if re.search(r'\b(on[- ]?site|in[- ]?office|office[- ]?based)\b', text_lower):
        return "onsite"

    # "flexible" / "hybrid"
    if re.search(r'\b(flexible|hybrid)\b', text_lower):
        return "flexible"

    return "flexible"
