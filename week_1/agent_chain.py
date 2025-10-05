from typing import List, Dict
from agent_test import run as llm_call


# -------------------------------
# PHASE 1: PLANNING
# -------------------------------

def plan(user_goal: str) -> List[str]:
    """
    Purpose:
      This function takes a broad user goal (e.g., 'Build a YouTube automation tool')
      and asks the model to break it into smaller, manageable subtasks.
    Returns:
      A Python list containing 3–5 subtasks as strings.
    """
    
    prompt = (
        "Break the user's goal into 3-5 short, actionable subtasks.\n"
        "Return ONLY a numbered list. No introduction or extra text.\n\n"
        f"User goal: {user_goal}"
    )
        # Call your LLM through the router to generate a list of subtasks.
    raw = llm_call(prompt)
    
     # We’ll now parse the model’s text output into a clean Python list.
    steps = []
    for line in raw.splitlines():  # Go through each line of model output
        line = line.strip()        # Remove any extra spaces
        if not line:
            continue               # Skip empty lines

        # Detect and remove "1. ", "2) ", etc., from the beginning of each line
        if line[0].isdigit():
            parts = line.split(" ", 1)             # Split once after first space
            step = parts[1] if len(parts) > 1 else line
        else:
            step = line

        steps.append(step)

    # Trim unwanted or too-short lines and limit to 5 subtasks max
    steps = [s for s in steps if len(s) > 3][:5]

    # Fallback (in case model fails or returns nothing)
    return steps or ["Summarize the goal.", "List 3 key steps.", "Give next actions."]


# -------------------------------
# PHASE 2: EXECUTION
# -------------------------------

def execute(user_goal: str, subtask: str) -> str:
    """
    Purpose:
      Executes one subtask at a time.
      Each subtask prompt includes context about the original goal.
    Returns:
      A string output (short explanation or list).
    """

    # Build a prompt that keeps the model focused and avoids repeating context unnecessarily.
    prompt = (
        "Complete the subtask concisely. Use bullet points if helpful.\n"
        f"Original goal: {user_goal}\n"
        f"Subtask: {subtask}\n"
    )

    # Return the result of one LLM call (trimmed of extra whitespace)
    return llm_call(prompt).strip()


# -------------------------------
# PHASE 3: SYNTHESIS
# -------------------------------

def synthesize(user_goal: str, steps: List[str], outputs: List[str]) -> str:
    """
    Purpose:
      Combines all subtask results into one final structured answer.
      Adds formatting, removes redundancy, and suggests 3 next actions.
    Returns:
      The final consolidated string (complete answer).
    """

    # Combine all steps and their corresponding outputs into one formatted block
    combined = []
    for i, (s, o) in enumerate(zip(steps, outputs), 1):
        combined.append(f"Step {i}: {s}\nResult:\n{o}")

    # Join them into one big text block with spacing
    block = "\n\n".join(combined)

    # Prompt the model to act like an "editor" that merges everything cleanly
    prompt = (
        "Merge the step results into ONE final answer. Remove repetition.\n"
        "Structure it with short sections and finish with EXACTLY 3 next actions.\n\n"
        f"User goal: {user_goal}\n\n"
        f"{block}\n\n"
        "Final consolidated answer:"
    )

    # Call LLM to perform synthesis and return the cleaned output
    return llm_call(prompt).strip()


# -------------------------------
# PHASE 4: AGENT RUNNER (Main Loop)
# -------------------------------

def run_agent(user_goal: str) -> str:
    """
    Purpose:
      Runs the full agent pipeline: plan → execute → synthesize.
      Prints intermediate results to console for transparency.
    Returns:
      The final merged answer as a string.
    """

    # === Step 1: Planning ===
    steps = plan(user_goal)
    print("📋 PLAN:")
    for i, s in enumerate(steps, 1):
        print(f"  {i}. {s}")  # Display the generated plan

    # === Step 2: Execution ===
    outputs = []
    for i, s in enumerate(steps, 1):
        print(f"\n⚙️ Subtask {i}: {s}")
        out = execute(user_goal, s)  # Solve each subtask one by one
        print(out)
        outputs.append(out)

    # === Step 3: Synthesis ===
    print("\n🧩 SYNTHESIS:")
    final_answer = synthesize(user_goal, steps, outputs)

    # Return the polished, unified output
    return final_answer


# -------------------------------
# PHASE 5: ENTRY POINT
# -------------------------------

if __name__ == "__main__":
    # You can replace this example goal with any custom query
    goal = "Design a lead-qualifier AI micro-SaaS for small e-commerce stores."

    # Run the full agent pipeline on this goal
    final = run_agent(goal)

    # Print final structured output
    print("\n===== ✅ FINAL ANSWER =====\n")
    print(final)
