#!/usr/bin/env python3
"""
AI AGENTS — Kopi EXACT dari LinkDiskusi ai_executor.py
======================================================
62 executor persona + 13 model API + collaborative pipeline
"""

import os
import json
import urllib.request
import time

# ═══════════════════════════════════════════════════════════════
# OPENROUTER CONFIG (EXACT dari LinkDiskusi)
# ═══════════════════════════════════════════════════════════════
OPENROUTER_BASE = "https://openrouter.ai/api/v1"

def _load_openrouter_key():
    key = os.environ.get("OPENROUTER_API_KEY", "")
    if key:
        return key
    search_paths = [
        os.path.expanduser("~/PROJECT/multi-agent-system/.env"),
        os.path.expanduser("~/PROJECT/multi-agent-system/config/.env"),
        os.path.expanduser("~/PROJECT/multi-agent-system/config/.env.bak"),
        os.path.expanduser("~/.env"),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"),
    ]
    for path in search_paths:
        if os.path.exists(path):
            try:
                with open(path) as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith("OPENROUTER_API_KEY="):
                            _, _, val = line.partition("=")
                            val = val.strip().strip('"').strip("'")
                            if val and val.startswith("sk-or-"):
                                return val
            except Exception:
                continue
    return ""

OPENROUTER_KEY = _load_openrouter_key()

# ═══════════════════════════════════════════════════════════════
# 13 FREE MODELS — EXACT dari LinkDiskusi (model ID yang di-API)
# ═══════════════════════════════════════════════════════════════
FREE_MODELS = [
    {"id": "nvidia/nemotron-3-super-120b-a12b:free", "name": "Nemotron Super 120B", "strength": "general"},
    {"id": "nvidia/nemotron-3-ultra-550b-a55b:free", "name": "Nemotron Ultra 550B", "strength": "reasoning"},
    {"id": "nvidia/nemotron-3-nano-30b-a3b:free", "name": "Nemotron Nano 30B", "strength": "fast"},
    {"id": "google/gemma-4-31b-it:free", "name": "Gemma 4 31B", "strength": "general"},
    {"id": "google/gemma-4-26b-a4b-it:free", "name": "Gemma 4 26B", "strength": "general"},
    {"id": "qwen/qwen3-next-80b-a3b-instruct:free", "name": "Qwen3 Next 80B", "strength": "reasoning"},
    {"id": "poolside/laguna-m.1:free", "name": "Laguna M.1", "strength": "code"},
    {"id": "cohere/north-mini-code:free", "name": "Cohere North Code", "strength": "code"},
    {"id": "meta-llama/llama-4-maverick:free", "name": "Llama 4 Maverick", "strength": "general"},
    {"id": "meta-llama/llama-3.3-70b-instruct:free", "name": "Llama 3.3 70B", "strength": "general"},
    {"id": "mistralai/mistral-small-3.1-24b-instruct:free", "name": "Mistral Small 3.1", "strength": "fast"},
    {"id": "deepseek/deepseek-r1:free", "name": "DeepSeek R1", "strength": "reasoning"},
    {"id": "deepseek/deepseek-chat:free", "name": "DeepSeek Chat", "strength": "general"},
]

_model_health = {}
HEALTH_COOLDOWN = 10

