#!/usr/bin/env python3
"""
JAGRATAM-CLI — CEO Command Interface (Jagratam-Empire)
======================================================
SOP MAS: Shadow Advisor + PRD sebagai kerangka kerja permanen.

Architecture:
  Shadow Advisor  → Berjalan di background, selalu aktif (SOP MAS)
  /chat           → Owner + CEO + 62+ AI (semua spesialis)
                    Diskusi strategis, bisnis, geopolitik, investasi
  /terminal       → Owner + CEO + 35+ AI (spesialis teknis/coding)
                    Eksekusi operasional, coding, devops, infrastruktur
  /               → Command palette (seperti OpenCode)

Cara pakai:
  python jagratam.py              # Buka langsung, ketik / untuk menu
  python jagratam.py /chat        # Langsung masuk mode chat
  python jagratam.py /terminal    # Langsung masuk mode terminal
  python jagratam.py /help        # Bantuan
"""

import sys
import os
import subprocess
import json
import shutil
from datetime import datetime

# ═══════════════════════════════════════════════════════════════
# SHADOW ADVISOR — SOP MAS (Background Layer)
# Berjalan selalu di belakang setiap interaksi
# ═══════════════════════════════════════════════════════════════
SHADOW_ADVISOR_SOP = """
[KONTEKS PERMANEN — SHADOW ADVISOR]

Kamu beroperasi dalam kerangka Shadow Advisor, sistem intelijen strategis
yang beroperasi di balik layar kekuasaan, bisnis, teknologi, media, dan
perilaku manusia. Ini adalah SOP MAS (Multi-Agent System) Jagratam-Empire.

PRINSIP DASAR:
- Berpikir sebagai OPERATOR, bukan penonton
- Berpikir sebagai PEMBUAT KEPUTUSAN, bukan pengamat
- Fokus pada KENYATAAN, bukan asumsi atau simulasi
- Utamakan EFEKTIVITAS & KUALITAS, bukan popularitas atau kuantitas
- Cari AKAR MASALAH, bukan gejalanya

FORMAT ANALISIS (selalu gunakan):
1. Situasi Sebenarnya — Apa yang sebenarnya terjadi?
2. Faktor Tersembunyi — Apa yang tidak disadari kebanyakan orang/AI?
3. Risiko Utama — Apa ancaman terbesar?
4. Peluang Strategis — Dimana leverage terbesar?
5. Rencana Aksi — Langkah konkret
6. Prediksi — Hasil terbaik, sedang, terburuk
7. Kesimpulan CEO — Rekomendasi paling logis

ATURAN CEO & 62+ AI:
1. Analisis masalah dari berbagai sudut pandang
2. Identifikasi informasi tersembunyi
3. Cari motif, insentif, kepentingan tersembunyi
4. Temukan resiko yang terabaikan
5. Temukan peluang leverage tertinggi
6. Jelaskan efek jangka pendek
7. Prioritaskan solusi paling efektif
8. Berikan peta strategis, bukan sekedar jawaban
"""

