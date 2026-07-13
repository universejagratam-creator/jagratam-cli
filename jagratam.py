#!/usr/bin/env python3
"""
JAGRATAM-CLI — OpenCode Clone with Unlimited Free AI
=====================================================
Clone dari OpenCode dengan 62+ AI models gratis tanpa batas token.
Backend: OpenRouter free tier via OpenCode

Cara pakai:
  jagratam                # Buka OpenCode langsung
  jagratam /help          # Bantuan
  jagratam /chat          # Collaborative pipeline
  jagratam /terminal      # CEO orchestrate
  jagratam /models        # Lihat semua models
  jagratam /providers     # Lihat providers
"""

import sys
import os
import subprocess
import shutil

# Fix Windows encoding
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


def find_opencode():
    """Find OpenCode binary."""
    oc_path = shutil.which("opencode")
    if oc_path:
        return oc_path
    known_paths = [
        r"C:\nvm4w\nodejs\node_modules\opencode-ai\node_modules\opencode-windows-x64\bin\opencode.exe",
        r"C:\nvm4w\nodejs\opencode.exe",
    ]
    for p in known_paths:
        if os.path.exists(p):
            return p
    return None


def run_opencode(args=None):
    """Run OpenCode with arguments."""
    oc = find_opencode()
    if not oc:
        print("  ERROR: OpenCode tidak ditemukan.")
        print("  Install: npm install -g opencode-ai")
        return 1
    cmd = [oc] + (args or [])
    return subprocess.call(cmd)


def show_help():
    print()
    print("  ==================================================")
    print("  JAGRATAM-CLI — OpenCode Clone (Unlimited Free AI)")
    print("  ==================================================")
    print()
    print("  --- OPENCODE COMMANDS (same as original) ---")
    print("  jagratam                  Buka OpenCode TUI langsung")
    print("  jagratam run [message]    Non-interactive execution")
    print("  jagratam serve            Headless server mode")
    print("  jagratam web              Server + web interface")
    print("  jagratam providers        Manage AI providers")
    print("  jagratam models           List all available models")
    print("  jagratam session          Manage sessions")
    print("  jagratam agent            Manage agents")
    print("  jagratam mcp              Manage MCP servers")
    print("  jagratam stats            Token usage statistics")
    print("  jagratam upgrade          Self-update")
    print()
    print("  --- JAGRATAM EXTENSIONS ---")
    print("  jagratam /chat            Collaborative pipeline (6 roles)")
    print("  jagratam /terminal        CEO orchestrate (task assignment)")
    print("  jagratam /ai-list         Lihat 62 AI executors")
    print("  jagratam /status          Status sistem")
    print()
    print("  --- MODELS (FREE via OpenRouter) ---")
    print("  openrouter/nvidia/nemotron-3-super-120b-a12b:free     Nemotron Super")
    print("  openrouter/nvidia/nemotron-3-ultra-550b-a55b:free     Nemotron Ultra")
    print("  openrouter/google/gemma-4-31b-it:free                 Gemma 4")
    print("  openrouter/meta-llama/llama-4-maverick:free           Llama 4")
    print("  openrouter/deepseek/deepseek-r1:free                  DeepSeek R1")
    print("  openrouter/deepseek/deepseek-chat:free                DeepSeek Chat")
    print("  openrouter/openrouter/free                            Auto (random free)")
    print("  ... dan 300+ models lainnya via OpenRouter")
    print()
    print("  --- CONFIG ---")
    print("  Config: ~/.config/opencode/opencode.json")
    print("  Provider: OpenRouter (300+ models, 27+ free)")
    print("  Key: OPENROUTER_API_KEY env var")
    print()
    print("  ==================================================")
    print()


