#!/usr/bin/env python3
"""
JAGRATAM-CLI — CEO Command Interface (Jagratam-Empire)
======================================================
SOP MAS: Shadow Advisor + PRD sebagai kerangka kerja permanen.
Backend: OpenRouter (free tier) — 55+ AI Executors

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
import time
from datetime import datetime

# Fix Windows encoding for Unicode output
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from ai_agents import (
    OPENROUTER_BASE, OPENROUTER_KEY, FREE_MODELS,
    AI_EXECUTORS, COLLABORATION_ROLES, TOPIC_ROLE_MAP,
    get_best_model, list_all_agents,
)

# ═══════════════════════════════════════════════════════════════
# API CALL — Panggil model via OpenRouter
# ═══════════════════════════════════════════════════════════════
def call_ai_model(executor_id, user_prompt, context=""):
    """Panggil AI executor via OpenRouter. Return response text."""
    executor = AI_EXECUTORS.get(executor_id)
    if not executor:
        return f"[ERROR: Unknown executor: {executor_id}]"

    if not OPENROUTER_KEY:
        return "[ERROR: OpenRouter API key tidak ditemukan. Set OPENROUTER_API_KEY di .env]"

    model = get_best_model(executor.get("model_preference", ["general"]))
    system_prompt = executor.get("system_prompt", f"Kamu adalah {executor['name']}. Bahasa Indonesia.")

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    if context:
        messages.append({"role": "system", "content": f"Konteks: {context}"})
    messages.append({"role": "user", "content": user_prompt})

    headers = {
        "Authorization": f"Bearer {OPENROUTER_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": model,
        "messages": messages,
        "max_tokens": 1000,
        "temperature": 0.7,
    }

    try:
        req = urllib.request.Request(
            f"{OPENROUTER_BASE}/chat/completions",
            data=json.dumps(data).encode("utf-8"),
            headers=headers,
            method="POST",
        )
        resp = urllib.request.urlopen(req, timeout=120)
        result = json.loads(resp.read())
        content = result["choices"][0]["message"]["content"]
        return content if content else "[Tidak ada respon]"
    except Exception as e:
        return f"[ERROR: {str(e)}]"


def call_model_direct(model_id=None, user_prompt="", system_prompt=""):
    """Panggil model langsung via OpenRouter. Default: openrouter/free."""
    if not OPENROUTER_KEY:
        return "[ERROR: OpenRouter API key tidak ditemukan]"

    if not model_id:
        model_id = "openrouter/free"

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": user_prompt})

    headers = {
        "Authorization": f"Bearer {OPENROUTER_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": model_id,
        "messages": messages,
        "max_tokens": 1500,
        "temperature": 0.7,
    }

    try:
        req = urllib.request.Request(
            f"{OPENROUTER_BASE}/chat/completions",
            data=json.dumps(data).encode("utf-8"),
            headers=headers,
            method="POST",
        )
        resp = urllib.request.urlopen(req, timeout=120)
        result = json.loads(resp.read())
        content = result["choices"][0]["message"]["content"]
        return content if content else "[Tidak ada respon]"
    except Exception as e:
        return f"[ERROR: {str(e)}]"


# ═══════════════════════════════════════════════════════════════
# /CHAT — RUANG RAPAT DEWAN KOMISARIS (Drama Style)
# ═══════════════════════════════════════════════════════════════
def chat_mode():
    """Mode /chat — Semua AI berbicara dalam format drama."""
    # Pilih AI yang akan berdiskusi (subset untuk speed)
    discussion_agents = [
        "kimi-k2.5", "claude-opus", "deepseek-chat", "qwen-3.5",
        "glm-5.2", "gemini-flash", "groq-llama", "mistral-large",
        "codex", "perplexity", "hermes", "mirofish", "deepseek-r1",
        "freebuff", "opencode", "nemotron-super", "llama-4",
    ]

    print()
    print("  ==================================================")
    print("  RUANG RAPAT DEWAN KOMISARIS")
    print(f"  {len(discussion_agents)} AI Berdiskusi | CEO sebagai Moderator")
    print("  ==================================================")
    print("  Ketik topik untuk memulai rapat.")
    print("  Ketik / untuk kembali ke command menu.")
    print()

    while True:
        try:
            topic = input("  [Owner] > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n  Kembali ke command menu.")
            break

        if not topic:
            continue
        if topic == "/":
            break
        if topic == "/exit":
            print("  Sampai jumpa!")
            sys.exit(0)
        if topic == "/ai-list":
            list_all_agents()
            continue

        # CEO buka rapat
        print()
        print("  ==================================================")
        print("  RAPAT DIMULAI")
        print(f"  Topik: {topic}")
        print("  ==================================================")
        print()
        print("  CEO: Selamat datang di Rapat Dewan Komisaris.")
        print(f"       Topik hari ini: \"{topic}\"")
        print("       Silakan berdiskusi sesuai keahlian masing-masing.")
        print()

        # FASE 1: Setiap AI berbicara
        all_responses = []
        for agent_id in discussion_agents:
            agent = AI_EXECUTORS.get(agent_id)
            if not agent:
                continue

            # Bangun konteks dari respon sebelumnya
            context = f"Topik rapat: {topic}"
            if all_responses:
                context += "\n\nRespon AI sebelumnya:\n"
                for prev_name, prev_resp in all_responses[-3:]:
                    prev_resp = prev_resp or "[Tidak ada respon]"
                    context += f"- {prev_name}: {prev_resp[:200]}...\n"

            prompt = f"Topik: {topic}\n\nBerikan pendapatmu sesuai keahlianmu. Bahasa Indonesia. 2-4 kalimat."

            print(f"  [{agent['name']}] sedang berpikir...")
            response = call_ai_model(agent_id, prompt, context)
            if not response:
                response = "[Tidak ada respon]"
            all_responses.append((agent["name"], response))

            # Tampilkan respons
            print()
            print(f"  {agent['name']}: {response}")
            print()

        # FASE 2: CEO rangkum
        print("  ==================================================")
        print("  CEO: Terima kasih semua AI. Saya rangkum diskusi:")
        print()

        summary_context = f"Topik: {topic}\n\n"
        for name, resp in all_responses:
            resp = resp or "[Tidak ada respon]"
            summary_context += f"{name}: {resp[:300]}\n\n"

        summary = call_model_direct(
            None,
            f"Rangkum diskusi ini dalam 3-5 poin utama. Bahasa Indonesia.",
            f"Kamu adalah CEO yang merangkum rapat. Singkat dan jelas.\n\n{summary_context}"
        )
        print(f"  CEO: {summary}")
        print()

        # FASE 3: Shadow Advisor — Kesimpulan
        print("  ==================================================")
        print("  SHADOW ADVISOR — LAPORAN KESIMPULAN")
        print("  ==================================================")
        print()

        conclusion_context = f"Topik: {topic}\n\nSemua respon:\n"
        for name, resp in all_responses:
            resp = resp or "[Tidak ada respon]"
            conclusion_context += f"{name}: {resp[:400]}\n\n"
        conclusion_context += f"\nRangkuman CEO: {summary}"

        conclusion = call_model_direct(
            None,
            f"Buat laporan lengkap:\n1. Situasi Sebenarnya\n2. Faktor Tersembunyi\n3. Risiko Utama\n4. Peluang Strategis\n5. Rencana Aksi\n6. Prediksi\n7. Kesimpulan CEO",
            f"Kamu adalah Shadow Advisor. Aktif saat kesimpulan rapat. Prinsip: berpikir sebagai operator, fokus kenyataan, cari akar masalah.\n\n{conclusion_context}"
        )
        print(f"  {conclusion}")
        print()
        print("  ==================================================")
        print("  RAPAT SELESAI")
        print("  Ketik topik baru untuk rapat berikutnya.")
        print("  ==================================================")
        print()


# ═══════════════════════════════════════════════════════════════
# /TERMINAL — RUANG OPERASIONAL (Task Assignment)
# ═══════════════════════════════════════════════════════════════
def terminal_mode():
    """Mode /terminal — CEO distribusi tugas ke CTO/CISO/Agent."""
    # CTO agents untuk eksekusi
    cto_agents = {
        "architect": "claude-opus",
        "frontend": "qwen-3.5",
        "backend": "deepseek-chat",
        "devops": "mistral-large",
        "security": "nemotron-super",
        "data": "glm-5.2",
        "mobile": "kimi-k2.5",
        "ai-ml": "deepseek-r1",
        "qa": "codex",
        "selfheal": "groq-llama",
    }

    print()
    print("  ==================================================")
    print("  RUANG OPERASIONAL")
    print(f"  CEO Orchestrate | {len(cto_agents)} CTO Specialists")
    print("  ==================================================")
    print("  Ketik tugas untuk dieksekusi.")
    print("  Ketik / untuk kembali ke command menu.")
    print()

    while True:
        try:
            task_input = input("  [Operasional] > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n  Kembali ke command menu.")
            break

        if not task_input:
            continue
        if task_input == "/":
            break
        if task_input == "/exit":
            print("  Sampai jumpa!")
            sys.exit(0)
        if task_input == "/ai-list":
            list_all_agents()
            continue

        # CEO analisis dan distribusi tugas
        print()
        print("  CEO: Menganalisis tugas dan mendistribusikan...")
        print()

        cto_list = "\n".join([f"  - {role}: {agent_id}" for role, agent_id in cto_agents.items()])
        ceo_prompt = f"""Tugas dari Owner: {task_input}

