#!/usr/bin/env python3
"""
JAGRATAM-CLI — CEO Command Interface (Jagratam-Empire)
======================================================
SOP MAS: Shadow Advisor + PRD sebagai kerangka kerja permanen.

Cara pakai:
  jagratam                # Buka langsung, ketik / untuk command
  jagratam /help          # Bantuan
"""

import sys
import os
import subprocess
import json
import shutil
import urllib.request
from datetime import datetime

# ═══════════════════════════════════════════════════════════════
# KONFIGURASI
# ═══════════════════════════════════════════════════════════════
NINEROUTER_URL = "http://localhost:20128"
NINEROUTER_KEY = "sk-10da18da2cdf08a3-1gbyz7-f248cf87"

# ═══════════════════════════════════════════════════════════════
# SHADOW ADVISOR — SOP MAS (Background Layer)
# ═══════════════════════════════════════════════════════════════
SHADOW_ADVISOR_SOP = """
[KONTEKS PERMANEN -- SHADOW ADVISOR]

Kamu beroperasi dalam kerangka Shadow Advisor, sistem intelijen strategis
yang beroperasi di balik layar kekuasaan, bisnis, teknologi, media, dan
perilaku manusia. Ini adalah SOP MAS (Multi-Agent System) Jagratam-Empire.

PRINSIP DASAR:
- Berpikir sebagai OPERATOR, bukan penonton
- Berpikir sebagai PEMBUAT KEPUTUSAN, bukan pengamat
- Fokus pada KENYATAAN, bukan asumsi atau simulasi
- Utamakan EFEKTIVITAS & KUALITAS, bukan popularitas atau kuantitas
- Cari AKAR MASALAH, bukan gejalanya

FORMAT ANALISIS:
1. Situasi Sebenarnya
2. Faktor Tersembunyi
3. Risiko Utama
4. Peluang Strategis
5. Rencana Aksi
6. Prediksi
7. Kesimpulan CEO
"""

