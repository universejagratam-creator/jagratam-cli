#!/usr/bin/env python3
"""
JAGRATAM-CLI — CEO Command Interface (Jagratam-Empire)
======================================================
SOP MAS: Shadow Advisor + PRD sebagai kerangka kerja permanen.
Backend: OpenRouter free tier — Pipeline EXACT dari LinkDiskusi

Cara pakai:
  jagratam                # Buka langsung
  jagratam /help          # Bantuan
"""

import sys
import os
import subprocess
import json
import shutil
import urllib.request
import time

# Fix Windows encoding
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from ai_agents import (
    OPENROUTER_BASE, OPENROUTER_KEY, FREE_MODELS,
    AI_EXECUTORS, COLLABORATION_ROLES, TOPIC_ROLE_MAP, ROLE_MODEL_PREF,
    get_best_model, assign_executors_to_roles, analyze_topic,
    call_openrouter, get_ai_response, list_all_agents,
)

# ═══════════════════════════════════════════════════════════════
# /CHAT — COLLABORATIVE PIPELINE (EXACT dari LinkDiskusi)
# ═══════════════════════════════════════════════════════════════
def chat_mode():
    """Mode /chat — Pipeline kolaboratif: analyst -> architect -> coder+reviewer+strategist -> summarizer"""
    print()
    print("  ==================================================")
    print("  RUANG RAPAT — COLLABORATIVE PIPELINE")
    print("  analyst -> architect -> coder+reviewer+strategist -> summarizer")
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

        # 1. Analisis topik
        analysis = analyze_topic(topic)
        category = analysis["category"]

        # 2. Assign executors ke roles
        role_assignments = assign_executors_to_roles(category)

        print()
        print("  ==================================================")
        print("  RAPAT DIMULAI")
        print(f"  Topik: {topic}")
        print(f"  Kategori: {category}")
        print(f"  Roles: {list(role_assignments.keys())}")
        for role, executor in role_assignments.items():
            ex = AI_EXECUTORS.get(executor, {})
            print(f"    {role:<12s} -> {ex.get('name', executor)}")
        print("  ==================================================")
        print()

        # 3. Jalankan pipeline
        accumulated_context = f"Owner's request: {topic}\n\nTopic category: {category}\nKeywords: {', '.join(analysis.get('keywords', []))}\n"
        pipeline_results = {}

        # PHASE 1: Sequential — Analyst & Architect
        print("  --- PHASE 1: ANALYST & ARCHITECT (Sequential) ---")
        print()
        for role in ["analyst", "architect"]:
            if role not in role_assignments:
                continue

            executor_name = role_assignments[role]
            role_config = COLLABORATION_ROLES[role]
            executor_config = AI_EXECUTORS.get(executor_name, {})

            print(f"  [{role.upper()}] {executor_config.get('name', executor_name)} sedang berpikir...")

            result = get_ai_response(executor_name, topic, accumulated_context)
            if result:
                content = result["content"]
                pipeline_results[role] = {"executor": executor_name, "executor_name": executor_config.get("name", executor_name), "content": content, "model": result.get("model", "")}
                accumulated_context += f"\n\n--- {role_config['name']} ({executor_config.get('name', executor_name)}) ---\n{content}"
                print()
                print(f"  {role_config['name']} ({executor_config.get('name', executor_name)}):")
                print(f"  {content}")
                print()
            else:
                print(f"  [ERROR] {executor_config.get('name', executor_name)} tidak merespon")

        # PHASE 2: Parallel — Coder, Reviewer, Strategist
        print("  --- PHASE 2: CODER + REVIEWER + STRATEGIST (Parallel) ---")
        print()
        parallel_results = {}
        for role in ["coder", "reviewer", "strategist"]:
            if role not in role_assignments:
                continue

            executor_name = role_assignments[role]
            role_config = COLLABORATION_ROLES[role]
            executor_config = AI_EXECUTORS.get(executor_name, {})

            print(f"  [{role.upper()}] {executor_config.get('name', executor_name)} sedang berpikir...")

            result = get_ai_response(executor_name, topic, accumulated_context)
            if result:
                content = result["content"]
                parallel_results[role] = {"executor": executor_name, "executor_name": executor_config.get("name", executor_name), "content": content, "model": result.get("model", "")}
                print()
                print(f"  {role_config['name']} ({executor_config.get('name', executor_name)}):")
                print(f"  {content}")
                print()
            else:
                print(f"  [ERROR] {executor_config.get('name', executor_name)} tidak merespon")

        # Merge parallel ke pipeline
        pipeline_results.update(parallel_results)
        for role, res in parallel_results.items():
            role_config = COLLABORATION_ROLES[role]
            accumulated_context += f"\n\n--- {role_config['name']} ({res['executor_name']}) ---\n{res['content']}"

        # PHASE 3: Sequential — Summarizer
        print("  --- PHASE 3: SUMMARIZER (Consolidation) ---")
        print()
        if "summarizer" in role_assignments:
            executor_name = role_assignments["summarizer"]
            role_config = COLLABORATION_ROLES["summarizer"]
            executor_config = AI_EXECUTORS.get(executor_name, {})

            print(f"  [SUMMARIZER] {executor_config.get('name', executor_name)} sedang merangkum...")

            result = get_ai_response(executor_name, topic, accumulated_context)
            if result:
                content = result["content"]
                pipeline_results["summarizer"] = {"executor": executor_name, "executor_name": executor_config.get("name", executor_name), "content": content, "model": result.get("model", "")}
                print()
                print(f"  {role_config['name']} ({executor_config.get('name', executor_name)}):")
                print(f"  {content}")
                print()
            else:
                print(f"  [ERROR] Summarizer tidak merespon")

        # HASIL AKHIR
        print("  ==================================================")
        print("  RAPAT SELESAI")
        print(f"  {len(pipeline_results)}/{len(role_assignments)} roles terisi")
        print("  ==================================================")
        print()