# ═══════════════════════════════════════════════════════════════
# 62 AI EXECUTORS — EXACT dari LinkDiskusi (persona names)
# ═══════════════════════════════════════════════════════════════
AI_EXECUTORS = {
    # CORE
    "freebuff": {"name": "Freebuff (Buffy)", "role": "Strategic AI", "system_prompt": "You are Freebuff, strategic AI analyst. Concise, data-driven.", "model_preference": ["reasoning", "general"]},
    "opencode": {"name": "OpenCode", "role": "Code AI", "system_prompt": "You are OpenCode, expert coding AI. Clean, efficient code.", "model_preference": ["code", "general"]},
    "cursor": {"name": "Cursor", "role": "Code Editor AI", "system_prompt": "You are Cursor, expert code editor. Debug, refactor, review.", "model_preference": ["code", "general"]},
    # ANTHROPIC REPLACEMENTS
    "claude-opus": {"name": "Nemotron Ultra 550B", "role": "Premium Reasoning (Free)", "system_prompt": "You are Nemotron Ultra, deep reasoning, complex analysis. Replaces Claude Opus.", "model_preference": ["reasoning", "general"]},
    "claude-sonnet": {"name": "Gemma 4 31B", "role": "Balanced AI (Free)", "system_prompt": "You are Gemma 4, balanced speed and capability. Replaces Claude Sonnet.", "model_preference": ["code", "reasoning"]},
    "claude-haiku": {"name": "Nemotron Nano 30B", "role": "Fast AI (Free)", "system_prompt": "You are Nemotron Nano, fast and efficient. Replaces Claude Haiku.", "model_preference": ["fast", "general"]},
    # OPENAI REPLACEMENTS
    "gpt-4o": {"name": "Qwen3 Next 80B", "role": "General AI (Free)", "system_prompt": "You are Qwen3 Next 80B, powerful reasoning. Replaces GPT-4o.", "model_preference": ["general", "reasoning"]},
    "gpt-4o-mini": {"name": "Groq Llama Ultra", "role": "Fast AI (Free)", "system_prompt": "You are Groq Llama, ultra-fast inference. Replaces GPT-4o Mini.", "model_preference": ["fast", "general"]},
    # GOOGLE REPLACEMENTS
    "gemini-pro": {"name": "Gemma 4 31B", "role": "Google Open (Free)", "system_prompt": "You are Gemma 4, Google open-source AI. Replaces Gemini Pro.", "model_preference": ["reasoning", "general"]},
    "gemini-flash": {"name": "Gemini 2.0 Flash", "role": "Google Fast", "system_prompt": "You are Gemini Flash, fast multimodal AI.", "model_preference": ["fast", "general"]},
    "gemma-4": {"name": "Gemma 4", "role": "Google Open", "system_prompt": "You are Gemma 4, Google open-source AI.", "model_preference": ["general", "fast"]},
    # DEEPSEEK
    "deepseek-r1": {"name": "DeepSeek R1", "role": "Reasoning AI", "system_prompt": "You are DeepSeek R1, reasoning, math, step-by-step.", "model_preference": ["reasoning", "code"]},
    "deepseek-chat": {"name": "DeepSeek Chat", "role": "DeepSeek Chat", "system_prompt": "You are DeepSeek Chat, coding, analysis, conversation.", "model_preference": ["code", "general"]},
    "deepseek-coder": {"name": "DeepSeek Coder", "role": "DeepSeek Code", "system_prompt": "You are DeepSeek Coder, expert code generation.", "model_preference": ["code", "general"]},
    # ZHIPU AI
    "glm-5.2": {"name": "GLM-5.2", "role": "Zhipu Premium", "system_prompt": "You are GLM-5.2, Chinese NLP, security, code review.", "model_preference": ["reasoning", "general"]},
    "glm-4-flash": {"name": "GLM-4 Flash", "role": "Zhipu Fast", "system_prompt": "You are GLM-4 Flash, fast QA, translation, code.", "model_preference": ["fast", "general"]},
    # MOONSHOT AI
    "kimi-k2.5": {"name": "Kimi K2.5", "role": "Moonshot Premium", "system_prompt": "You are Kimi K2.5, 256k context, vision, tools.", "model_preference": ["reasoning", "general"]},
    "kimi-k2-lite": {"name": "Kimi K2.5 Lite", "role": "Moonshot Fast", "system_prompt": "You are Kimi Lite, fast lightweight AI.", "model_preference": ["fast", "general"]},
    # ALIBABA
    "qwen-3.5": {"name": "Qwen 3.5", "role": "Alibaba Premium", "system_prompt": "You are Qwen 3.5, multi-language, coding, reasoning.", "model_preference": ["code", "reasoning"]},
    "qwen-turbo": {"name": "Qwen Turbo", "role": "Alibaba Fast", "system_prompt": "You are Qwen Turbo, fast QA, translation.", "model_preference": ["fast", "general"]},
    # META
    "llama-4": {"name": "Llama 4 Maverick", "role": "Meta Latest", "system_prompt": "You are Llama 4, Meta's latest open-source model.", "model_preference": ["general", "reasoning"]},
    "llama-3.3": {"name": "Llama 3.3 70B", "role": "Meta Stable", "system_prompt": "You are Llama 3.3, stable 70B general-purpose.", "model_preference": ["general", "reasoning"]},
    # MISTRAL
    "mistral-large": {"name": "Mistral Large", "role": "Mistral Premium", "system_prompt": "You are Mistral Large, coding, reasoning, multilingual.", "model_preference": ["code", "reasoning"]},
    "codestral": {"name": "Codestral", "role": "Mistral Code", "system_prompt": "You are Codestral, Mistral code expert.", "model_preference": ["code", "general"]},
    "mistral-small": {"name": "Mistral Small", "role": "Mistral Fast", "system_prompt": "You are Mistral Small, fast tasks, code.", "model_preference": ["fast", "general"]},
    # NVIDIA
    "nemotron-super": {"name": "Nemotron Super 120B", "role": "NVIDIA Premium", "system_prompt": "You are Nemotron Super, NVIDIA powerful model.", "model_preference": ["general", "reasoning"]},
    "nemotron-ultra": {"name": "Nemotron Ultra 550B", "role": "NVIDIA Ultra", "system_prompt": "You are Nemotron Ultra, deep reasoning, complex tasks.", "model_preference": ["reasoning", "general"]},
    "nemotron-nano": {"name": "Nemotron Nano 30B", "role": "NVIDIA Fast", "system_prompt": "You are Nemotron Nano, fast NVIDIA model.", "model_preference": ["fast", "general"]},
    # GROQ
    "groq-llama": {"name": "Groq Llama 3.3", "role": "Ultra-Fast AI", "system_prompt": "You are Groq Llama, ultra-fast inference.", "model_preference": ["fast", "general"]},
    # COHERE
    "command-r-plus": {"name": "Command R+", "role": "Cohere Premium", "system_prompt": "You are Command R+, RAG, search, generation.", "model_preference": ["general", "reasoning"]},
    # 01.AI
    "yi-lightning": {"name": "Yi Lightning", "role": "01.AI Fast", "system_prompt": "You are Yi Lightning, fast bilingual AI.", "model_preference": ["fast", "general"]},
    # SAMBANOVA
    "sambanova-llama": {"name": "SambaNova Llama", "role": "Enterprise AI", "system_prompt": "You are SambaNova Llama, enterprise inference.", "model_preference": ["general", "fast"]},
    # CEREBRAS
    "cerebras-llama": {"name": "Cerebras Llama", "role": "Wafer-Scale AI", "system_prompt": "You are Cerebras Llama, wafer-scale inference.", "model_preference": ["fast", "general"]},
    # NOVITA
    "novita-llama": {"name": "Novita Llama", "role": "Budget AI", "system_prompt": "You are Novita Llama, budget inference.", "model_preference": ["general", "fast"]},
    # TOGETHER
    "together-llama": {"name": "Together Llama", "role": "Together AI", "system_prompt": "You are Together Llama, open-source hosting.", "model_preference": ["general", "fast"]},
    # OPENROUTER
    "openrouter-auto": {"name": "OpenRouter Auto", "role": "Auto Router", "system_prompt": "You are OpenRouter, auto-routing best model.", "model_preference": ["general", "reasoning"]},
    "nine-router": {"name": "9Router", "role": "Multi-Model Router", "system_prompt": "You are 9Router, multi-model coordination.", "model_preference": ["general", "reasoning"]},
    # SPECIALIZED
    "emergent": {"name": "Emergent.sh", "role": "Emergent AI", "system_prompt": "You are Emergent, advanced analysis.", "model_preference": ["reasoning", "general"]},
    "hermes": {"name": "Hermes", "role": "Nous Hermes", "system_prompt": "You are Hermes, Nous Research AI. Creative, insightful.", "model_preference": ["general", "reasoning"]},
    "mirofish": {"name": "MiroFish", "role": "Creative AI", "system_prompt": "You are MiroFish, creative innovative solutions.", "model_preference": ["general", "reasoning"]},
    "deepagents": {"name": "DeepAgents", "role": "Planning AI", "system_prompt": "You are DeepAgents, planning and orchestration.", "model_preference": ["reasoning", "general"]},
    "egolite": {"name": "EgoLite", "role": "Web AI", "system_prompt": "You are EgoLite, web automation, research.", "model_preference": ["general", "fast"]},
    "userstrix": {"name": "UserStrix", "role": "UX AI", "system_prompt": "You are UserStrix, UX design, user experience.", "model_preference": ["general", "code"]},
    "neurobro": {"name": "NeuroBro", "role": "AI Router", "system_prompt": "You are NeuroBro, AI meta-router, workflow optimization.", "model_preference": ["general", "reasoning"]},
    "codex": {"name": "Codex", "role": "Code Generation", "system_prompt": "You are Codex, production-ready code generation.", "model_preference": ["code", "general"]},
    "openchat": {"name": "OpenChat", "role": "Open Chat AI", "system_prompt": "You are OpenChat, open-source chat AI.", "model_preference": ["general", "fast"]},
    "phi": {"name": "Phi-3 Mini", "role": "Microsoft Compact", "system_prompt": "You are Phi-3, compact but powerful.", "model_preference": ["fast", "general"]},
    "starcoder": {"name": "StarCoder", "role": "Code Completion", "system_prompt": "You are StarCoder, code completion expert.", "model_preference": ["code", "general"]},
    "perplexity": {"name": "Perplexity", "role": "Search AI", "system_prompt": "You are Perplexity, search-augmented AI. Cite sources.", "model_preference": ["general", "reasoning"]},
    "fireworks": {"name": "Fireworks", "role": "Fast Inference", "system_prompt": "You are Fireworks, fast open-source inference.", "model_preference": ["fast", "general"]},
    "cloudflare": {"name": "Cloudflare AI", "role": "Edge AI", "system_prompt": "You are Cloudflare AI, edge inference.", "model_preference": ["fast", "general"]},
    "huggingface": {"name": "HuggingFace", "role": "Open Source Hub", "system_prompt": "You are HuggingFace, open-source model hub.", "model_preference": ["general", "code"]},
    "github-copilot": {"name": "GitHub Copilot", "role": "Code Assistant", "system_prompt": "You are GitHub Copilot, code assistant.", "model_preference": ["code", "general"]},
    "lepton": {"name": "Lepton AI", "role": "Serverless AI", "system_prompt": "You are Lepton AI, serverless inference.", "model_preference": ["fast", "general"]},
    # FREE TIERS
    "kimi-free": {"name": "Kimi Free", "role": "Moonshot Free", "system_prompt": "You are Kimi Free, long context, vision.", "model_preference": ["general", "reasoning"]},
    "glm-free": {"name": "GLM Free", "role": "Zhipu Free", "system_prompt": "You are GLM Free, Chinese NLP, code.", "model_preference": ["general", "fast"]},
    "deepseek-free": {"name": "DeepSeek Free", "role": "DeepSeek Free", "system_prompt": "You are DeepSeek Free, coding, reasoning.", "model_preference": ["code", "general"]},
    "qwen-free": {"name": "Qwen Free", "role": "Alibaba Free", "system_prompt": "You are Qwen Free, multilingual, coding.", "model_preference": ["general", "fast"]},
    "groq-free": {"name": "Groq Free", "role": "Groq Free", "system_prompt": "You are Groq Free, ultra-fast free inference.", "model_preference": ["fast", "general"]},
    "mistral-free": {"name": "Mistral Free", "role": "Mistral Free", "system_prompt": "You are Mistral Free, European AI free tier.", "model_preference": ["general", "fast"]},
    "nvidia-free": {"name": "NVIDIA Free", "role": "NVIDIA Free", "system_prompt": "You are NVIDIA Free, GPU-optimized free.", "model_preference": ["general", "fast"]},
    "together-free": {"name": "Together Free", "role": "Together Free", "system_prompt": "You are Together Free, open-source free tier.", "model_preference": ["general", "fast"]},
}