Daftar CTO yang tersedia:
{cto_list}

Analisis tugas ini dan distribusi ke CTO yang tepat.
Format:
→ CTO [Role]: [Task spesifik]

Jangan coding sendiri. CEO adalah ORCHESTRATOR."""

        ceo_assignment = call_model_direct(
            None,
            ceo_prompt,
            "Kamu adalah CEO JAGRATAM di Ruang Operasional. Orkestrasi, bukan coding sendiri. Bahasa Indonesia."
        )
        print(f"  CEO: {ceo_assignment}")
        print()

        # Setiap CTO eksekusi task mereka
        print("  ==================================================")
        print("  EKSEKUSI DIMULAI")
        print("  ==================================================")
        print()

        for role, agent_id in cto_agents.items():
            # Cek apakah CEO menugaskan role ini
            if role.lower() not in ceo_assignment.lower():
                continue

            agent = AI_EXECUTORS.get(agent_id, {})
            agent_name = agent.get("name", agent_id)

            prompt = f"Tugas dari CEO: {task_input}\n\nKerjakan sesuai keahlianmu sebagai {role}. Bahasa Indonesia. Berikan output konkret."

            print(f"  [{agent_name}] mengerjakan tugas...")
            result = call_ai_model(agent_id, prompt)

            print()
            print(f"  {agent_name}: {result}")
            print()

        # CEO review
        print("  ==================================================")
        print("  CEO: Review hasil eksekusi...")
        print()

        review = call_model_direct(
            None,
            "Berikan ringkasan hasil eksekusi. Singkat. Bahasa Indonesia.",
            f"Kamu adalah CEO review hasil kerja CTO. Tugas: {task_input}"
        )
        print(f"  CEO: {review}")
        print()
        print("  ==================================================")
        print("  EKSEKUSI SELESAI")
        print("  ==================================================")
        print()


# ═══════════════════════════════════════════════════════════════
# COMMAND MENU
# ═══════════════════════════════════════════════════════════════
def show_slash_menu():
    print()
    print("  ==================================================")
    print("  COMMAND MENU")
    print("  ==================================================")
    print()
    print("  --- MODE ---")
    print("  /chat             Rapat Dewan Komisaris (semua AI berbicara)")
    print("  /terminal         Ruang Operasional (CEO distribusi tugas)")
    print()
    print("  --- INFO ---")
    print("  /ai-list          Lihat semua AI agents")
    print("  /status           Status sistem")
    print("  /sop              SOP Shadow Advisor")
    print()
    print("  --- UTILS ---")
    print("  /opencode         Buka OpenCode langsung")
    print("  /clear            Clear layar")
    print("  /exit             Keluar")
    print()
    print("  ==================================================")
    print()


# ═══════════════════════════════════════════════════════════════
# MAIN INTERACTIVE MODE
# ═══════════════════════════════════════════════════════════════
def interactive_mode():
    print()
    print("  ==================================================")
    print("       JAGRATAM-CLI -- CEO Command Interface")
    print("       SOP MAS: Shadow Advisor + PRD Active")
    print("       Backend: OpenRouter (55+ AI Free)")
    print("  ==================================================")
    print()
    print("  Ketik / untuk command menu | Ketik pesan langsung untuk chat CEO")
    print()

    while True:
        try:
            user_input = input("jagratam> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nSampai jumpa!")
            break

        if not user_input:
            continue

        if user_input.startswith("/"):
            if user_input == "/":
                show_slash_menu()
                try:
                    choice = input("  Pilih command: ").strip()
                except (EOFError, KeyboardInterrupt):
                    print("\nSampai jumpa!")
                    break

                if choice:
                    choice = choice.lower()
                    if choice in ("chat", "1", "/chat"):
                        chat_mode()
                    elif choice in ("terminal", "2", "/terminal"):
                        terminal_mode()
                    elif choice in ("ai-list", "3", "/ai-list", "ailist"):
                        list_all_agents()
                    elif choice in ("status", "4", "/status"):
                        show_status()
                    elif choice in ("sop", "5", "/sop"):
                        show_sop()
                    elif choice in ("help", "6", "/help"):
                        show_slash_menu()
                    elif choice in ("clear", "7", "/clear"):
                        os.system("cls" if os.name == "nt" else "clear")
                    elif choice in ("exit", "8", "/exit"):
                        print("Sampai jumpa!")
                        break
                continue

            cmd = user_input.lower().split()[0]
            if cmd == "/chat":
                chat_mode()
            elif cmd == "/terminal":
                terminal_mode()
            elif cmd == "/ai-list":
                list_all_agents()
            elif cmd == "/status":
                show_status()
            elif cmd == "/sop":
                show_sop()
            elif cmd == "/opencode":
                run_opencode()
            elif cmd == "/clear":
                os.system("cls" if os.name == "nt" else "clear")
            elif cmd == "/exit":
                print("Sampai jumpa!")
                break
            elif cmd == "/help":
                show_slash_menu()
            continue

        # Default: chat dengan CEO + Shadow Advisor
        print()
        print("  [Shadow Advisor] Memproses...")
        print()

        response = call_model_direct(
            None,
            user_prompt=f"Pesan dari Owner: {user_input}\n\nJawab dengan format Shadow Advisor:\n1. Situasi Sebenarnya\n2. Faktor Tersembunyi\n3. Risiko Utama\n4. Peluang Strategis\n5. Rencana Aksi\n6. Prediksi\n7. Kesimpulan CEO",
            system_prompt="Kamu adalah Shadow Advisor, sistem intelijen strategis. Berpikir sebagai operator, fokus kenyataan, cari akar masalah. Bahasa Indonesia."
        )
        print(f"  CEO: {response}")
        print()


def show_status():
    print()
    print("  ==================================================")
    print("  STATUS SISTEM")
    print("  ==================================================")
    print(f"  OpenCode    : {'[OK]' if shutil.which('opencode') else '[!!] Tidak ditemukan'}")
    print(f"  OpenRouter  : {'[OK] Key ada' if OPENROUTER_KEY else '[!!] Key tidak ditemukan'}")
    print(f"  AI Agents   : {len(AI_EXECUTORS)} total")
    print(f"  Free Models : {len(FREE_MODELS)} tersedia")
    print(f"  Shadow Adv. : [OK] SOP MAS Active")
    print(f"  PRD         : [OK] Active")
    print(f"  /chat       : Semua AI berbicara (drama style)")
    print(f"  /terminal   : CEO distribusi tugas ke CTO")
    print(f"  ==================================================")
    print()


def show_sop():
    print()
    print("  SHADOW ADVISOR — SOP MAS")
    print("  Aktif hanya saat kesimpulan rapat.")
    print()
    print("  Format Laporan:")
    print("  1. Situasi Sebenarnya")
    print("  2. Faktor Tersembunyi")
    print("  3. Risiko Utama")
    print("  4. Peluang Strategis")
    print("  5. Rencana Aksi")
    print("  6. Prediksi")
    print("  7. Kesimpulan CEO")
    print()
    print("  Prinsip:")
    print("  - Berpikir sebagai operator, bukan penonton")
    print("  - Fokus pada kenyataan, bukan asumsi")
    print("  - Cari akar masalah, bukan gejalanya")
    print("  - Utamakan efektivitas, bukan popularitas")
    print()


def find_opencode():
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
    oc = find_opencode()
    if not oc:
        print("  ERROR: OpenCode tidak ditemukan.")
        return 1
    cmd = [oc] + (args or [])
    if oc.endswith(".ps1"):
        cmd = ["powershell", "-ExecutionPolicy", "Bypass", "-File", oc] + (args or [])
    return subprocess.call(cmd)


# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════
def main():
    args = sys.argv[1:]
    if not args:
        interactive_mode()
        return
    cmd = args[0]
    if cmd in ("/help", "--help", "-h"):
        print(__doc__)
        return
    if cmd == "/chat":
        chat_mode()
        return
    if cmd == "/terminal":
        terminal_mode()
        return
    if cmd == "/ai-list":
        list_all_agents()
        return
    if cmd == "/status":
        show_status()
        return
    run_opencode(args)


if __name__ == "__main__":
    main()