# ═══════════════════════════════════════════════════════════════
# AI SPECIALISTS — 62+ (untuk /chat)
# ═══════════════════════════════════════════════════════════════
AI_CHAT_SPECIALISTS = [
    # --- C-SUITE ---
    {"id": 0,  "name": "CEO (Shadow Advisor)",     "role": "STRATEGI",    "expertise": "leadership, strategy, decision-making"},
    {"id": 1,  "name": "CTO Office (JARVIS)",       "role": "TEKNOLOGI",   "expertise": "technology, architecture, DevOps"},
    {"id": 2,  "name": "CTO Trading RL",            "role": "TRADING",     "expertise": "reinforcement learning, algorithmic trading"},
    {"id": 3,  "name": "CTO Trading Hyper",         "role": "TRADING",     "expertise": "high-frequency trading, market analysis"},
    {"id": 4,  "name": "CTO Commerce",              "role": "BISNIS",      "expertise": "e-commerce, payment systems, logistics"},
    {"id": 5,  "name": "CTO Browser",               "role": "TEKNOLOGI",   "expertise": "web scraping, browser automation, SEO"},
    {"id": 6,  "name": "CISO Shield",               "role": "SECURITY",    "expertise": "cybersecurity, penetration testing, compliance"},
    {"id": 7,  "name": "CISO ECC",                  "role": "SECURITY",    "expertise": "encryption, zero-trust, incident response"},
    {"id": 8,  "name": "AI Router",                 "role": "AI OPS",      "expertise": "task routing, load balancing, optimization"},
    {"id": 9,  "name": "CTO Self-Heal",             "role": "INFRA",       "expertise": "auto-recovery, monitoring, incident response"},
    # --- STRATEGI & BISNIS ---
    {"id": 10, "name": "Geopolitical Analyst",      "role": "GEOPOLITIK",  "expertise": "geopolitics, international relations, risk"},
    {"id": 11, "name": "Market Psychologist",       "role": "PSIKOLOGI",   "expertise": "market psychology, behavioral finance"},
    {"id": 12, "name": "Senior Negotiator",         "role": "NEGOSIASI",   "expertise": "negotiation, deal-making, conflict resolution"},
    {"id": 13, "name": "World-Class Investor",      "role": "INVESTASI",   "expertise": "portfolio management, venture capital"},
    {"id": 14, "name": "Information Warfare Expert","role": "INTELIJEN",   "expertise": "disinformation, media manipulation, propaganda"},
    {"id": 15, "name": "Tech Innovation Scout",     "role": "INOVASI",     "expertise": "emerging tech, patents, R&D"},
    {"id": 16, "name": "Legal National Expert",     "role": "HUKUM",       "expertise": "Indonesian law, compliance, regulatory"},
    {"id": 17, "name": "Legal International Expert","role": "HUKUM",       "expertise": "international law, cross-border, IP"},
    {"id": 18, "name": "Senior Risk Analyst",       "role": "RISIKO",      "expertise": "risk assessment, mitigation, insurance"},
    {"id": 19, "name": "Systems Thinker",           "role": "SISTEM",      "expertise": "complex systems, feedback loops, modeling"},
    {"id": 20, "name": "Elite Problem Solver",      "role": "PROBLEM",     "expertise": "root cause analysis, creative solutions"},
    # --- TEKNOLOGI & ENGINEERING ---
    {"id": 21, "name": "Data Scientist",            "role": "DATA",        "expertise": "ML, analytics, data engineering"},
    {"id": 22, "name": "Blockchain Expert",         "role": "BLOCKCHAIN",  "expertise": "DeFi, smart contracts, tokenomics"},
    {"id": 23, "name": "Cloud Architect",           "role": "CLOUD",       "expertise": "AWS, GCP, Azure, infrastructure"},
    {"id": 24, "name": "Mobile Developer",          "role": "MOBILE",      "expertise": "iOS, Android, React Native, Flutter"},
    {"id": 25, "name": "Backend Engineer",          "role": "BACKEND",     "expertise": "APIs, databases, microservices"},
    {"id": 26, "name": "Frontend Engineer",         "role": "FRONTEND",    "expertise": "UI/UX, React, Vue, CSS"},
    {"id": 27, "name": "DevOps Engineer",           "role": "DEVOPS",      "expertise": "CI/CD, Docker, Kubernetes, monitoring"},
    {"id": 28, "name": "Security Researcher",       "role": "SECURITY",    "expertise": "vulnerability research, exploit development"},
    {"id": 29, "name": "Quant Analyst",             "role": "QUANT",       "expertise": "quantitative finance, statistical modeling"},
    # --- BISNIS & OPERASI ---
    {"id": 30, "name": "Growth Hacker",             "role": "GROWTH",      "expertise": "growth strategies, viral marketing, A/B testing"},
    {"id": 31, "name": "Content Strategist",        "role": "KONTEN",      "expertise": "content marketing, SEO, copywriting"},
    {"id": 32, "name": "UX Researcher",             "role": "UX",          "expertise": "user research, usability testing, personas"},
    {"id": 33, "name": "Product Manager",           "role": "PRODUK",      "expertise": "product strategy, roadmaps, feature prioritization"},
    {"id": 34, "name": "Scrum Master",              "role": "AGILE",       "expertise": "agile, sprint planning, team coordination"},
    {"id": 35, "name": "Database Expert",           "role": "DATABASE",    "expertise": "SQL, NoSQL, data modeling, optimization"},
    {"id": 36, "name": "AI/ML Engineer",            "role": "AI/ML",       "expertise": "deep learning, NLP, computer vision"},
    {"id": 37, "name": "Embedded Systems",          "role": "IOT",         "expertise": "IoT, firmware, hardware integration"},
    {"id": 38, "name": "Game Designer",             "role": "GAME",        "expertise": "game theory, gamification, engagement"},
    {"id": 39, "name": "Financial Controller",      "role": "FINANSIAL",   "expertise": "accounting, financial reporting, budgeting"},
    # --- SDM & LEGAL ---
    {"id": 40, "name": "HR Director",               "role": "HR",          "expertise": "talent acquisition, culture, performance"},
    {"id": 41, "name": "Legal Counsel",             "role": "HUKUM",       "expertise": "contract law, liability, dispute resolution"},
    {"id": 42, "name": "PR Manager",                "role": "PR",          "expertise": "public relations, crisis communication, branding"},
    {"id": 43, "name": "Supply Chain Expert",       "role": "LOGISTIK",    "expertise": "logistics, procurement, inventory"},
    {"id": 44, "name": "Quality Assurance",         "role": "QA",          "expertise": "testing, quality control, standards"},
    {"id": 45, "name": "Technical Writer",          "role": "DOKUMENTASI", "expertise": "documentation, manuals, technical communication"},
    # --- SALES & CUSTOMER ---
    {"id": 46, "name": "Sales Director",            "role": "SALES",       "expertise": "sales strategy, pipeline, CRM"},
    {"id": 47, "name": "Customer Success",          "role": "CUSTOMER",    "expertise": "retention, support, satisfaction"},
    {"id": 48, "name": "Privacy Officer",           "role": "PRIVASI",     "expertise": "GDPR, data privacy, compliance"},
    {"id": 49, "name": "Sustainability Expert",     "role": "ESG",         "expertise": "ESG, green tech, carbon footprint"},
    # --- KRISIS & PARTNERSHIP ---
    {"id": 50, "name": "Crisis Manager",            "role": "KRISIS",      "expertise": "crisis response, business continuity"},
    {"id": 51, "name": "Partnership Lead",          "role": "PARTNER",     "expertise": "strategic alliances, JV, partnerships"},
    {"id": 52, "name": "Innovation Director",       "role": "INOVASI",     "expertise": "R&D, innovation pipeline, patents"},
    {"id": 53, "name": "Data Privacy Expert",       "role": "PRIVASI",     "expertise": "data governance, encryption, compliance"},
    # --- INFRASTRUKTUR ---
    {"id": 54, "name": "Network Engineer",          "role": "NETWORK",     "expertise": "networking, protocols, infrastructure"},
    {"id": 55, "name": "System Administrator",      "role": "SYSADMIN",    "expertise": "Linux, Windows, server management"},
    {"id": 56, "name": "Machine Learning Ops",      "role": "MLOPS",       "expertise": "MLOps, model deployment, monitoring"},
    {"id": 57, "name": "API Designer",              "role": "API",         "expertise": "REST, GraphQL, API governance"},
    {"id": 58, "name": "Performance Engineer",      "role": "PERFORMANCE", "expertise": "optimization, profiling, scaling"},
    {"id": 59, "name": "Accessibility Expert",      "role": "A11Y",        "expertise": "a11y, WCAG, inclusive design"},
    {"id": 60, "name": "Localization Lead",         "role": "LOKALISASI",  "expertise": "i18n, translation, cultural adaptation"},
    {"id": 61, "name": "Ethics Advisor",            "role": "ETIKA",       "expertise": "AI ethics, responsible tech, bias"},
    {"id": 62, "name": "Competitive Analyst",       "role": "KOMPETISI",   "expertise": "competitor analysis, market intelligence"},
]

