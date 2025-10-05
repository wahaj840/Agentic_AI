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

```bash
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




## 🚀 Day 2: Agent Architecture & Prompt Chaining

### 🎯 Objective
Implement a multi-step **agent pipeline** capable of decomposing a high-level goal into structured subtasks, executing them sequentially with LLM reasoning, and synthesizing all results into a final actionable plan.

### 🧠 Key Tasks Completed
1. **Created `agent_chain.py`** – the main agent script.
2. **Implemented 3-stage workflow:**
   - **Plan:** break a user goal into 5-10 subtasks.  
   - **Execute:** process each subtask independently using the selected LLM provider.  
   - **Synthesize:** merge all intermediate outputs into a structured final report.
3. **Integrated LLM provider routing** (Groq → HF → Ollama) with automatic fallback.
4. **Validated full pipeline** using the prompt:  
   > `"Design a lead-qualifier AI micro-SaaS for small e-commerce stores"`
5. **Tested end-to-end flow** — observed correct subtask generation, independent reasoning per subtask, and consolidated synthesis output.

### ⚙️ Technical Outcomes
- ✅ Modular architecture (`plan_task`, `execute_subtasks`, `synthesize_output`)
- ✅ Working multi-provider routing via `.env`
- ✅ No runtime or API errors
- ✅ Full reasoning trace displayed in terminal
- ✅ Business-structured final report generated automatically

### 🧩 Skills Strengthened
- Prompt-chaining logic (similar to LangChain / CrewAI)
- LLM I/O structuring and context management
- Multi-model API handling and fallback mechanisms
- Practical understanding of reasoning + synthesis loops

### 📄 Next Step
Proceed to **Day 3: Tool Integration** — adding utility modules (e.g., Google Search, file writer, or math calculator) so that the agent can reason *and act*.