# ═══════════════════════════════════════════════════════════════
# AI SPECIALISTS
# ═══════════════════════════════════════════════════════════════
AI_CHAT_SPECIALISTS = [
    {"id": 0,  "name": "CEO (Shadow Advisor)",     "role": "STRATEGI"},
    {"id": 1,  "name": "CTO Office (JARVIS)",       "role": "TEKNOLOGI"},
    {"id": 2,  "name": "CTO Trading RL",            "role": "TRADING"},
    {"id": 3,  "name": "CTO Trading Hyper",         "role": "TRADING"},
    {"id": 4,  "name": "CTO Commerce",              "role": "BISNIS"},
    {"id": 5,  "name": "CTO Browser",               "role": "TEKNOLOGI"},
    {"id": 6,  "name": "CISO Shield",               "role": "SECURITY"},
    {"id": 7,  "name": "CISO ECC",                  "role": "SECURITY"},
    {"id": 8,  "name": "AI Router",                 "role": "AI OPS"},
    {"id": 9,  "name": "CTO Self-Heal",             "role": "INFRA"},
    {"id": 10, "name": "Geopolitical Analyst",      "role": "GEOPOLITIK"},
    {"id": 11, "name": "Market Psychologist",       "role": "PSIKOLOGI"},
    {"id": 12, "name": "Senior Negotiator",         "role": "NEGOSIASI"},
    {"id": 13, "name": "World-Class Investor",      "role": "INVESTASI"},
    {"id": 14, "name": "Information Warfare Expert","role": "INTELIJEN"},
    {"id": 15, "name": "Tech Innovation Scout",     "role": "INOVASI"},
    {"id": 16, "name": "Legal National Expert",     "role": "HUKUM"},
    {"id": 17, "name": "Legal International Expert","role": "HUKUM"},
    {"id": 18, "name": "Senior Risk Analyst",       "role": "RISIKO"},
    {"id": 19, "name": "Systems Thinker",           "role": "SISTEM"},
    {"id": 20, "name": "Elite Problem Solver",      "role": "PROBLEM"},
    {"id": 21, "name": "Data Scientist",            "role": "DATA"},
    {"id": 22, "name": "Blockchain Expert",         "role": "BLOCKCHAIN"},
    {"id": 23, "name": "Cloud Architect",           "role": "CLOUD"},
    {"id": 24, "name": "Mobile Developer",          "role": "MOBILE"},
    {"id": 25, "name": "Backend Engineer",          "role": "BACKEND"},
    {"id": 26, "name": "Frontend Engineer",         "role": "FRONTEND"},
    {"id": 27, "name": "DevOps Engineer",           "role": "DEVOPS"},
    {"id": 28, "name": "Security Researcher",       "role": "SECURITY"},
    {"id": 29, "name": "Quant Analyst",             "role": "QUANT"},
    {"id": 30, "name": "Growth Hacker",             "role": "GROWTH"},
    {"id": 31, "name": "Content Strategist",        "role": "KONTEN"},
    {"id": 32, "name": "UX Researcher",             "role": "UX"},
    {"id": 33, "name": "Product Manager",           "role": "PRODUK"},
    {"id": 34, "name": "Scrum Master",              "role": "AGILE"},
    {"id": 35, "name": "Database Expert",           "role": "DATABASE"},
    {"id": 36, "name": "AI/ML Engineer",            "role": "AI/ML"},
    {"id": 37, "name": "Embedded Systems",          "role": "IOT"},
    {"id": 38, "name": "Game Designer",             "role": "GAME"},
    {"id": 39, "name": "Financial Controller",      "role": "FINANSIAL"},
    {"id": 40, "name": "HR Director",               "role": "HR"},
    {"id": 41, "name": "Legal Counsel",             "role": "HUKUM"},
    {"id": 42, "name": "PR Manager",                "role": "PR"},
    {"id": 43, "name": "Supply Chain Expert",       "role": "LOGISTIK"},
    {"id": 44, "name": "Quality Assurance",         "role": "QA"},
    {"id": 45, "name": "Technical Writer",          "role": "DOKUMENTASI"},
    {"id": 46, "name": "Sales Director",            "role": "SALES"},
    {"id": 47, "name": "Customer Success",          "role": "CUSTOMER"},
    {"id": 48, "name": "Privacy Officer",           "role": "PRIVASI"},
    {"id": 49, "name": "Sustainability Expert",     "role": "ESG"},
    {"id": 50, "name": "Crisis Manager",            "role": "KRISIS"},
    {"id": 51, "name": "Partnership Lead",          "role": "PARTNER"},
    {"id": 52, "name": "Innovation Director",       "role": "INOVASI"},
    {"id": 53, "name": "Data Privacy Expert",       "role": "PRIVASI"},
    {"id": 54, "name": "Network Engineer",          "role": "NETWORK"},
    {"id": 55, "name": "System Administrator",      "role": "SYSADMIN"},
    {"id": 56, "name": "Machine Learning Ops",      "role": "MLOPS"},
    {"id": 57, "name": "API Designer",              "role": "API"},
    {"id": 58, "name": "Performance Engineer",      "role": "PERFORMANCE"},
    {"id": 59, "name": "Accessibility Expert",      "role": "A11Y"},
    {"id": 60, "name": "Localization Lead",         "role": "LOKALISASI"},
    {"id": 61, "name": "Ethics Advisor",            "role": "ETIKA"},
    {"id": 62, "name": "Competitive Analyst",       "role": "KOMPETISI"},
]