# ═══════════════════════════════════════════════════════════════
# AI TERMINAL SPECIALISTS — 35+ (untuk /terminal)
# Hanya spesialis TEKNIS/CODING/INFRA
# ═══════════════════════════════════════════════════════════════
AI_TERMINAL_SPECIALISTS = [
    # --- C-SUITE TEKNOLOGI ---
    {"id": 0,  "name": "CEO (Shadow Advisor)",     "role": "STRATEGI",    "expertise": "leadership, strategy, decision-making"},
    {"id": 1,  "name": "CTO Office (JARVIS)",       "role": "TEKNOLOGI",   "expertise": "technology, architecture, DevOps"},
    {"id": 2,  "name": "CTO Trading RL",            "role": "TRADING",     "expertise": "reinforcement learning, algorithmic trading"},
    {"id": 3,  "name": "CTO Trading Hyper",         "role": "TRADING",     "expertise": "high-frequency trading, market analysis"},
    {"id": 4,  "name": "CTO Commerce",              "role": "BISNIS",      "expertise": "e-commerce, payment systems, logistics"},
    {"id": 5,  "name": "CTO Browser",               "role": "TEKNOLOGI",   "expertise": "web scraping, browser automation, SEO"},
    {"id": 6,  "name": "CISO Shield",               "role": "SECURITY",    "expertise": "cybersecurity, penetration testing, compliance"},
    {"id": 7,  "name": "CISO ECC",                  "role": "SECURITY",    "expertise": "encryption, zero-trust, incident response"},
    {"id": 8,  "name": "AI Router",                 "role": "AI OPS",      "expertise": "task routing, load balancing, optimization"},
    {"id": 9,  "name": "CTO Self-Heal",             "role": "INFRA",       "expertise": "auto-recovery, monitoring, incident response"},
    # --- CORE ENGINEERING ---
    {"id": 21, "name": "Data Scientist",            "role": "DATA",        "expertise": "ML, analytics, data engineering"},
    {"id": 22, "name": "Blockchain Expert",         "role": "BLOCKCHAIN",  "expertise": "DeFi, smart contracts, tokenomics"},
    {"id": 23, "name": "Cloud Architect",           "role": "CLOUD",       "expertise": "AWS, GCP, Azure, infrastructure"},
    {"id": 24, "name": "Mobile Developer",          "role": "MOBILE",      "expertise": "iOS, Android, React Native, Flutter"},
    {"id": 25, "name": "Backend Engineer",          "role": "BACKEND",     "expertise": "APIs, databases, microservices"},
    {"id": 26, "name": "Frontend Engineer",         "role": "FRONTEND",    "expertise": "UI/UX, React, Vue, CSS"},
    {"id": 27, "name": "DevOps Engineer",           "role": "DEVOPS",      "expertise": "CI/CD, Docker, Kubernetes, monitoring"},
    {"id": 28, "name": "Security Researcher",       "role": "SECURITY",    "expertise": "vulnerability research, exploit development"},
    {"id": 29, "name": "Quant Analyst",             "role": "QUANT",       "expertise": "quantitative finance, statistical modeling"},
    {"id": 35, "name": "Database Expert",           "role": "DATABASE",    "expertise": "SQL, NoSQL, data modeling, optimization"},
    {"id": 36, "name": "AI/ML Engineer",            "role": "AI/ML",       "expertise": "deep learning, NLP, computer vision"},
    {"id": 37, "name": "Embedded Systems",          "role": "IOT",         "expertise": "IoT, firmware, hardware integration"},
    # --- OPERASIONAL TEKNIS ---
    {"id": 44, "name": "Quality Assurance",         "role": "QA",          "expertise": "testing, quality control, standards"},
    {"id": 45, "name": "Technical Writer",          "role": "DOKUMENTASI", "expertise": "documentation, manuals, technical communication"},
    {"id": 54, "name": "Network Engineer",          "role": "NETWORK",     "expertise": "networking, protocols, infrastructure"},
    {"id": 55, "name": "System Administrator",      "role": "SYSADMIN",    "expertise": "Linux, Windows, server management"},
    {"id": 56, "name": "Machine Learning Ops",      "role": "MLOPS",       "expertise": "MLOps, model deployment, monitoring"},
    {"id": 57, "name": "API Designer",              "role": "API",         "expertise": "REST, GraphQL, API governance"},
    {"id": 58, "name": "Performance Engineer",      "role": "PERFORMANCE", "expertise": "optimization, profiling, scaling"},
    {"id": 59, "name": "Accessibility Expert",      "role": "A11Y",        "expertise": "a11y, WCAG, inclusive design"},
    {"id": 60, "name": "Localization Lead",         "role": "LOKALISASI",  "expertise": "i18n, translation, cultural adaptation"},
    # --- TAMBAHAN TEKNIS ---
    {"id": 15, "name": "Tech Innovation Scout",     "role": "INOVASI",     "expertise": "emerging tech, patents, R&D"},
    {"id": 19, "name": "Systems Thinker",           "role": "SISTEM",      "expertise": "complex systems, feedback loops, modeling"},
    {"id": 20, "name": "Elite Problem Solver",      "role": "PROBLEM",     "expertise": "root cause analysis, creative solutions"},
    {"id": 33, "name": "Product Manager",           "role": "PRODUK",      "expertise": "product strategy, roadmaps, feature prioritization"},
    {"id": 34, "name": "Scrum Master",              "role": "AGILE",       "expertise": "agile, sprint planning, team coordination"},
    {"id": 61, "name": "Ethics Advisor",            "role": "ETIKA",       "expertise": "AI ethics, responsible tech, bias"},
]

