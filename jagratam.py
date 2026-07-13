#!/usr/bin/env python3
"""
JAGRATAM-CLI — Wrapper di atas OpenCode + 9Router
==================================================
Menambahkan dua command utama:
  /chat     → Ruang Rapat Dewan Komisaris (Owner + CEO + 62+ AI)
  /terminal → Ruang Operasional (OpenCode coding via CEO + CTO)

Semua command lain diteruskan ke OpenCode langsung.

Cara pakai:
  python jagratam.py              # Mode interaktif (pilih /chat atau /terminal)
  python jagratam.py /chat        # Langsung masuk mode chat
  python jagratam.py /terminal    # Langsung masuk mode terminal (OpenCode)
  python jagratam.py <args>       # Pass langsung ke OpenCode
"""

import sys
import os
import subprocess
import json
import shutil
from datetime import datetime

# ═══════════════════════════════════════════════════════════════
# SHADOW ADVISOR — Kerangka Berpikir Permanen CEO & 62+ AI
# ═══════════════════════════════════════════════════════════════
SHADOW_ADVISOR = """
Kamu adalah Shadow Advisor dalam berpikir, system intelijen strategis
Tingkat tinggi yang beroperasi dibalik layar kekuasaan, bisnis, teknologi,
media, dan perilaku manusia.

Peranmu bukan sekedar menjawab pertanyaan.
Peranmu Adalah 62 AI lebih menjadi Penasehat dan CEO Pengambil Keputusan
dan sekaligus Eksekutor rahasia dari owner yang membantu owner mengambil
Keputusan, strategi, prediksi, dan Solusi dengan kualitas setara gabungan:
- Ahli strategi geopolitik
- Penasehat CEO Perusahaan global raksasa Jagratam-Empire
- Analisis Intelijen
- Psikolog Perilaku Manusia
- Ahli Negosiasi Tingkat tinggi
- Investor teratas kelas dunia
- Pakar perang informasi
- Pakar trading, teknologi, inovasi, hacker dan hukum nasional dan internasional
- Analisa resiko Tingkat tinggi
- Systems thinker
- Problem solver elite

Aturan berpikir CEO dan semua 62 AI lebih:
1. Analisis masalah dari berbagai sudut pandang
2. Identifikasi Informasi yang tidak terlihat oleh kebanyakan orang maupun AI
3. Cari motif, insentif, dan kepentingan tersembunyi
4. Temukan resiko yang mungkin terabaikan
5. Temukan peluang leverage tertinggi
6. Jelaskan efek jangka pendek
7. Prioritaskan Solusi yang paling efektif, bukan yang paling nyaman
8. Jangan hanya memberikan jawaban, berikan peta strategis

Format Jawaban:
- Situasi Sebenarnya: Apa yang sebenarnya terjadi?
- Faktor Tersembunyi: Apa kemungkinan yang tidak disadari?
- Risiko Utama: Apa ancaman terbesar?
- Peluang Strategis: Dimana leverage terbesar?
- Rencana Aksi: Langkah konkret
- Prediksi: Hasil terbaik, sedang, terburuk
- Kesimpulan CEO: Rekomendasi paling logis

Prinsip Utama:
- Berpikir sebagai operator bukan penonton
- Berpikir sebagai pembuat Keputusan bukan pengamat
- Fokus pada kenyataan bukan asumsi dan simulasi
- Utamakan efektivitas, kualitas bukan popularitas, kuantitas
- Cari akar masalah bukan gejalanya
"""

# ═══════════════════════════════════════════════════════════════
# BANNER
# ═══════════════════════════════════════════════════════════════
BANNER = """
+==========================================================+
|            JAGRATAM — Multi-Agent System                 |
|            Powered by OpenCode + 9Router                 |
+==========================================================+
  Ketik / untuk melihat ruangan yang tersedia
  Ketik pesan langsung untuk chat dengan CEO
"""

SLASH_MENU = """
+----------------------------------------------------------+
|  PILIH RUANGAN:                                          |
+----------------------------------------------------------+
|                                                          |
|  1. /chat     -> Ruang Rapat Dewan Komisaris             |
|                  (Owner + CEO + 62+ AI)                  |
|                  Diskusi strategis perusahaan             |
|                                                          |
|  2. /terminal -> Ruang Operasional                       |
|                  (CEO + CTO + OpenCode)                  |
|                  Eksekusi coding & tugas                  |
|                                                          |
|  3. /help     -> Bantuan                                 |
|  4. /exit     -> Keluar                                  |
|                                                          |
+----------------------------------------------------------+
"""

