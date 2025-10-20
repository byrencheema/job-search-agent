# Customization Guide

Quick guide to customizing the system for your needs.

## Change Job Search Parameters

**File:** `main.py` (lines 40-45)

```python
JOB_ROLE = "Machine Learning Engineer"  # Change this
LOCATION = "San Francisco"               # Change this
NUM_RESULTS = 10                         # Change this (1-50)
```

## Modify Agent Focus

**File:** `src/agents.py`

### Example: Make Skills Advisor recommend only free resources

```python
# In create_skills_advisor_agent(), modify backstory:
backstory=(
    'You are a career coach who ONLY recommends FREE resources:\n'
    '- Free Coursera courses (audit option)\n'
    '- YouTube tutorials\n'
    '- Free coding bootcamps\n'
    '- Open-source projects\n\n'
    # ... rest of backstory
)
```

### Example: Make Interview Coach focus on technical questions

```python
# In create_interview_coach_agent(), modify goal:
goal=(
    'Generate 10-15 TECHNICAL interview questions for {role} positions, '
    'focusing 80% on coding, system design, and technical problem-solving.'
),
```

## Change LLM Model

**File:** `src/config.py`

```python
# Faster, cheaper
CLAUDE_MODEL = "claude-haiku-4-5-20250815"

# Default (balanced)
CLAUDE_MODEL = "claude-sonnet-4-5-20251022"

# Most powerful
CLAUDE_MODEL = "claude-opus-4-20250514"
```

## Add a New Agent

See full example in [BEST_PRACTICES.md](BEST_PRACTICES.md), but the steps are:

1. Create agent function in `src/agents.py`
2. Create task function in `src/tasks.py`
3. Add to `create_all_agents()` and `create_all_tasks()`
4. Update `main.py` console output

## Reduce Verbosity

**File:** `src/config.py`

```python
AGENT_VERBOSE = False  # Less output, faster runs
```

## Make Search Interactive

**File:** `main.py` (replace lines 40-45)

```python
JOB_ROLE = input("Job role: ").strip()
LOCATION = input("Location: ").strip()
NUM_RESULTS = int(input("# of results: ").strip() or "5")
```

Now run with: `uv run main.py`

---

That's the essentials! For more, see the code comments - they're detailed.
