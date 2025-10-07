"""
tools.py
---------
Implements simple utility tools that the AI agent can call dynamically.
Each tool follows a consistent input/output structure so it can be used interchangeably.
"""

import os
import re
from datetime import datetime

# ===============================
# 1️⃣ SEARCH TOOL  (Mock for now)
# ===============================
def search_web(query: str) -> str:
    """
    Simulates a web search.
    Later, we can connect to DuckDuckGo or Google Search APIs.
    """
    print(f"[Tool: Search] Searching the web for: {query}")
    # Return a placeholder response
    return f"Simulated web search results for '{query}'"

# ===============================
# 2️⃣ MATH TOOL
# ===============================
def solve_math(expression: str) -> str:
    """
    Evaluates basic math expressions safely.
    """
    try:
        # Only allow numbers, operators, parentheses, and dots
        if not re.match(r"^[0-9+\-*/(). ]+$", expression):
            return "Invalid or unsafe math expression."
        result = eval(expression)
        return f"The result of {expression} is {result}"
    except Exception as e:
        return f"Math error: {str(e)}"

# ===============================
# 3️⃣ FILE WRITER TOOL
# ===============================
def write_to_file(filename: str, content: str) -> str:
    """
    Writes content to a local file in the 'outputs' directory.
    """
    os.makedirs("outputs", exist_ok=True)
    file_path = os.path.join("outputs", filename)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"Saved on {datetime.now()}\n\n")
        f.write(content)

    return f"[Tool: File Writer] Content saved successfully → {file_path}"