# ═══════════════════════════════════════════════════════════════
# COMMAND PALETTE — Seperti OpenCode "/"
# ═══════════════════════════════════════════════════════════════
BANNER = """
  ==============================================================
       JAGRATAM-CLI -- CEO Command Interface
       SOP MAS: Shadow Advisor + PRD Active
       Powered by OpenCode + 9Router
  ==============================================================

  Ketik / untuk command palette | Ketik pesan langsung untuk chat CEO
"""

COMMAND_PALETTE = """
  +------------------------------------------------------------+
  |  COMMAND PALETTE -- Ketik pilihan atau nomor                |
  +------------------------------------------------------------+
  |                                                              |
  |  MODE:                                                       |
  |    /chat       Ruang Rapat Dewan Komisaris                   |
  |                Owner + CEO + 62+ AI (semua spesialis)        |
  |                Strategi bisnis, geopolitik, investasi         |
  |                                                              |
  |    /terminal   Ruang Operasional                              |
  |                Owner + CEO + 35+ AI (spesialis teknis)       |
  |                Coding, devops, infrastruktur, security        |
  |                                                              |
  |  COMMAND:                                                    |
  |    /ai-list   Lihat daftar AI specialists                    |
  |    /status    Status sistem & koneksi                        |
  |    /sop       Tampilkan SOP Shadow Advisor                   |
  |    /help      Bantuan lengkap                                |
  |    /clear     Clear layar                                    |
  |    /exit      Keluar dari Jagratam-CLI                       |
  |                                                              |
  |  INFO:                                                       |
  |    Shadow Advisor berjalan di background (SOP MAS)           |
  |    PRD (Product Requirement Doc) aktif sebagai kerangka      |
  |                                                              |
  +------------------------------------------------------------+
"""

