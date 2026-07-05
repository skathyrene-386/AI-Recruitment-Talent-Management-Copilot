import re
import spacy

_nlp = None


def get_nlp():
    global _nlp
    if _nlp is None:
        _nlp = spacy.load("en_core_web_sm")
    return _nlp


SECTION_HEADERS = {
    "education": ["education", "academic background", "qualifications"],
    "skills": ["skills", "technical skills", "key skills"],
    "experience": ["experience", "work experience", "employment history", "professional experience"],
    "certifications": ["certifications", "certificates", "licenses"],
    "projects": ["projects", "academic projects", "personal projects"],
}

EMAIL_REGEX = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
PHONE_REGEX = r"(\+?\d{1,3}[\s-]?)?(\(?\d{3,4}\)?[\s-]?)?\d{3,4}[\s-]?\d{3,4}"


def extract_email(text):
    match = re.search(EMAIL_REGEX, text)
    return match.group(0) if match else ""


def extract_phone(text):
    match = re.search(PHONE_REGEX, text)
    return match.group(0).strip() if match else ""


def extract_name(text):
    nlp = get_nlp()
    first_chunk = "\n".join(text.strip().split("\n")[:5])
    doc = nlp(first_chunk)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    lines = [l.strip() for l in text.strip().split("\n") if l.strip()]
    return lines[0] if lines else ""


def split_into_sections(text):
    lines = text.split("\n")
    sections = {}
    current_section = "header"
    sections[current_section] = []

    for line in lines:
        stripped = line.strip().lower()
        matched_section = None
        for section, keywords in SECTION_HEADERS.items():
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


def parse_resume(raw_text):
    sections = split_into_sections(raw_text)

    profile = {
        "name": extract_name(raw_text),
        "email": extract_email(raw_text),
        "phone": extract_phone(raw_text),
        "education": extract_list_items(sections.get("education", "")),
        "skills": extract_list_items(sections.get("skills", "")),
        "experience": extract_list_items(sections.get("experience", "")),
        "certifications": extract_list_items(sections.get("certifications", "")),
        "projects": extract_list_items(sections.get("projects", "")),
    }
    return profile