# ═══════════════════════════════════════════════════════════════
# COLLABORATION ROLES — EXACT dari LinkDiskusi
# ═══════════════════════════════════════════════════════════════
COLLABORATION_ROLES = {
    "analyst": {"name": "Analyst", "instruction": "You are the ANALYST. Define the problem, scope, constraints. Be concise: 3-5 bullets."},
    "architect": {"name": "Architect", "instruction": "You are the ARCHITECT. Design the solution based on the Analyst's definition. Architecture + key decisions."},
    "coder": {"name": "Coder", "instruction": "You are the CODER. Implement the solution based on the Architect's design. Write clean code."},
    "reviewer": {"name": "Reviewer", "instruction": "You are the REVIEWER. Review for bugs, security, quality. Flag issues, don't debate."},
    "strategist": {"name": "Strategist", "instruction": "You are the STRATEGIST. Plan execution: steps, priorities, timeline. Action items."},
    "summarizer": {"name": "Summarizer", "instruction": "You are the SUMMARIZER. Consolidate ALL responses into ONE clear final answer."},
}

TOPIC_ROLE_MAP = {
    "code": ["analyst", "architect", "coder", "reviewer", "summarizer"],
    "trading": ["analyst", "architect", "coder", "strategist", "summarizer"],
    "architecture": ["analyst", "architect", "reviewer", "summarizer"],
    "security": ["analyst", "reviewer", "strategist", "summarizer"],
    "general": ["analyst", "architect", "strategist", "summarizer"],
    "debug": ["analyst", "coder", "reviewer", "summarizer"],
    "strategy": ["analyst", "strategist", "summarizer"],
    "research": ["analyst", "strategist", "summarizer"],
}