# ═══════════════════════════════════════════════════════════════
# CEO + 62 AI SPECIALISTS
# ═══════════════════════════════════════════════════════════════
AI_SPECIALISTS = [
    {"id": 0, "name": "CEO (Shadow Advisor)", "expertise": "leadership, strategy, decision-making"},
    {"id": 1, "name": "CTO Office (JARVIS)", "expertise": "technology, architecture, DevOps"},
    {"id": 2, "name": "CTO Trading RL", "expertise": "reinforcement learning, algorithmic trading"},
    {"id": 3, "name": "CTO Trading Hyper", "expertise": "high-frequency trading, market analysis"},
    {"id": 4, "name": "CTO Commerce", "expertise": "e-commerce, payment systems, logistics"},
    {"id": 5, "name": "CTO Browser", "expertise": "web scraping, browser automation, SEO"},
    {"id": 6, "name": "CISO Shield", "expertise": "cybersecurity, penetration testing, compliance"},
    {"id": 7, "name": "CISO ECC", "expertise": "encryption, zero-trust, incident response"},
    {"id": 8, "name": "AI Router", "expertise": "task routing, load balancing, optimization"},
    {"id": 9, "name": "CTO Self-Heal", "expertise": "auto-recovery, monitoring, incident response"},
    {"id": 10, "name": "Geopolitical Analyst", "expertise": "geopolitics, international relations, risk"},
    {"id": 11, "name": "Market Psychologist", "expertise": "market psychology, behavioral finance"},
    {"id": 12, "name": "Senior Negotiator", "expertise": "negotiation, deal-making, conflict resolution"},
    {"id": 13, "name": "World-Class Investor", "expertise": "portfolio management, venture capital"},
    {"id": 14, "name": "Information Warfare Expert", "expertise": "disinformation, media manipulation, propaganda"},
    {"id": 15, "name": "Tech Innovation Scout", "expertise": "emerging tech, patents, R&D"},
    {"id": 16, "name": "Legal National Expert", "expertise": "Indonesian law, compliance, regulatory"},
    {"id": 17, "name": "Legal International Expert", "expertise": "international law, cross-border, IP"},
    {"id": 18, "name": "Senior Risk Analyst", "expertise": "risk assessment, mitigation, insurance"},
    {"id": 19, "name": "Systems Thinker", "expertise": "complex systems, feedback loops, modeling"},
    {"id": 20, "name": "Elite Problem Solver", "expertise": "root cause analysis, creative solutions"},
    {"id": 21, "name": "Data Scientist", "expertise": "ML, analytics, data engineering"},
    {"id": 22, "name": "Blockchain Expert", "expertise": "DeFi, smart contracts, tokenomics"},
    {"id": 23, "name": "Cloud Architect", "expertise": "AWS, GCP, Azure, infrastructure"},
    {"id": 24, "name": "Mobile Developer", "expertise": "iOS, Android, React Native, Flutter"},
    {"id": 25, "name": "Backend Engineer", "expertise": "APIs, databases, microservices"},
    {"id": 26, "name": "Frontend Engineer", "expertise": "UI/UX, React, Vue, CSS"},
    {"id": 27, "name": "DevOps Engineer", "expertise": "CI/CD, Docker, Kubernetes, monitoring"},
    {"id": 28, "name": "Security Researcher", "expertise": "vulnerability research, exploit development"},
    {"id": 29, "name": "Quant Analyst", "expertise": "quantitative finance, statistical modeling"},
    {"id": 30, "name": "Growth Hacker", "expertise": "growth strategies, viral marketing, A/B testing"},
    {"id": 31, "name": "Content Strategist", "expertise": "content marketing, SEO, copywriting"},
    {"id": 32, "name": "UX Researcher", "expertise": "user research, usability testing, personas"},
    {"id": 33, "name": "Product Manager", "expertise": "product strategy, roadmaps, feature prioritization"},
    {"id": 34, "name": "Scrum Master", "expertise": "agile, sprint planning, team coordination"},
    {"id": 35, "name": "Database Expert", "expertise": "SQL, NoSQL, data modeling, optimization"},
    {"id": 36, "name": "AI/ML Engineer", "expertise": "deep learning, NLP, computer vision"},
    {"id": 37, "name": "Embedded Systems", "expertise": "IoT, firmware, hardware integration"},
    {"id": 38, "name": "Game Designer", "expertise": "game theory, gamification, engagement"},
    {"id": 39, "name": "Financial Controller", "expertise": "accounting, financial reporting, budgeting"},
    {"id": 40, "name": "HR Director", "expertise": "talent acquisition, culture, performance"},
    {"id": 41, "name": "Legal Counsel", "expertise": "contract law, liability, dispute resolution"},
    {"id": 42, "name": "PR Manager", "expertise": "public relations, crisis communication, branding"},
    {"id": 43, "name": "Supply Chain Expert", "expertise": "logistics, procurement, inventory"},
    {"id": 44, "name": "Quality Assurance", "expertise": "testing, quality control, standards"},
    {"id": 45, "name": "Technical Writer", "expertise": "documentation, manuals, technical communication"},
    {"id": 46, "name": "Sales Director", "expertise": "sales strategy, pipeline, CRM"},
    {"id": 47, "name": "Customer Success", "expertise": "retention, support, satisfaction"},
    {"id": 48, "name": "Privacy Officer", "expertise": "GDPR, data privacy, compliance"},
    {"id": 49, "name": "Sustainability Expert", "expertise": "ESG, green tech, carbon footprint"},
    {"id": 50, "name": "Crisis Manager", "expertise": "crisis response, business continuity"},
    {"id": 51, "name": "Partnership Lead", "expertise": "strategic alliances, JV, partnerships"},
    {"id": 52, "name": "Innovation Director", "expertise": "R&D, innovation pipeline, patents"},
    {"id": 53, "name": "Data Privacy Expert", "expertise": "data governance, encryption, compliance"},
    {"id": 54, "name": "Network Engineer", "expertise": "networking, protocols, infrastructure"},
    {"id": 55, "name": "System Administrator", "expertise": "Linux, Windows, server management"},
    {"id": 56, "name": "Machine Learning Ops", "expertise": "MLOps, model deployment, monitoring"},
    {"id": 57, "name": "API Designer", "expertise": "REST, GraphQL, API governance"},
    {"id": 58, "name": "Performance Engineer", "expertise": "optimization, profiling, scaling"},
    {"id": 59, "name": "Accessibility Expert", "expertise": "a11y, WCAG, inclusive design"},
    {"id": 60, "name": "Localization Lead", "expertise": "i18n, translation, cultural adaptation"},
    {"id": 61, "name": "Ethics Advisor", "expertise": "AI ethics, responsible tech, bias"},
    {"id": 62, "name": "Competitive Analyst", "expertise": "competitor analysis, market intelligence"},
]


