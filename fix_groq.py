"""
Groq Fix Script
Run from: C:\\project-main\\interview_service
Command:  py -3.11 fix_groq.py
"""

import os

BASE = r"C:\project-main\interview_service"

# Groq model to use (compatible with gpt-4o-mini tasks)
GROQ_MODEL = "llama-3.3-70b-versatile"

FILES = {

    # ── LangChain wali files (ChatOpenAI → ChatGroq) ──────────────────────────

    r"practice\Aptitude\wording_llm.py": [
        (
            'from langchain_openai import ChatOpenAI',
            'from langchain_groq import ChatGroq'
        ),
        (
            'llm = ChatOpenAI(\n    model="nvidia/nemotron-3-ultra-550b-a55b:free",\n    temperature=0.5\n)',
            f'llm = ChatGroq(\n    model="{GROQ_MODEL}",\n    temperature=0.5\n)'
        ),
    ],

    r"practice\HR\hr.py": [
        (
            'from langchain_openai import ChatOpenAI',
            'from langchain_groq import ChatGroq'
        ),
        (
            'llm = ChatOpenAI(\n    model=config.MODEL,\n    temperature=0.2,\n)',
            f'llm = ChatGroq(\n    model="{GROQ_MODEL}",\n    temperature=0.2,\n)'
        ),
    ],

    r"practice\HR\interview_engine.py": [
        (
            'from langchain_openai import ChatOpenAI',
            'from langchain_groq import ChatGroq'
        ),
        (
            'llm = ChatOpenAI(\n    model=config.MODEL,\n    temperature=0.2\n)',
            f'llm = ChatGroq(\n    model="{GROQ_MODEL}",\n    temperature=0.2\n)'
        ),
    ],

    # ── AsyncOpenAI / OpenAI client wali files — OpenRouter pe rehti hain ──────
    # (In files mein sirf model string change karni hai agar hardcoded hai)

    r"practice\Tech\engines\resume_engine.py": [
        (
            'model="nvidia/nemotron-3-ultra-550b-a55b:free"',
            'model="openai/gpt-4o-mini"'
        ),
    ],
}


def apply_patches(rel_path, patches):
    full = os.path.join(BASE, rel_path)
    if not os.path.exists(full):
        print(f"  ❌ Not found: {full}")
        return

    with open(full, "r", encoding="utf-8") as f:
        content = f.read()

    changed = False
    for old, new in patches:
        if old in content:
            content = content.replace(old, new, 1)
            changed = True
            print(f"  ✅ Patched: {rel_path}")
        else:
            print(f"  ⚠️  Pattern not found (may already be patched): {rel_path}")
            print(f"      Looking for: {repr(old[:60])}...")

    if changed:
        with open(full, "w", encoding="utf-8") as f:
            f.write(content)


if __name__ == "__main__":
    print("=" * 55)
    print("  Groq Fix Script")
    print("=" * 55)

    for rel_path, patches in FILES.items():
        apply_patches(rel_path, patches)

    print("\n" + "=" * 55)
    print("  Ab yeh karo:\n")
    print("  1. pip install langchain-groq")
    print('  2. .env mein check karo: GROQ_API_KEY=gsk_...')
    print("  3. uvicorn main:app --reload")
    print("=" * 55)