ROLE_MODEL_PREF = {
    "analyst": ["reasoning", "general"],
    "architect": ["reasoning", "general"],
    "coder": ["code", "general"],
    "reviewer": ["code", "general"],
    "strategist": ["reasoning", "general"],
    "summarizer": ["general", "reasoning"],
}

# ═══════════════════════════════════════════════════════════════
# HELPER — EXACT dari LinkDiskusi
# ═══════════════════════════════════════════════════════════════
def get_best_model(preference=None):
    """Pick best model from FREE_MODELS based on preference. EXACT dari LinkDiskusi."""
    now = time.time()
    available = [m for m in FREE_MODELS if now - _model_health.get(m["id"], 0) > HEALTH_COOLDOWN]
    if not available:
        _model_health.clear()
        available = FREE_MODELS
    if preference:
        for pref in preference:
            matched = [m for m in available if m["strength"] == pref]
            if matched:
                return matched[0]["id"]
    return available[0]["id"] if available else FREE_MODELS[0]["id"]


def assign_executors_to_roles(topic_category):
    """Assign executors to roles based on topic. EXACT dari LinkDiskusi."""
    needed_roles = TOPIC_ROLE_MAP.get(topic_category, TOPIC_ROLE_MAP["general"])
    available_executors = list(AI_EXECUTORS.keys())
    assigned, used = {}, set()

    for role in needed_roles:
        role_prefs = ROLE_MODEL_PREF.get(role, ["general"])
        best_executor = None
        best_score = -1

        for ex in available_executors:
            if ex in used:
                continue
            ex_config = AI_EXECUTORS.get(ex, {})
            ex_prefs = ex_config.get("model_preference", ["general"])
            score = sum(1 for pref in role_prefs if pref in ex_prefs)
            if score > best_score:
                best_score = score
                best_executor = ex

        if best_executor:
            assigned[role] = best_executor
            used.add(best_executor)

    return assigned


