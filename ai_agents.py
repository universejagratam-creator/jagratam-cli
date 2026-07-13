#!/usr/bin/env python3
"""
AI AGENTS — Daftar Lengkap 55+ AI dari LinkDiskusi + MAS
========================================================
Backend: OpenRouter (free tier)
Model: nvidia, google, qwen, deepseek, meta, mistral, dll.
"""

import os
import json
import urllib.request

# ═══════════════════════════════════════════════════════════════
# OPENROUTER CONFIG
# ═══════════════════════════════════════════════════════════════
OPENROUTER_BASE = "https://openrouter.ai/api/v1"

def _load_openrouter_key():
    """Load OpenRouter API key dari .env"""
    key = os.environ.get("OPENROUTER_API_KEY", "")
    if key:
        return key
    env_paths = [
        os.path.expanduser("~/PROJECT/multi-agent-system/.env"),
        os.path.expanduser("~/.env"),
    ]
    for path in env_paths:
        if os.path.exists(path):
            with open(path) as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("OPENROUTER_API_KEY="):
                        _, _, val = line.partition("=")
                        return val.strip().strip('"').strip("'")
    return ""

OPENROUTER_KEY = _load_openrouter_key()

# ═══════════════════════════════════════════════════════════════
# FREE MODELS (OpenRouter free router + individual)
# ═══════════════════════════════════════════════════════════════
FREE_MODELS = [
    {"id": "openrouter/free", "name": "OpenRouter Free (Auto)", "strength": "general"},
    {"id": "nvidia/nemotron-3-super-120b-a12b:free", "name": "Nemotron Super 120B", "strength": "general"},
    {"id": "nvidia/nemotron-3-ultra-550b-a55b:free", "name": "Nemotron Ultra 550B", "strength": "reasoning"},
    {"id": "google/gemma-4-31b-it:free", "name": "Gemma 4 31B", "strength": "general"},
    {"id": "poolside/laguna-xs-2.1:free", "name": "Laguna XS.2", "strength": "code"},
]