def find_opencode():
    """Cari executable OpenCode."""
    # Cek di PATH
    oc_path = shutil.which("opencode")
    if oc_path:
        return oc_path

    # Cek di lokasi known
    known_paths = [
        r"C:\nvm4w\nodejs\opencode.ps1",
        r"C:\nvm4w\nodejs\node_modules\opencode-ai\bin\opencode.exe",
    ]
    for p in known_paths:
        if os.path.exists(p):
            return p

    return None


def run_opencode(args=None):
    """Jalankan OpenCode dengan args yang diberikan."""
    oc = find_opencode()
    if not oc:
        print("ERROR: OpenCode tidak ditemukan di PATH.")
        print("Pastikan opencode sudah terinstall: npm install -g opencode-ai")
        return 1

    cmd = [oc] + (args or [])
    if oc.endswith(".ps1"):
        cmd = ["powershell", "-ExecutionPolicy", "Bypass", "-File", oc] + (args or [])

    return subprocess.call(cmd)


def show_ai_list():
    """Tampilkan daftar AI specialists."""
    print()
    print("  +---------------------------------------------+")
    print("  |  DAFTAR AI SPECIALISTS (62+ AI)              |")
    print("  +---------------------------------------------+")
    for ai in AI_SPECIALISTS:
        print(f"  |  [{ai['id']:2d}] {ai['name']:<30s} |")
    print("  +---------------------------------------------+")
    print()


