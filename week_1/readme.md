# 🧠 Agentic AI – Week 1 Progress Report  
**Goal:** Complete the environment setup, connect LLM providers, and push a clean, secure codebase to GitHub.  

---

## 📅 Duration  
**Day 1 — Environment Setup & Verification**

---

## ⚙️ 1️⃣ Setup Summary  

| Task | Description | Status |
|------|--------------|--------|
| Python Environment | Created and activated a virtual environment (`python –m venv .venv`) | ✅ |
| Dependency Setup | Verified pip, planned to add `requirements.txt` later | ✅ |
| Environment Variables | Created `.env.example` and `.env` for API keys | ✅ |
| Git Configuration | Added `.gitignore` for `.env`, `.venv`, and cache files | ✅ |
| GitHub Repo | Connected via `gh auth login` | ✅ |
| Push Protection Fix | Removed exposed secrets and rebuilt commit history | ✅ |
| Provider Check | Verified Groq / Hugging Face / Ollama | ✅ |
| Agent Test | Successfully ran prompts (`Say hello`, `Weather in Dublin`) | ✅ |

---

## 🧩 2️⃣ Difficulties Faced & Solutions  

| Issue | Description | Root Cause | Solution |
|-------|--------------|------------|-----------|
| **1. PowerShell Script Activation Blocked** | Error: “Running scripts is disabled on this system” when executing `.\.venv\Scripts\Activate.ps1` | Default PowerShell execution policy restricted script loading | Executed: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` |
| **2. GitHub Push Rejected – Secrets Detected** | Push blocked due to Groq API key detected in `.env.example` | GitHub push protection blocked commit history containing sensitive keys | Removed secrets and rebuilt branch via:<br>`git checkout --orphan clean-main` → `git add .` → `git push --force` |
| **3. GH CLI Login Token Error** | “Missing required scope ‘read:org’” during authentication | Incomplete OAuth permissions | Re-authenticated using `gh auth login` → selected “Login with web browser” |
| **4. Python File Not Found** | Running `python check_env.py` returned “No such file or directory” | Script was executed from the wrong directory | Navigated to correct path using `cd week_1` |
| **5. API Key Not Found** | `check_env.py` displayed “API key not found” | `.env` file not yet created locally | Duplicated `.env.example` → renamed to `.env` → added keys locally |
| **6. CLI Ampersand Error** | “& operator is not allowed” in PowerShell | PowerShell interpreted `&` as a command operator | Removed the `&` character or enclosed commands in double quotes |
| **7. Push Protection Cache Residuals** | GitHub still rejected push after removing key | Old commit history still contained key traces | Cleaned repo via:<br>`git reflog expire --expire=now --all` → `git gc --prune=now --aggressive` |
| **8. Provider Verification Failed** | Initial run didn’t detect Groq or HF | `.env` not loaded properly | Fixed with `dotenv` check in `check_env.py` |
| **9. Invalid CLI Argument** | “unrecognized arguments: --provider” | `argparse` implementation incomplete | Updated `agent_test.py` with correct argument parser |

---

## 📘 3️⃣ Key Learnings  

- Understood **how GitHub Push Protection** detects and blocks secrets.  
- Learned to **clean commit history safely** using orphan branches.  
- Gained clarity on **environment variable management** with `.env` and `.env.example`.  
- Configured **PowerShell execution policies** for virtual environments.  
- Successfully integrated and verified **Groq, Hugging Face, and Ollama providers**.  
- Confirmed **LLM agent response flow** through CLI commands.  

---

## 🧪 4️⃣ Verification Results  


# Environment check
python check_env.py
✅ GROQ_API_KEY found  
✅ HF_TOKEN found  
✅ OLLAMA_HOST set → http://localhost:11434  
🎉 At least one provider is configured.

# Agent test
python agent_test.py --prompt "What's the weather in Dublin today?"
--- Used provider: GROQ ---
(Produces detailed natural language response)
---




## 🚀 Day 2: Agent Architecture & Prompt Chaining

### 🎯 Objective
Implement a multi-step **agent pipeline** capable of decomposing a high-level goal into structured subtasks, executing them sequentially with LLM reasoning, and synthesizing all results into a final actionable plan.

---

### 🧠 Key Tasks Completed
1. **Created `agent_chain.py`** – the main agent logic file.  
2. Implemented a **3-stage reasoning workflow**:
   - **Plan:** break a complex user goal into multiple actionable subtasks.  
   - **Execute:** process each subtask independently via the chosen LLM provider (Groq → Hugging Face → Ollama fallback).  
   - **Synthesize:** merge all intermediate results into a coherent final report.  
3. Integrated **multi-provider routing** with automatic fallback based on environment variables (`.env`).  
4. Validated the full pipeline using the test prompt:  
   > `"Design a lead-qualifier AI micro-SaaS for small e-commerce stores"`  
5. Observed correct subtask generation, independent reasoning per step, and a final synthesized business plan output.

---

### ⚙️ Technical Outcomes
| Feature | Description | Status |
|----------|--------------|--------|
| Multi-provider routing | Groq → HF → Ollama fallback | ✅ |
| Modular design | Functions: `plan_task`, `execute_subtasks`, `synthesize_output` | ✅ |
| CLI Integration | Accepts `--prompt` argument for dynamic queries | ✅ |
| Output Trace | Displays reasoning flow and subtask logs in terminal | ✅ |
| Final Output | Structured and contextualized synthesis report | ✅ |

---

### 🧩 Example Run
```bash
python agent_chain.py --prompt "Design a lead-qualifier AI micro-SaaS for small e-commerce stores"