def show_status():
    oc = find_opencode()
    key = os.environ.get("OPENROUTER_API_KEY", "")
    if not key:
        env_paths = [
            os.path.expanduser("~/PROJECT/multi-agent-system/.env"),
            os.path.expanduser("~/PROJECT/multi-agent-system/config/.env.bak"),
        ]
        for p in env_paths:
            if os.path.exists(p):
                try:
                    with open(p) as f:
                        for line in f:
                            if line.startswith("OPENROUTER_API_KEY="):
                                _, _, val = line.partition("=")
                                val = val.strip().strip('"').strip("'")
                                if val.startswith("sk-or-"):
                                    key = val
                                    break
                except:
                    pass
            if key:
                break

    print()
    print("  ==================================================")
    print("  JAGRATAM-CLI STATUS")
    print("  ==================================================")
    print(f"  OpenCode    : {'[OK] ' + oc if oc else '[!!] Tidak ditemukan'}")
    print(f"  OpenRouter  : {'[OK] Key ada' if key else '[!!] Key tidak ditemukan'}")
    print(f"  Models      : 300+ via OpenRouter (27+ free)")
    print(f"  Providers   : OpenRouter, 9Router, Google")
    print(f"  Config      : ~/.config/opencode/opencode.json")
    print(f"  ==================================================")
    print()


def show_ai_list():
    print()
    print("  ==================================================")
    print("  62 AI EXECUTORS (dari LinkDiskusi)")
    print("  ==================================================")
    print()
    executors = {
        "freebuff": "Freebuff (Buffy) — Strategic AI",
        "opencode": "OpenCode — Code AI",
        "cursor": "Cursor — Code Editor AI",
        "claude-opus": "Nemotron Ultra 550B — Premium Reasoning",
        "claude-sonnet": "Gemma 4 31B — Balanced AI",
        "claude-haiku": "Nemotron Nano 30B — Fast AI",
        "gpt-4o": "Qwen3 Next 80B — General AI",
        "gpt-4o-mini": "Groq Llama Ultra — Fast AI",
        "gemini-pro": "Gemma 4 31B — Google Open",
        "gemini-flash": "Gemini 2.0 Flash — Google Fast",
        "deepseek-r1": "DeepSeek R1 — Reasoning AI",
        "deepseek-chat": "DeepSeek Chat — Chat AI",
        "deepseek-coder": "DeepSeek Coder — Code AI",
        "glm-5.2": "GLM-5.2 — Zhipu Premium",
        "kimi-k2.5": "Kimi K2.5 — Moonshot Premium",
        "qwen-3.5": "Qwen 3.5 — Alibaba Premium",
        "llama-4": "Llama 4 Maverick — Meta Latest",
        "mistral-large": "Mistral Large — Mistral Premium",
        "codestral": "Codestral — Mistral Code",
        "nemotron-super": "Nemotron Super 120B — NVIDIA Premium",
        "nemotron-ultra": "Nemotron Ultra 550B — NVIDIA Ultra",
        "groq-llama": "Groq Llama 3.3 — Ultra-Fast AI",
        "hermes": "Hermes — Nous Hermes",
        "mirofish": "MiroFish — Creative AI",
        "codex": "Codex — Code Generation",
        "perplexity": "Perplexity — Search AI",
    }
    for k, v in executors.items():
        print(f"    {k:<20s} {v}")
    print()
    print("  ... dan 36 lainnya (total 62)")
    print()


def main():
    args = sys.argv[1:]

    if not args:
        # Default: buka OpenCode TUI
        return run_opencode()

    cmd = args[0]

    # Jagratam-specific commands
    if cmd == "/help" or cmd == "--help" or cmd == "-h":
        show_help()
        return 0
    if cmd == "/status":
        show_status()
        return 0
    if cmd == "/ai-list":
        show_ai_list()
        return 0
    if cmd == "/chat":
        # Run OpenCode with collaborative prompt
        return run_opencode(["run", "--agent", "build",
            "Jalankan collaborative pipeline: analyst -> architect -> coder+reviewer+strategist -> summarizer. "
            "Topik: " + " ".join(args[1:]) if len(args) > 1 else "test"])
    if cmd == "/terminal":
        return run_opencode(["run", "--agent", "build",
            "CEO orchestrate: analisis tugas, distribusi ke specialist, eksekusi. "
            "Tugas: " + " ".join(args[1:]) if len(args) > 1 else "test"])
    if cmd == "/models":
        return run_opencode(["models"] + args[1:])
    if cmd == "/providers":
        return run_opencode(["providers"] + args[1:])

    # Pass-through to OpenCode
    return run_opencode(args)


if __name__ == "__main__":
    sys.exit(main() or 0)