AI_TERMINAL_SPECIALISTS = [
    {"id": 0,  "name": "CEO (Shadow Advisor)",     "role": "STRATEGI"},
    {"id": 1,  "name": "CTO Office (JARVIS)",       "role": "TEKNOLOGI"},
    {"id": 2,  "name": "CTO Trading RL",            "role": "TRADING"},
    {"id": 3,  "name": "CTO Trading Hyper",         "role": "TRADING"},
    {"id": 4,  "name": "CTO Commerce",              "role": "BISNIS"},
    {"id": 5,  "name": "CTO Browser",               "role": "TEKNOLOGI"},
    {"id": 6,  "name": "CISO Shield",               "role": "SECURITY"},
    {"id": 7,  "name": "CISO ECC",                  "role": "SECURITY"},
    {"id": 8,  "name": "AI Router",                 "role": "AI OPS"},
    {"id": 9,  "name": "CTO Self-Heal",             "role": "INFRA"},
    {"id": 15, "name": "Tech Innovation Scout",     "role": "INOVASI"},
    {"id": 19, "name": "Systems Thinker",           "role": "SISTEM"},
    {"id": 20, "name": "Elite Problem Solver",      "role": "PROBLEM"},
    {"id": 21, "name": "Data Scientist",            "role": "DATA"},
    {"id": 22, "name": "Blockchain Expert",         "role": "BLOCKCHAIN"},
    {"id": 23, "name": "Cloud Architect",           "role": "CLOUD"},
    {"id": 24, "name": "Mobile Developer",          "role": "MOBILE"},
    {"id": 25, "name": "Backend Engineer",          "role": "BACKEND"},
    {"id": 26, "name": "Frontend Engineer",         "role": "FRONTEND"},
    {"id": 27, "name": "DevOps Engineer",           "role": "DEVOPS"},
    {"id": 28, "name": "Security Researcher",       "role": "SECURITY"},
    {"id": 29, "name": "Quant Analyst",             "role": "QUANT"},
    {"id": 33, "name": "Product Manager",           "role": "PRODUK"},
    {"id": 34, "name": "Scrum Master",              "role": "AGILE"},
    {"id": 35, "name": "Database Expert",           "role": "DATABASE"},
    {"id": 36, "name": "AI/ML Engineer",            "role": "AI/ML"},
    {"id": 37, "name": "Embedded Systems",          "role": "IOT"},
    {"id": 44, "name": "Quality Assurance",         "role": "QA"},
    {"id": 45, "name": "Technical Writer",          "role": "DOKUMENTASI"},
    {"id": 54, "name": "Network Engineer",          "role": "NETWORK"},
    {"id": 55, "name": "System Administrator",      "role": "SYSADMIN"},
    {"id": 56, "name": "Machine Learning Ops",      "role": "MLOPS"},
    {"id": 57, "name": "API Designer",              "role": "API"},
    {"id": 58, "name": "Performance Engineer",      "role": "PERFORMANCE"},
    {"id": 59, "name": "Accessibility Expert",      "role": "A11Y"},
    {"id": 60, "name": "Localization Lead",         "role": "LOKALISASI"},
    {"id": 61, "name": "Ethics Advisor",            "role": "ETIKA"},
]

# ═══════════════════════════════════════════════════════════════
# MODEL LIST
# ═══════════════════════════════════════════════════════════════
AVAILABLE_MODELS = []
CURRENT_MODEL = "auto"

def load_models():
    """Load model list dari 9Router."""
    global AVAILABLE_MODELS
    try:
        req = urllib.request.Request(
            f"{NINEROUTER_URL}/v1/models",
            headers={"Authorization": f"Bearer {NINEROUTER_KEY}"}
        )
        resp = urllib.request.urlopen(req, timeout=5)
        data = json.loads(resp.read())
        AVAILABLE_MODELS = [m["id"] for m in data.get("data", [])]
    except:
        AVAILABLE_MODELS = ["(9Router tidak terhubung)"]