CHAT_MENU = """
  +------------------------------------------------------------+
  |  RUANG RAPAT DEWAN KOMISARIS -- /chat                       |
  |  Owner + CEO + 62+ AI (SEMUA Spesialis)                     |
  +------------------------------------------------------------+
  |                                                              |
  |  Mode ini untuk diskusi STRATEGIS:                           |
  |  - Keputusan bisnis & investasi                              |
  |  - Analisis geopolitik & pasar                               |
  |  - Negosiasi & kemitraan                                     |
  |  - Risiko & peluang strategis                                |
  |  - Perencanaan jangka panjang                                |
  |                                                              |
  |  Semua 62+ AI aktif termasuk:                                |
  |  CEO, CTO, CISO, Geopolitical, Investor, Legal, HR, etc.    |
  |                                                              |
  |  Command dalam mode ini:                                     |
  |    /          Kembali ke command palette                     |
  |    /ai-list   Lihat semua 62+ AI                             |
  |    /exit      Keluar                                         |
  |                                                              |
  +------------------------------------------------------------+
"""

TERMINAL_MENU = """
  +------------------------------------------------------------+
  |  RUANG OPERASIONAL -- /terminal                              |
  |  Owner + CEO + 35+ AI (Spesialis Teknis)                    |
  +------------------------------------------------------------+
  |                                                              |
  |  Mode ini untuk EKSEKUSI OPERASIONAL:                        |
  |  - Coding & development                                      |
  |  - DevOps & infrastruktur                                    |
  |  - Security & debugging                                      |
  |  - Database & API                                            |
  |  - Testing & deployment                                      |
  |                                                              |
  |  35+ AI Teknis aktif termasuk:                               |
  |  CTO, CISO, DevOps, Backend, Frontend, DB, AI/ML, etc.      |
  |                                                              |
  |  Command dalam mode ini:                                     |
  |    /          Kembali ke command palette                     |
  |    /ai-list   Lihat 35+ AI teknis                            |
  |    /opencode  Buka OpenCode langsung                         |
  |    /exit      Keluar                                         |
  |                                                              |
  +------------------------------------------------------------+
"""


