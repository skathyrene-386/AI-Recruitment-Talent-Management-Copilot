import sqlite3
import json
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "recruitment.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT,
            name TEXT,
            email TEXT,
            phone TEXT,
            education TEXT,
            skills TEXT,
            experience TEXT,
            certifications TEXT,
            projects TEXT,
            raw_text TEXT,
            created_at TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS job_descriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_title TEXT,
            required_skills TEXT,
            experience_level TEXT,
            qualifications TEXT,
            responsibilities TEXT,
            raw_text TEXT,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_candidate(profile: dict, file_name: str, raw_text: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO candidates
        (file_name, name, email, phone, education, skills, experience, certifications, projects, raw_text, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        file_name,
        profile.get("name"),
        profile.get("email"),
        profile.get("phone"),
        json.dumps(profile.get("education", [])),
        json.dumps(profile.get("skills", [])),
        json.dumps(profile.get("experience", [])),
        json.dumps(profile.get("certifications", [])),
        json.dumps(profile.get("projects", [])),
        raw_text,
        datetime.now().isoformat()
    ))
    conn.commit()
    candidate_id = cur.lastrowid
    conn.close()
    return candidate_id


def save_job_description(jd: dict, raw_text: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO job_descriptions
        (job_title, required_skills, experience_level, qualifications, responsibilities, raw_text, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        jd.get("job_title"),
        json.dumps(jd.get("required_skills", [])),
        jd.get("experience_level"),
        json.dumps(jd.get("qualifications", [])),
        json.dumps(jd.get("responsibilities", [])),
        raw_text,
        datetime.now().isoformat()
    ))
    conn.commit()
    jd_id = cur.lastrowid
    conn.close()
    return jd_id


def get_all_candidates():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM candidates ORDER BY id DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_all_job_descriptions():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM job_descriptions ORDER BY id DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]