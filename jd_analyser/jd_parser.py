import re

JD_SECTION_HEADERS = {
    "required_skills": ["required skills", "skills required", "must have skills", "key skills"],
    "qualifications": ["qualifications", "education requirements", "eligibility"],
    "responsibilities": ["responsibilities", "key responsibilities", "roles and responsibilities", "duties"],
}

EXPERIENCE_REGEX = r"(\d+)\+?\s*(?:to|-)?\s*(\d+)?\s*years?"


def extract_job_title(text):
    lines = [l.strip() for l in text.strip().split("\n") if l.strip()]
    return lines[0] if lines else ""


def extract_experience_level(text):
    match = re.search(EXPERIENCE_REGEX, text, re.IGNORECASE)
    if match:
        return match.group(0)
    return "Not specified"


def split_jd_sections(text):
    lines = text.split("\n")
    sections = {}
    current_section = "summary"
    sections[current_section] = []

    for line in lines:
        stripped = line.strip().lower()
        matched_section = None
        for section, keywords in JD_SECTION_HEADERS.items():
            if any(stripped == kw or stripped.startswith(kw) for kw in keywords):
                matched_section = section
                break
        if matched_section:
            current_section = matched_section
            sections[current_section] = []
        else:
            sections[current_section].append(line)

    return {k: "\n".join(v).strip() for k, v in sections.items()}


def extract_list_items(section_text):
    if not section_text:
        return []
    section_text = re.sub(r"[•▪●]", "\n", section_text)
    items = re.split(r"[\n,]", section_text)
    return [item.strip() for item in items if item.strip()]


def parse_job_description(raw_text):
    sections = split_jd_sections(raw_text)

    jd = {
        "job_title": extract_job_title(raw_text),
        "required_skills": extract_list_items(sections.get("required_skills", "")),
        "experience_level": extract_experience_level(raw_text),
        "qualifications": extract_list_items(sections.get("qualifications", "")),
        "responsibilities": extract_list_items(sections.get("responsibilities", "")),
    }
    return jd