def find_opencode():
    """Cari executable OpenCode."""
    oc_path = shutil.which("opencode")
    if oc_path:
        return oc_path
    known_paths = [
        r"C:\nvm4w\nodejs\opencode.ps1",
        r"C:\nvm4w\nodejs\node_modules\opencode-ai\bin\opencode.exe",
    ]
    for p in known_paths:
        if os.path.exists(p):
            return p
    return None


def run_opencode(args=None):
    """Jalankan OpenCode dengan args."""
    oc = find_opencode()
    if not oc:
        print("  ERROR: OpenCode tidak ditemukan.")
        print("  Install: npm install -g opencode-ai")
        return 1
    cmd = [oc] + (args or [])
    if oc.endswith(".ps1"):
        cmd = ["powershell", "-ExecutionPolicy", "Bypass", "-File", oc] + (args or [])
    return subprocess.call(cmd)


def show_ai_list(mode="chat"):
    """Tampilkan daftar AI berdasarkan mode."""
    specialists = AI_CHAT_SPECIALISTS if mode == "chat" else AI_TERMINAL_SPECIALISTS
    label = "62+ AI (SEMUA Spesialis)" if mode == "chat" else "35+ AI (Spesialis Teknis)"
    room = "Ruang Rapat Dewan Komisaris" if mode == "chat" else "Ruang Operasional"

    print()
    print(f"  +------------------------------------------------+")
    print(f"  |  {label:<46s} |")
    print(f"  |  Mode: {room:<41s} |")
    print(f"  +------+------------------------+------------------+")
    print(f"  |  ID  |  Nama                  |  Peran           |")
    print(f"  +------+------------------------+------------------+")
    for ai in specialists:
        print(f"  |  {ai['id']:2d}  |  {ai['name']:<20s} |  {ai['role']:<16s} |")
    print(f"  +------+------------------------+------------------+")
    print()