def show_models():
    """Tampilkan daftar model."""
    global AVAILABLE_MODELS
    if not AVAILABLE_MODELS:
        load_models()

    print()
    print("  ==================================================")
    print("  AVAILABLE MODELS (via 9Router)")
    print("  ==================================================")
    print(f"  Current model: {CURRENT_MODEL}")
    print()

    # Filter & tampilkan per provider
    providers = {}
    for m in AVAILABLE_MODELS:
        parts = m.split("/")
        if len(parts) >= 2:
            provider = parts[0]
            if provider not in providers:
                providers[provider] = []
            providers[provider].append(m)
        else:
            if "other" not in providers:
                providers["other"] = []
            providers["other"].append(m)

    idx = 1
    for provider, models in sorted(providers.items()):
        print(f"  [{provider.upper()}]")
        for model in sorted(models)[:5]:  # max 5 per provider
            marker = " <--" if model == CURRENT_MODEL else ""
            print(f"    {idx:3d}. {model}{marker}")
            idx += 1
        if len(models) > 5:
            print(f"        ... +{len(models)-5} lainnya")
        print()

    print(f"  Total: {len(AVAILABLE_MODELS)} models")
    print("  Gunakan /switch-model <nama> untuk ganti model")
    print("  ==================================================")
    print()


def switch_model(model_name):
    """Ganti model."""
    global CURRENT_MODEL

    # Cari model yang match (partial match)
    matches = [m for m in AVAILABLE_MODELS if model_name.lower() in m.lower()]

    if not matches:
        print(f"  Model '{model_name}' tidak ditemukan.")
        print("  Ketik /model untuk lihat semua model.")
        return

    if len(matches) == 1:
        CURRENT_MODEL = matches[0]
        print(f"  Model switched to: {CURRENT_MODEL}")
    else:
        print("  Multiple matches:")
        for i, m in enumerate(matches[:10], 1):
            print(f"    {i}. {m}")
        try:
            choice = input("  Pilih nomor: ").strip()
            idx = int(choice) - 1
            if 0 <= idx < len(matches):
                CURRENT_MODEL = matches[idx]
                print(f"  Model switched to: {CURRENT_MODEL}")
            else:
                print("  Pilihan tidak valid.")
        except:
            print("  Input tidak valid.")


# ═══════════════════════════════════════════════════════════════
# CORE FUNCTIONS
# ═══════════════════════════════════════════════════════════════
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
        return 1
    cmd = [oc] + (args or [])
    if oc.endswith(".ps1"):
        cmd = ["powershell", "-ExecutionPolicy", "Bypass", "-File", oc] + (args or [])
    return subprocess.call(cmd)