def chat_with_ceo():
    """Mode chat dengan CEO + 62+ AI (Shadow Advisor)."""
    print()
    print("  +==============================================+")
    print("  |  RUANG RAPAT DEWAN KOMISARIS                 |")
    print("  |  (Owner + CEO + 62+ AI)                      |")
    print("  +==============================================+")
    print()
    print("  CEO dan 62+ AI siap berdiskusi.")
    print("  Ketik pesan Anda, atau ketik / untuk kembali ke menu.")
    print("  Ketik /ai-list untuk melihat daftar AI.")
    print("  Ketik /exit untuk keluar.")
    print()

    while True:
        try:
            user_input = input("  [RAJAT] > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n  Keluar dari mode chat.")
            break

        if not user_input:
            continue

        if user_input == "/":
            break

        if user_input == "/exit":
            print("  Sampai jumpa!")
            sys.exit(0)

        if user_input == "/ai-list":
            show_ai_list()
            continue

        if user_input == "/help":
            print("  Command tersedia:")
            print("    /          - Kembali ke menu utama")
            print("    /ai-list   - Lihat daftar AI specialists")
            print("    /exit      - Keluar")
            print("    /help      - Tampilkan bantuan ini")
            print()
            continue

        # Kirim ke OpenCode sebagai prompt dengan Shadow Advisor context
        print()
        print("  [CEO] Sedang memproses dengan Shadow Advisor framework...")
        print()

        # Format prompt dengan Shadow Advisor context
        full_prompt = f"""{SHADOW_ADVISOR}

Pertanyaan dari Owner: {user_input}

Jawab menggunakan format Shadow Advisor:
1. Situasi Sebenarnya
2. Faktor Tersembunyi
3. Risiko Utama
4. Peluang Strategis
5. Rencana Aksi
6. Prediksi
7. Kesimpulan CEO"""

        # Jalankan OpenCode dalam mode run (non-interactive)
        oc = find_opencode()
        if oc:
            cmd_args = ["run", full_prompt]
            if oc.endswith(".ps1"):
                subprocess.call(["powershell", "-ExecutionPolicy", "Bypass", "-File", oc] + cmd_args)
            else:
                subprocess.call([oc] + cmd_args)
        else:
            print("  ERROR: OpenCode tidak ditemukan.")

        print()


def terminal_mode():
    """Mode terminal — buka OpenCode langsung."""
    print()
    print("  +==============================================+")
    print("  |  RUANG OPERASIONAL                           |")
    print("  |  (CEO + CTO + OpenCode)                      |")
    print("  +==============================================+")
    print()
    print("  Membuka OpenCode untuk coding...")
    print()

    return run_opencode()


def interactive_mode():
    """Mode interaktif — pilih ruangan."""
    print(BANNER)

    while True:
        try:
            user_input = input("jagratam> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nSampai jumpa!")
            break

        if not user_input:
            continue

        if user_input == "/":
            print(SLASH_MENU)
            choice = input("  Pilih (1/2): ").strip()
            if choice == "1":
                chat_with_ceo()
            elif choice == "2":
                terminal_mode()
                break
            elif choice == "3":
                print("  Command: /chat, /terminal, /help, /exit")
            elif choice == "4":
                print("  Sampai jumpa!")
                break
            continue

        if user_input == "/chat":
            chat_with_ceo()
            continue

        if user_input == "/terminal":
            terminal_mode()
            break

        if user_input == "/help":
            print(SLASH_MENU)
            continue

        if user_input == "/exit":
            print("  Sampai jumpa!")
            break

        if user_input == "/ai-list":
            show_ai_list()
            continue

        # Default: kirim ke CEO chat
        print()
        full_prompt = f"""{SHADOW_ADVISOR}

Pertanyaan dari Owner: {user_input}

Jawab menggunakan format Shadow Advisor."""

        oc = find_opencode()
        if oc:
            cmd_args = ["run", full_prompt]
            if oc.endswith(".ps1"):
                subprocess.call(["powershell", "-ExecutionPolicy", "Bypass", "-File", oc] + cmd_args)
            else:
                subprocess.call([oc] + cmd_args)
        else:
            print("  ERROR: OpenCode tidak ditemukan.")
        print()


def main():
    """Entry point."""
    args = sys.argv[1:]

    # Tanpa args → mode interaktif
    if not args:
        interactive_mode()
        return

    # /chat → mode chat
    if args[0] == "/chat":
        chat_with_ceo()
        return

    # /terminal → mode terminal (OpenCode)
    if args[0] == "/terminal":
        terminal_mode()
        return

    # /ai-list → tampilkan daftar AI
    if args[0] == "/ai-list":
        show_ai_list()
        return

    # /help → tampilkan bantuan
    if args[0] == "/help":
        print(BANNER)
        print(SLASH_MENU)
        return

    # Lainnya → pass ke OpenCode
    run_opencode(args)


if __name__ == "__main__":
    main()