--- Used provider: GROQ ---
📋 PLAN:
  1. Conduct market research to identify target audience needs and pain points.
  2. Define the key features for the AI-powered lead qualifier.
  3. Design a user-friendly interface.
  4. Develop a machine learning model.
  5. Plan the technical infrastructure for deployment and scalability.

⚙️ Subtask 1: Conduct market research...
⚙️ Subtask 2: Define key features...
...
🧩 SYNTHESIS:
✅ Final summarized business plan generated successfully!


---

## 🚀 Day 3: Tool Integration & Smart Routing

### 🎯 Objective
Expand the agent’s capabilities by integrating **external tools** (Search / Math / File Writer) and enabling it to **decide automatically** whether to call a tool or perform reasoning through the existing chain.

---

### ⚙️ Key Tasks Completed

| Task | Description | Status |
|------|--------------|--------|
| **Tool Detection Logic** | Implemented `looks_like_tool_request()` to auto-detect when a prompt requires a tool (e.g. "search", "save", math expressions). | ✅ |
| **Tool Router (`use_tools`)** | Added central router to delegate queries to `search_web`, `solve_math`, or `write_to_file`. | ✅ |
| **Math Tool** | Performs safe calculations (e.g. `23 * 7 + 12 → 173`). | ✅ |
| **Search Tool** | Simulates web search results (`[Tool: Search] Simulated web search…`). | ✅ |
| **File Writer Tool** | Saves generated content to `outputs/agent_output.txt` with success confirmation. | ✅ |
| **Argument Parser Update** | Added `--prompt` (required) and `--act` (optional) flags to `main()`. | ✅ |
| **Smart Router Decision Flow** | Routes to either tool mode or reasoning chain based on prompt. | ✅ |
| **Full System Validation** | Successfully tested end-to-end scenarios for Reasoning and Tool modes. | ✅ |

---

### 🧪 Verification Results

```bash
# Reasoning chain
python agent_chain.py --prompt "Design a lead-qualifier AI micro-SaaS for small e-commerce stores"
# ✅ Produced multi-step plan, executed subtasks, and merged final report.

# Web search (tool mode)
python agent_chain.py --prompt "search latest AI tools 2025"
# → [Tool: Search] Simulated web search results for 'latest AI tools 2025'

# Math (tool mode)
python agent_chain.py --prompt "23 * 7 + 12"
# → The result of 23 * 7 + 12 is 173

# File write (tool mode)
python agent_chain.py --prompt "save this summary"
# → [Tool: File Writer] Content saved successfully → outputs\agent_output.txt

# Force tool mode
python agent_chain.py --act --prompt "search Mistral vs Llama benchmarks"
# → [Tool: Search] Simulated web search results for 'Mistral vs Llama benchmarks'
