# 🧠 Agentic AI – Week 1 Setup

This project is part of my AI learning roadmap.  
It sets up a local environment to test LLM integrations (Groq, Hugging Face, etc.) safely using `.env` files.

---

## ⚙️ Setup Instructions

```bash
# Clone repository
git clone https://github.com/wahaj840/Agentic_AI.git
cd Agentic_AI/week_1

# Create a virtual environment
python -m venv .venv

# Activate it (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt  # (create this later if needed)

# Copy the environment example
copy .env.example .env

# Edit .env to include your real API keys locally
# Example:
# GROQ_API_KEY=your_real_key_here