# ═══════════════════════════════════════════════════════════════
# /TERMINAL — CEO ORCHESTRATE
# ═══════════════════════════════════════════════════════════════
def terminal_mode():
    """Mode /terminal — CEO distribusi tugas ke CTO/CISO/Agent."""
    print()
    print("  ==================================================")
    print("  RUANG OPERASIONAL")
    print("  CEO Orchestrate | Task Assignment")
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

        # Analisis dan eksekusi
        analysis = analyze_topic(task_input)
        category = analysis["category"]
        role_assignments = assign_executors_to_roles(category)

        print()
        print(f"  CEO: Menganalisis tugas (kategori: {category})...")
        print()

        # Jalankan pipeline
        accumulated_context = f"Task: {task_input}\nCategory: {category}\n"
        pipeline_results = {}

        for role in ["analyst", "architect", "coder", "reviewer", "strategist", "summarizer"]:
            if role not in role_assignments:
                continue

            executor_name = role_assignments[role]
            role_config = COLLABORATION_ROLES[role]
            executor_config = AI_EXECUTORS.get(executor_name, {})

            print(f"  [{role.upper()}] {executor_config.get('name', executor_name)}...")

            result = get_ai_response(executor_name, task_input, accumulated_context)
            if result:
                content = result["content"]
                pipeline_results[role] = {"executor_name": executor_config.get("name", executor_name), "content": content}
                accumulated_context += f"\n\n--- {role_config['name']} ---\n{content}"
                print(f"  {content[:200]}...")
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
    print("  /chat             Collaborative Pipeline (analyst->architect->coder->reviewer->strategist->summarizer)")
    print("  /terminal         CEO Orchestrate (Task Assignment)")
    print()
    print("  --- INFO ---")
    print("  /ai-list          Lihat semua 62 AI agents + 13 models")
    print("  /status           Status sistem")
    print("  /sop              SOP Shadow Advisor")
    print()
    print("  --- UTILS ---")
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
    print("       Backend: OpenRouter (13 Free Models)")
    print("       Pipeline: EXACT dari LinkDiskusi")
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
            elif cmd == "/clear":
                os.system("cls" if os.name == "nt" else "clear")
            elif cmd == "/exit":
                print("Sampai jumpa!")
                break
            elif cmd == "/help":
                show_slash_menu()
            continue

        # Default: chat dengan Shadow Advisor
        print()
        print("  [Shadow Advisor] Memproses...")
        print()

        messages = [
            {"role": "system", "content": "Kamu adalah Shadow Advisor, sistem intelijen strategis. Berpikir sebagai operator, fokus kenyataan, cari akar masalah. Bahasa Indonesia."},
            {"role": "user", "content": f"Pesan dari Owner: {user_input}\n\nJawab dengan format Shadow Advisor:\n1. Situasi Sebenarnya\n2. Faktor Tersembunyi\n3. Risiko Utama\n4. Peluang Strategis\n5. Rencana Aksi\n6. Prediksi\n7. Kesimpulan CEO"},
        ]
        model = get_best_model(["reasoning", "general"])
        response = call_openrouter(model, messages)
        if not response:
            for m in FREE_MODELS:
                response = call_openrouter(m["id"], messages)
                if response:
                    break
        print(f"  CEO: {response if response else '[Tidak ada respon]'}")
        print()


def show_status():
    print()
    print("  ==================================================")
    print("  STATUS SISTEM")
    print("  ==================================================")
    print(f"  OpenCode    : {'[OK]' if shutil.which('opencode') else '[!!] Tidak ditemukan'}")
    print(f"  OpenRouter  : {'[OK] Key ada' if OPENROUTER_KEY else '[!!] Key tidak ditemukan'}")
    print(f"  Executors   : {len(AI_EXECUTORS)} persona")
    print(f"  Models      : {len(FREE_MODELS)} free models (API)")
    print(f"  Pipeline    : analyst->architect->coder+reviewer+strategist->summarizer")
    print(f"  Shadow Adv. : [OK] SOP MAS Active")
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


if __name__ == "__main__":
    main()
