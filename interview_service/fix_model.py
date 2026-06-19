"""
Model Fix Script
Run from: C:\\project-main\\interview_service
Command:  py -3.11 fix_model.py
"""

import os

BASE = r"C:\project-main\interview_service"

OLD_MODEL = "nvidia/nemotron-3-ultra-550b-a55b:free"
NEW_MODEL = "llama-3.3-70b-versatile"

FILES = [
    r"practice\Config\config.py",
    r"practice\HR\hr.py",
    r"practice\Aptitude\wording_llm.py",
    r"practice\Tech\engines\topic_engine.py",
    r"practice\Tech\engines\resume_engine.py",
    r"practice\Tech\engines\answer_analyzer.py",
    r"practice\Tech\engines\final_evaluation_engine.py",
    r"practice\Tech\Question_generator.py",
]

if __name__ == "__main__":
    print("=" * 50)
    print("  Model Fix Script")
    print("=" * 50)

    for rel in FILES:
        full = os.path.join(BASE, rel)
        if not os.path.exists(full):
            print(f"  ❌ Not found: {rel}")
            continue

        with open(full, "r", encoding="utf-8") as f:
            content = f.read()

        if OLD_MODEL in content:
            content = content.replace(OLD_MODEL, NEW_MODEL)
            with open(full, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  ✅ Fixed: {rel}")
        else:
            print(f"  ⚠️  Already ok: {rel}")

    print("\n  Done! Ab uvicorn main:app --reload chalao!")
    print("=" * 50)