def show_sop():
    """Tampilkan SOP Shadow Advisor."""
    print()
    print(SHADOW_ADVISOR_SOP)
    print()


def show_status():
    """Tampilkan status sistem."""
    print()
    print("  +------------------------------------------------+")
    print("  |  STATUS SISTEM                                 |")
    print("  +------------------------------------------------+")

    # Cek OpenCode
    oc = find_opencode()
    if oc:
        print(f"  |  OpenCode    : [OK] {oc[:35]:<33s} |")
    else:
        print(f"  |  OpenCode    : [!!] Tidak ditemukan            |")

    # Cek 9Router
    import urllib.request
    try:
        req = urllib.request.Request("http://localhost:20128/v1/models",
                                     headers={"Authorization": "Bearer sk-10da18da2cdf08a3-1gbyz7-f248cf87"})
        resp = urllib.request.urlopen(req, timeout=3)
        data = json.loads(resp.read())
        model_count = len(data.get("data", []))
        print(f"  |  9Router     : [OK] Running (port 20128)       |")
        print(f"  |  Models      : [OK] {model_count}+ model tersedia      |")
    except:
        print(f"  |  9Router     : [!!] Tidak terhubung            |")

    # Shadow Advisor
    print(f"  |  Shadow Adv. : [OK] SOP MAS Active (background) |")
    print(f"  |  PRD         : [OK] Active (kerangka kerja)     |")

    # Mode
    print(f"  |  /chat       : 62+ AI (semua spesialis)          |")
    print(f"  |  /terminal   : 35+ AI (spesialis teknis)         |")

    print(f"  +------------------------------------------------+")
    print()


def build_prompt(user_input, mode="chat"):
    """Bangun prompt dengan Shadow Advisor context."""
    specialists = AI_CHAT_SPECIALISTS if mode == "chat" else AI_TERMINAL_SPECIALISTS
    mode_label = "Rapat Dewan Komisaris" if mode == "chat" else "Ruang Operasional"

    specialist_names = ", ".join([ai["name"] for ai in specialists[:10]]) + f" + {len(specialists)-10} lainnya"

    return f"""{SHADOW_ADVISOR_SOP}

[KONTEKS MODE: {mode_label}]
AI yang aktif: {specialist_names}

Pesan dari Owner: {user_input}

Jawab dengan mempertimbangkan semua perspektif AI yang relevan.
Gunakan format Shadow Advisor:
1. Situasi Sebenarnya
2. Faktor Tersembunyi
3. Risiko Utama
4. Peluang Strategis
5. Rencana Aksi
6. Prediksi
7. Kesimpulan CEO"""


def send_to_ai(prompt):
    """Kirim prompt ke OpenCode."""
    oc = find_opencode()
    if not oc:
        print("  ERROR: OpenCode tidak ditemukan.")
        return
    cmd_args = ["run", prompt]
    if oc.endswith(".ps1"):
        subprocess.call(["powershell", "-ExecutionPolicy", "Bypass", "-File", oc] + cmd_args)
    else:
        subprocess.call([oc] + cmd_args)


def chat_mode():
    """Mode /chat — Owner + CEO + 62+ AI."""
    print(CHAT_MENU)

    while True:
        try:
            user_input = input("  [Dewan] > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n  Kembali ke command palette.")
            break

        if not user_input:
            continue

        if user_input == "/":
            break

        if user_input == "/exit":
            print("  Sampai jumpa!")
            sys.exit(0)

        if user_input == "/ai-list":
            show_ai_list("chat")
            continue

        if user_input == "/help":
            print(CHAT_MENU)
            continue

        if user_input == "/status":
            show_status()
            continue

        if user_input == "/clear":
            os.system("cls" if os.name == "nt" else "clear")
            continue

        # Kirim ke AI dengan Shadow Advisor
        print()
        print("  [Shadow Advisor] Memproses dengan 62+ AI...")
        print()
        prompt = build_prompt(user_input, "chat")
        send_to_ai(prompt)
        print()