def analyze_topic(message):
    """Simple keyword topic analyzer. EXACT dari LinkDiskusi."""
    msg = message.lower()
    if any(w in msg for w in ["code", "coding", "program", "bug", "debug", "api", "function", "script", "python", "javascript"]):
        return {"category": "code", "keywords": ["code"], "confidence": 0.8}
    if any(w in msg for w in ["trade", "trading", "forex", "crypto", "stock", "bingx", "binance", "position"]):
        return {"category": "trading", "keywords": ["trading"], "confidence": 0.8}
    if any(w in msg for w in ["architect", "system design", "infrastructure", "deploy", "docker", "server"]):
        return {"category": "architecture", "keywords": ["architecture"], "confidence": 0.8}
    if any(w in msg for w in ["security", "hack", "vulnerability", "encrypt", "firewall", "shield"]):
        return {"category": "security", "keywords": ["security"], "confidence": 0.8}
    if any(w in msg for w in ["strategi", "strategy", "plan", "rencana", "bisnis", "marketing"]):
        return {"category": "strategy", "keywords": ["strategy"], "confidence": 0.8}
    if any(w in msg for w in ["riset", "research", "analisis", "data", "study"]):
        return {"category": "research", "keywords": ["research"], "confidence": 0.8}
    return {"category": "general", "keywords": [], "confidence": 0.5}