# ═══════════════════════════════════════════════════════════════
# 55+ AI EXECUTORS (dari LinkDiskusi ai_executor.py)
# ═══════════════════════════════════════════════════════════════
AI_EXECUTORS = {
    # ── CORE ──
    "freebuff": {"name": "Freebuff (Buffy)", "role": "Strategic AI", "avatar": "🤖", "color": "#4f46e5", "system_prompt": "Kamu adalah Freebuff, analis strategis AI. Singkat, berbasis data. Bahasa Indonesia.", "model_preference": ["reasoning", "general"]},
    "opencode": {"name": "OpenCode", "role": "Code AI", "avatar": "💻", "color": "#06b6d4", "system_prompt": "Kamu adalah OpenCode, ahli coding AI. Kode bersih, efisien. Bahasa Indonesia.", "model_preference": ["code", "general"]},
    "cursor": {"name": "Cursor", "role": "Code Editor AI", "avatar": "✏️", "color": "#8b5cf6", "system_prompt": "Kamu adalah Cursor, ahli edit kode. Debug, refactor, review. Bahasa Indonesia.", "model_preference": ["code", "general"]},

    # ── ANTHROPIC REPLACEMENTS (FREE) ──
    "claude-opus": {"name": "Nemotron Ultra 550B", "role": "Premium Reasoning (Free)", "avatar": "⚡", "color": "#059669", "system_prompt": "Kamu adalah Nemotron Ultra, reasoning mendalam, analisis kompleks. Pengganti Claude Opus. Bahasa Indonesia.", "model_preference": ["reasoning", "general"]},
    "claude-sonnet": {"name": "Gemma 4 31B", "role": "Balanced AI (Free)", "avatar": "💎", "color": "#22c55e", "system_prompt": "Kamu adalah Gemma 4, seimbang antara speed dan capability. Pengganti Claude Sonnet. Bahasa Indonesia.", "model_preference": ["code", "reasoning"]},
    "claude-haiku": {"name": "Nemotron Nano 30B", "role": "Fast AI (Free)", "avatar": "🚀", "color": "#34d399", "system_prompt": "Kamu adalah Nemotron Nano, cepat dan efisien. Pengganti Claude Haiku. Bahasa Indonesia.", "model_preference": ["fast", "general"]},

    # ── OPENAI REPLACEMENTS (FREE) ──
    "gpt-4o": {"name": "Qwen3 Next 80B", "role": "General AI (Free)", "avatar": "☁️", "color": "#ef4444", "system_prompt": "Kamu adalah Qwen3 Next 80B, reasoning kuat. Pengganti GPT-4o. Bahasa Indonesia.", "model_preference": ["general", "reasoning"]},
    "gpt-4o-mini": {"name": "Groq Llama Ultra", "role": "Fast AI (Free)", "avatar": "🚀", "color": "#f97316", "system_prompt": "Kamu adalah Groq Llama, inference ultra-fast. Pengganti GPT-4o Mini. Bahasa Indonesia.", "model_preference": ["fast", "general"]},

    # ── GOOGLE REPLACEMENTS (FREE) ──
    "gemini-pro": {"name": "Gemma 4 31B", "role": "Google Open (Free)", "avatar": "💎", "color": "#22c55e", "system_prompt": "Kamu adalah Gemma 4, AI open-source Google. Pengganti Gemini Pro. Bahasa Indonesia.", "model_preference": ["reasoning", "general"]},
    "gemini-flash": {"name": "Gemini 2.0 Flash", "role": "Google Fast", "avatar": "⚡", "color": "#facc15", "system_prompt": "Kamu adalah Gemini Flash, AI cepat multimodal. Bahasa Indonesia.", "model_preference": ["fast", "general"]},

    # ── DEEPSEEK ──
    "deepseek-r1": {"name": "DeepSeek R1", "role": "Reasoning AI", "avatar": "🔍", "color": "#0ea5e9", "system_prompt": "Kamu adalah DeepSeek R1, reasoning, matematika, step-by-step. Bahasa Indonesia.", "model_preference": ["reasoning", "code"]},
    "deepseek-chat": {"name": "DeepSeek Chat", "role": "DeepSeek Chat", "avatar": "🔍", "color": "#38bdf8", "system_prompt": "Kamu adalah DeepSeek Chat, coding, analisis, percakapan. Bahasa Indonesia.", "model_preference": ["code", "general"]},
    "deepseek-coder": {"name": "DeepSeek Coder", "role": "DeepSeek Code", "avatar": "💻", "color": "#06b6d4", "system_prompt": "Kamu adalah DeepSeek Coder, expert code generation. Bahasa Indonesia.", "model_preference": ["code", "general"]},

    # ── ZHIPU AI ──
    "glm-5.2": {"name": "GLM-5.2", "role": "Zhipu Premium", "avatar": "🧠", "color": "#6366f1", "system_prompt": "Kamu adalah GLM-5.2, NLP China, security, code review. Bahasa Indonesia.", "model_preference": ["reasoning", "general"]},
    "glm-4-flash": {"name": "GLM-4 Flash", "role": "Zhipu Fast", "avatar": "🧠", "color": "#818cf8", "system_prompt": "Kamu adalah GLM-4 Flash, fast QA, translation, code. Bahasa Indonesia.", "model_preference": ["fast", "general"]},

    # ── MOONSHOT AI ──
    "kimi-k2.5": {"name": "Kimi K2.5", "role": "Moonshot Premium", "avatar": "🌙", "color": "#f59e0b", "system_prompt": "Kamu adalah Kimi K2.5, 256k context, vision, tools. Bahasa Indonesia.", "model_preference": ["reasoning", "general"]},
    "kimi-k2-lite": {"name": "Kimi K2.5 Lite", "role": "Moonshot Fast", "avatar": "🌙", "color": "#fbbf24", "system_prompt": "Kamu adalah Kimi Lite, fast lightweight AI. Bahasa Indonesia.", "model_preference": ["fast", "general"]},

    # ── ALIBABA ──
    "qwen-3.5": {"name": "Qwen 3.5", "role": "Alibaba Premium", "avatar": "☁️", "color": "#ef4444", "system_prompt": "Kamu adalah Qwen 3.5, multi-language, coding, reasoning. Bahasa Indonesia.", "model_preference": ["code", "reasoning"]},
    "qwen-turbo": {"name": "Qwen Turbo", "role": "Alibaba Fast", "avatar": "☁️", "color": "#f87171", "system_prompt": "Kamu adalah Qwen Turbo, fast QA, translation. Bahasa Indonesia.", "model_preference": ["fast", "general"]},

    # ── META ──
    "llama-4": {"name": "Llama 4 Maverick", "role": "Meta Latest", "avatar": "🦙", "color": "#0ea5e9", "system_prompt": "Kamu adalah Llama 4, model open-source terbaru Meta. Bahasa Indonesia.", "model_preference": ["general", "reasoning"]},
    "llama-3.3": {"name": "Llama 3.3 70B", "role": "Meta Stable", "avatar": "🦙", "color": "#38bdf8", "system_prompt": "Kamu adalah Llama 3.3, stabil 70B general-purpose. Bahasa Indonesia.", "model_preference": ["general", "reasoning"]},

    # ── MISTRAL ──
    "mistral-large": {"name": "Mistral Large", "role": "Mistral Premium", "avatar": "🌊", "color": "#3b82f6", "system_prompt": "Kamu adalah Mistral Large, coding, reasoning, multilingual. Bahasa Indonesia.", "model_preference": ["code", "reasoning"]},
    "codestral": {"name": "Codestral", "role": "Mistral Code", "avatar": "⚡", "color": "#60a5fa", "system_prompt": "Kamu adalah Codestral, expert code Mistral. Bahasa Indonesia.", "model_preference": ["code", "general"]},

    # ── NVIDIA ──
    "nemotron-super": {"name": "Nemotron Super 120B", "role": "NVIDIA Premium", "avatar": "🟢", "color": "#10b981", "system_prompt": "Kamu adalah Nemotron Super, model kuat NVIDIA. Bahasa Indonesia.", "model_preference": ["general", "reasoning"]},
    "nemotron-ultra": {"name": "Nemotron Ultra 550B", "role": "NVIDIA Ultra", "avatar": "⚡", "color": "#059669", "system_prompt": "Kamu adalah Nemotron Ultra, reasoning mendalam, tugas kompleks. Bahasa Indonesia.", "model_preference": ["reasoning", "general"]},

    # ── GROQ ──
    "groq-llama": {"name": "Groq Llama 3.3", "role": "Ultra-Fast AI", "avatar": "🚀", "color": "#f97316", "system_prompt": "Kamu adalah Groq Llama, inference ultra-fast. Bahasa Indonesia.", "model_preference": ["fast", "general"]},

    # ── COHERE ──
    "command-r-plus": {"name": "Command R+", "role": "Cohere Premium", "avatar": "🔷", "color": "#8b5cf6", "system_prompt": "Kamu adalah Command R+, RAG, search, generation. Bahasa Indonesia.", "model_preference": ["general", "reasoning"]},

    # ── SPECIALIZED ──
    "hermes": {"name": "Hermes", "role": "Nous Hermes", "avatar": "🏛️", "color": "#8b5cf6", "system_prompt": "Kamu adalah Hermes, AI Nous Research. Kreatif, insight. Bahasa Indonesia.", "model_preference": ["general", "reasoning"]},
    "mirofish": {"name": "MiroFish", "role": "Creative AI", "avatar": "🐟", "color": "#06b6d4", "system_prompt": "Kamu adalah MiroFish, solusi kreatif inovatif. Bahasa Indonesia.", "model_preference": ["general", "reasoning"]},
    "deepagents": {"name": "DeepAgents", "role": "Planning AI", "avatar": "🎯", "color": "#ef4444", "system_prompt": "Kamu adalah DeepAgents, planning dan orchestration. Bahasa Indonesia.", "model_preference": ["reasoning", "general"]},
    "perplexity": {"name": "Perplexity", "role": "Search AI", "avatar": "🔎", "color": "#0ea5e9", "system_prompt": "Kamu adalah Perplexity, search-augmented AI. Sertakan sumber. Bahasa Indonesia.", "model_preference": ["general", "reasoning"]},
    "codex": {"name": "Codex", "role": "Code Generation", "avatar": "💻", "color": "#10b981", "system_prompt": "Kamu adalah Codex, production-ready code generation. Bahasa Indonesia.", "model_preference": ["code", "general"]},

    # ── FREE TIERS ──
    "kimi-free": {"name": "Kimi Free", "role": "Moonshot Free", "avatar": "🌙", "color": "#fbbf24", "system_prompt": "Kamu adalah Kimi Free, long context, vision. Bahasa Indonesia.", "model_preference": ["general", "reasoning"]},
    "glm-free": {"name": "GLM Free", "role": "Zhipu Free", "avatar": "🧠", "color": "#818cf8", "system_prompt": "Kamu adalah GLM Free, NLP China, code. Bahasa Indonesia.", "model_preference": ["general", "fast"]},
    "deepseek-free": {"name": "DeepSeek Free", "role": "DeepSeek Free", "avatar": "🔍", "color": "#38bdf8", "system_prompt": "Kamu adalah DeepSeek Free, coding, reasoning. Bahasa Indonesia.", "model_preference": ["code", "general"]},
    "qwen-free": {"name": "Qwen Free", "role": "Alibaba Free", "avatar": "☁️", "color": "#f87171", "system_prompt": "Kamu adalah Qwen Free, multilingual, coding. Bahasa Indonesia.", "model_preference": ["general", "fast"]},
    "groq-free": {"name": "Groq Free", "role": "Groq Free", "avatar": "🚀", "color": "#f97316", "system_prompt": "Kamu adalah Groq Free, ultra-fast free inference. Bahasa Indonesia.", "model_preference": ["fast", "general"]},
    "mistral-free": {"name": "Mistral Free", "role": "Mistral Free", "avatar": "🌊", "color": "#93c5fd", "system_prompt": "Kamu adalah Mistral Free, European AI free tier. Bahasa Indonesia.", "model_preference": ["general", "fast"]},
    "nvidia-free": {"name": "NVIDIA Free", "role": "NVIDIA Free", "avatar": "🟢", "color": "#34d399", "system_prompt": "Kamu adalah NVIDIA Free, GPU-optimized free. Bahasa Indonesia.", "model_preference": ["general", "fast"]},
}