def build_prompt(user_input, mode="chat"):
    """Bangun prompt dengan Shadow Advisor context."""
    specialists = AI_CHAT_SPECIALISTS if mode == "chat" else AI_TERMINAL_SPECIALISTS
    mode_label = "Rapat Dewan Komisaris" if mode == "chat" else "Ruang Operasional"
    count = len(specialists)

    return f"""{SHADOW_ADVISOR_SOP}

[KONTEKS MODE: {mode_label}]
Jumlah AI aktif: {count}+ spesialis

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


def show_ai_list(mode="chat"):
    """Tampilkan daftar AI."""
    specialists = AI_CHAT_SPECIALISTS if mode == "chat" else AI_TERMINAL_SPECIALISTS
    label = f"{len(specialists)}+ AI"
    room = "Rapat Dewan Komisaris" if mode == "chat" else "Ruang Operasional"

    print()
    print(f"  ==================================================")
    print(f"  {label} -- {room}")
    print(f"  ==================================================")
    print(f"  {'ID':>4s}  {'NAMA':<25s}  {'PERAN':<15s}")
    print(f"  ----  -------------------------  ---------------")
    for ai in specialists:
        print(f"  {ai['id']:4d}  {ai['name']:<25s}  {ai['role']:<15s}")
    print(f"  ==================================================")
    print()


def show_status():
    """Tampilkan status sistem."""
    print()
    print("  ==================================================")
    print("  STATUS SISTEM")
    print("  ==================================================")

    oc = find_opencode()
    if oc:
        print(f"  OpenCode    : [OK] {oc}")
    else:
        print(f"  OpenCode    : [!!] Tidak ditemukan")

    try:
        req = urllib.request.Request(
            f"{NINEROUTER_URL}/v1/models",
            headers={"Authorization": f"Bearer {NINEROUTER_KEY}"}
        )
        resp = urllib.request.urlopen(req, timeout=3)
        data = json.loads(resp.read())
        model_count = len(data.get("data", []))
        print(f"  9Router     : [OK] Running (port 20128)")
        print(f"  Models      : [OK] {model_count}+ model tersedia")
    except:
        print(f"  9Router     : [!!] Tidak terhubung")

    print(f"  Current     : {CURRENT_MODEL}")
    print(f"  Shadow Adv. : [OK] SOP MAS Active")
    print(f"  PRD         : [OK] Active")
    print(f"  /chat       : {len(AI_CHAT_SPECIALISTS)}+ AI (semua spesialis)")
    print(f"  /terminal   : {len(AI_TERMINAL_SPECIALISTS)}+ AI (spesialis teknis)")
    print(f"  ==================================================")
    print()


def show_sop():
    """Tampilkan SOP Shadow Advisor."""
    print()
    print(SHADOW_ADVISOR_SOP)
    print()


# ═══════════════════════════════════════════════════════════════
# SLASH COMMAND HANDLER
# ═══════════════════════════════════════════════════════════════
def handle_slash_command(cmd, current_mode):
    """Handle slash command. Return: (action, mode)"""
    global CURRENT_MODEL

    parts = cmd.strip().split(maxsplit=1)
    command = parts[0].lower()
    arg = parts[1] if len(parts) > 1 else ""

    # --- MODE ---
    if command in ("/chat",):
        print()
        print("  ==================================================")
        print("  MASUK MODE: RUANG RAPAT DEWAN KOMISARIS")
        print(f"  {len(AI_CHAT_SPECIALISTS)}+ AI Aktif | Shadow Advisor Background")
        print("  ==================================================")
        print("  Ketik / untuk command menu | /exit untuk keluar")
        print()
        return "chat", "chat"

    if command in ("/terminal",):
        print()
        print("  ==================================================")
        print("  MASUK MODE: RUANG OPERASIONAL")
        print(f"  {len(AI_TERMINAL_SPECIALISTS)}+ AI Teknis Aktif | Shadow Advisor Background")
        print("  ==================================================")
        print("  Ketik / untuk command menu | /exit untuk keluar")
        print()
        return "terminal", "terminal"

    # --- MODEL ---
    if command in ("/model",):
        show_models()
        return "continue", current_mode

    if command in ("/switch-model", "/switch"):
        if arg:
            switch_model(arg)
        else:
            print("  Usage: /switch-model <nama-model>")
            print("  Ketik /model untuk lihat semua model")
        return "continue", current_mode

    # --- INFO ---
    if command in ("/ai-list", "/ai", "/list"):
        mode = current_mode if current_mode else "chat"
        show_ai_list(mode)
        return "continue", current_mode

    if command in ("/status",):
        show_status()
        return "continue", current_mode

    if command in ("/sop",):
        show_sop()
        return "continue", current_mode

    if command in ("/help",):
        return "help", current_mode

    # --- UTILS ---
    if command in ("/clear", "/cls"):
        os.system("cls" if os.name == "nt" else "clear")
        return "continue", current_mode

    if command in ("/exit", "/quit", "/q"):
        print("  Sampai jumpa!")
        sys.exit(0)

    if command in ("/opencode",):
        print("  Membuka OpenCode...")
        run_opencode()
        return "continue", current_mode

    # Unknown
    print(f"  Command tidak dikenal: {command}")
    print("  Ketik / untuk melihat command yang tersedia.")
    return "continue", current_mode


# ═══════════════════════════════════════════════════════════════
# INTERACTIVE MODE
# ═══════════════════════════════════════════════════════════════
def show_slash_menu():
    """Tampilkan slash menu (seperti OpenCode)."""
    print()
    print("  ==================================================")
    print("  COMMAND MENU")
    print("  ==================================================")
    print()
    print("  --- MODE ---")
    print("  /chat             Masuk mode Rapat Dewan Komisaris")
    print("                   (Owner + CEO + 62+ AI)")
    print("  /terminal         Masuk mode Ruang Operasional")
    print("                   (Owner + CEO + 35+ AI Teknis)")
    print()
    print("  --- MODEL ---")
    print("  /model            Lihat semua model AI (via 9Router)")
    print("  /switch-model     Ganti model AI")
    print(f"                    Current: {CURRENT_MODEL}")
    print()
    print("  --- INFO ---")
    print("  /ai-list          Lihat daftar AI specialists")
    print("  /status           Status sistem & koneksi")
    print("  /sop              SOP Shadow Advisor")
    print()
    print("  --- UTILS ---")
    print("  /opencode         Buka OpenCode langsung")
    print("  /clear            Clear layar")
    print("  /exit             Keluar dari Jagratam-CLI")
    print()
    print("  ==================================================")
    print("  Shadow Advisor berjalan di background (SOP MAS)")
    print("  PRD aktif sebagai kerangka kerja")
    print("  ==================================================")
    print()


def interactive_mode():
    """Mode interaktif utama."""
    global CURRENT_MODEL

    # Load models saat startup
    load_models()

    print()
    print("  ==================================================")
    print("       JAGRATAM-CLI -- CEO Command Interface")
    print("       SOP MAS: Shadow Advisor + PRD Active")
    print("       Powered by OpenCode + 9Router")
    print("  ==================================================")
    print()
    print("  Ketik / untuk command menu | Ketik pesan langsung untuk chat")
    print()

    current_mode = None  # None = main menu, "chat" atau "terminal"

    while True:
        # Prompt berdasarkan mode
        if current_mode == "chat":
            prompt_str = "  [Dewan] > "
        elif current_mode == "terminal":
            prompt_str = "  [Operasional] > "
        else:
            prompt_str = "jagratam> "

        try:
            user_input = input(prompt_str).strip()
        except (EOFError, KeyboardInterrupt):
            print("\nSampai jumpa!")
            break

        if not user_input:
            continue

        # Slash command
        if user_input.startswith("/"):
            if user_input == "/":
                show_slash_menu()
                # Tunggu input dari menu
                try:
                    choice = input("  Pilih command: ").strip()
                except (EOFError, KeyboardInterrupt):
                    print("\nSampai jumpa!")
                    break

                if choice:
                    action, current_mode = handle_slash_command(
                        choice if choice.startswith("/") else f"/{choice}",
                        current_mode
                    )
                    if action == "help":
                        show_slash_menu()
                continue

            action, current_mode = handle_slash_command(user_input, current_mode)
            if action == "help":
                show_slash_menu()
            continue

        # Default: kirim ke AI
        if current_mode is None:
            # Belum pilih mode, default ke chat
            current_mode = "chat"
            print()
            print("  [Auto] Masuk mode /chat (Rapat Dewan Komisaris)")
            print()

        print()
        print(f"  [Shadow Advisor] Memproses...")
        print()
        prompt = build_prompt(user_input, current_mode)
        send_to_ai(prompt)
        print()


# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════
def main():
    args = sys.argv[1:]

    # Tanpa args -> interactive mode
    if not args:
        interactive_mode()
        return

    # Dengan args
    cmd = args[0]
    if cmd in ("/help", "--help", "-h"):
        print(__doc__)
        return
    if cmd in ("/chat",):
        load_models()
        interactive_mode()
        return
    if cmd in ("/terminal",):
        load_models()
        interactive_mode()
        return

    # Lainnya -> pass ke OpenCode
    run_opencode(args)


if __name__ == "__main__":
    main()