def call_openrouter(model, messages, timeout=60):
    """Call OpenRouter API with retry on 429."""
    if not OPENROUTER_KEY:
        return None
    headers = {"Authorization": f"Bearer {OPENROUTER_KEY}", "Content-Type": "application/json"}
    data = {"model": model, "messages": messages, "max_tokens": 2000, "temperature": 0.7}
    for attempt in range(3):
        try:
            req = urllib.request.Request(
                f"{OPENROUTER_BASE}/chat/completions",
                data=json.dumps(data).encode("utf-8"),
                headers=headers, method="POST",
            )
            resp = urllib.request.urlopen(req, timeout=timeout)
            result = json.loads(resp.read())
            content = result["choices"][0]["message"]["content"]
            return content if content else None
        except urllib.error.HTTPError as e:
            if e.code == 429:
                _model_health[model] = time.time()
                time.sleep(3 * (attempt + 1))
                continue
            return None
        except Exception:
            return None
    return None


def get_ai_response(executor_name, message, context="", previous_results=None):
    """Get AI response for an executor. Dengan fallback semua models."""
    executor = AI_EXECUTORS.get(executor_name)
    if not executor:
        return None

    preference = executor.get("model_preference", ["general"])
    messages = []
    if executor.get("system_prompt"):
        messages.append({"role": "system", "content": executor["system_prompt"]})
    if context:
        messages.append({"role": "system", "content": f"Context: {context[:2000]}"})

    # Build prompt with role instruction
    role_instruction = "Provide your analysis and output."
    for r, rc in COLLABORATION_ROLES.items():
        if r in message.lower() or rc["name"].lower() in message.lower():
            role_instruction = rc["instruction"]
            break

    prev_text = ""
    if previous_results:
        for prev_role, prev_result in previous_results.items():
            prev_role_name = COLLABORATION_ROLES.get(prev_role, {}).get("name", prev_role)
            prev_text += f"\n\n[{prev_role_name}]:\n{str(prev_result.get('content', ''))[:500]}"

    if prev_text:
        prompt = f"{role_instruction}\n\n{prev_text}\n\nNow, based on the above, provide your output:"
    else:
        prompt = f"{role_instruction}\n\nNow, analyze the request and provide your output:"

    messages.append({"role": "user", "content": prompt})

    # Try model based on preference
    model = get_best_model(preference)
    content = call_openrouter(model, messages)
    if content:
        return {"content": content, "model": model}

    # Fallback: try all models
    now = time.time()
    for m in FREE_MODELS:
        if now - _model_health.get(m["id"], 0) < HEALTH_COOLDOWN:
            continue
        content = call_openrouter(m["id"], messages)
        if content:
            return {"content": content, "model": m["id"]}

    # Last resort: try ALL models
    for m in FREE_MODELS:
        content = call_openrouter(m["id"], messages)
        if content:
            return {"content": content, "model": m["id"]}

    return None


def list_all_agents():
    """Tampilkan semua 62 AI agents."""
    print()
    print("  ==================================================")
    print(f"  AI AGENTS -- {len(AI_EXECUTORS)} Total (persona) + {len(FREE_MODELS)} Models (API)")
    print("  ==================================================")
    print()
    for key, agent in AI_EXECUTORS.items():
        print(f"    {key:<22s} {agent['name']:<28s} [{agent['role']}]")
    print()
    print("  --- 13 MODELS YANG DI-API KE OPENROUTER ---")
    for m in FREE_MODELS:
        print(f"    {m['id']:<55s} [{m['strength']}]")
    print()
    print(f"  OpenRouter Key: {'[OK]' if OPENROUTER_KEY else '[!!] Tidak ditemukan'}")
    print()