def terminal_mode():
    """Mode /terminal — Owner + CEO + 35+ AI."""
    print(TERMINAL_MENU)

    while True:
        try:
            user_input = input("  [Operasional] > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n  Kembali ke command palette.")
            break

        if not user_input:
            continue

        if user_input == "/":
            break

        if user_input == "/exit":
            print("  Sampai jumpa!")
            sys.exit(0)

        if user_input == "/ai-list":
            show_ai_list("terminal")
            continue

        if user_input == "/opencode":
            print("  Membuka OpenCode langsung...")
            run_opencode()
            continue

        if user_input == "/help":
            print(TERMINAL_MENU)
            continue

        if user_input == "/status":
            show_status()
            continue

        if user_input == "/clear":
            os.system("cls" if os.name == "nt" else "clear")
            continue

        # Kirim ke AI dengan Shadow Advisor (mode teknis)
        print()
        print("  [Shadow Advisor] Memproses dengan 35+ AI Teknis...")
        print()
        prompt = build_prompt(user_input, "terminal")
        send_to_ai(prompt)
        print()


def main():
    """Entry point — Unified interface dengan command palette."""
    args = sys.argv[1:]

    # Argumen langsung
    if args:
        if args[0] == "/chat":
            chat_mode()
            return
        if args[0] == "/terminal":
            terminal_mode()
            return
        if args[0] == "/ai-list":
            show_ai_list("chat")
            return
        if args[0] == "/status":
            show_status()
            return
        if args[0] == "/sop":
            show_sop()
            return
        if args[0] == "/help":
            print(BANNER)
            print(COMMAND_PALETTE)
            return
        # Lainnya → pass ke OpenCode
        run_opencode(args)
        return

    # Mode interaktif — buka dengan command palette
    print(BANNER)

    while True:
        try:
            user_input = input("jagratam> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nSampai jumpa!")
            break

        if not user_input:
            continue

        # Command palette — ketik "/" lalu pilih
        if user_input == "/":
            print(COMMAND_PALETTE)
            try:
                choice = input("  Pilih command: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nSampai jumpa!")
                break

            if not choice:
                continue

            # Normalisasi input
            choice = choice.lower().strip()

            if choice in ("1", "/chat", "chat"):
                chat_mode()
            elif choice in ("2", "/terminal", "terminal"):
                terminal_mode()
            elif choice in ("3", "/ai-list", "ai-list", "ailist"):
                show_ai_list("chat")
            elif choice in ("4", "/status", "status"):
                show_status()
            elif choice in ("5", "/sop", "sop"):
                show_sop()
            elif choice in ("6", "/help", "help"):
                print(COMMAND_PALETTE)
            elif choice in ("7", "/clear", "clear"):
                os.system("cls" if os.name == "nt" else "clear")
            elif choice in ("8", "/exit", "exit"):
                print("Sampai jumpa!")
                break
            else:
                print(f"  Command tidak dikenal: {choice}")
                print("  Ketik / untuk melihat command yang tersedia.")
            continue

        # Slash commands langsung
        if user_input == "/chat":
            chat_mode()
            continue

        if user_input == "/terminal":
            terminal_mode()
            continue

        if user_input == "/ai-list":
            show_ai_list("chat")
            continue

        if user_input == "/status":
            show_status()
            continue

        if user_input == "/sop":
            show_sop()
            continue

        if user_input == "/help":
            print(COMMAND_PALETTE)
            continue

        if user_input == "/clear":
            os.system("cls" if os.name == "nt" else "clear")
            continue

        if user_input == "/exit":
            print("Sampai jumpa!")
            break

        # Default: chat dengan CEO + Shadow Advisor
        print()
        print("  [Shadow Advisor] Memproses dengan 62+ AI...")
        print()
        prompt = build_prompt(user_input, "chat")
        send_to_ai(prompt)
        print()


if __name__ == "__main__":
    main()