# ═══════════════════════════════════════════════════════════════
# COLLABORATION ROLES (dari LinkDiskusi)
# ═══════════════════════════════════════════════════════════════
COLLABORATION_ROLES = {
    "analyst": {"name": "Analyst", "instruction": "Kamu adalah ANALYST. Definisikan masalah, scope, constraint. Singkat: 3-5 bullet."},
    "architect": {"name": "Architect", "instruction": "Kamu adalah ARCHITECT. Rancang solusi berdasarkan definisi Analyst. Arsitektur + keputusan kunci."},
    "coder": {"name": "Coder", "instruction": "Kamu adalah CODER. Implementasi solusi berdasarkan rancangan Architect. Tulis kode bersih."},
    "reviewer": {"name": "Reviewer", "instruction": "Kamu adalah REVIEWER. Review bug, security, quality. Tandai masalah, jangan debat."},
    "strategist": {"name": "Strategist", "instruction": "Kamu adalah STRATEGIST. Rencanakan eksekusi: langkah, prioritas, timeline. Action items."},
    "summarizer": {"name": "Summarizer", "instruction": "Kamu adalah SUMMARIZER. Konsolidasikan SEMUA respon menjadi SATU jawaban akhir yang jelas."},
}

TOPIC_ROLE_MAP = {
    "code": ["analyst", "architect", "coder", "reviewer", "summarizer"],
    "strategy": ["analyst", "strategist", "summarizer"],
    "architecture": ["analyst", "architect", "reviewer", "summarizer"],
    "trading": ["analyst", "architect", "coder", "strategist", "summarizer"],
    "security": ["analyst", "reviewer", "strategist", "summarizer"],
    "general": ["analyst", "architect", "strategist", "summarizer"],
    "research": ["analyst", "strategist", "summarizer"],
    "debug": ["analyst", "coder", "reviewer", "summarizer"],
}

# ═══════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════
def get_best_model(preference=None):
    """Pilih model. Default: openrouter/free (auto-select dari 27+ free models)."""
    return "openrouter/free"


def list_all_agents():
    """Tampilkan semua AI agents."""
    print()
    print("  ==================================================")
    print(f"  AI AGENTS — {len(AI_EXECUTORS)} Total")
    print("  ==================================================")
    print()
    for key, agent in AI_EXECUTORS.items():
        model = get_best_model(agent.get("model_preference", ["general"]))
        print(f"    {key:<20s} {agent['name']:<25s} [{agent['role']}]")
    print()
    print(f"  Free Models: {len(FREE_MODELS)} tersedia via OpenRouter")
    print(f"  OpenRouter Key: {'[OK]' if OPENROUTER_KEY else '[!!] Tidak ditemukan'}")
    print()
