# Workshop Instructor Guide

Quick reference for running the "Intro to AI Agents" workshop at UC Irvine.

## Workshop Details
- **Date:** October 20, 2025
- **Duration:** 90 minutes total
- **Hands-on coding:** 40 minutes
- **Audience:** 50+ students (CS majors + non-technical)
- **Goal:** Students leave with a working job search system

## Timeline (90 minutes)

### Part 1: Introduction (15 min)
- What are AI agents? (5 min)
- Demo of the system (5 min)
- Setup verification (5 min)

### Part 2: Code Walkthrough (20 min)
- Architecture overview (5 min)
- Agents deep-dive (5 min)
- Tasks and tools (5 min)
- Best practices highlights (5 min)

### Part 3: Hands-on Coding (40 min)
- Run default example (5 min)
- Customize search parameters (10 min)
- Modify an agent (15 min)
- Try adding features (10 min)

### Part 4: Wrap-up (15 min)
- Show results (5 min)
- Q&A (10 min)

## Pre-Workshop Setup

### 1. Test the System
```bash
cd job-search-agent
uv run main.py
```

### 2. Prepare API Keys
- Have backup Anthropic API keys ready (in case students have issues)
- Remind students to get Adzuna keys before workshop

### 3. Check Examples
Verify `examples/example_output.txt` displays correctly

## Student Setup (First 5 Minutes)

**Quick checklist for students:**
```bash
# 1. Clone
git clone <repo-url>
cd job-search-agent

# 2. Install
uv sync

# 3. Configure
cp .env.example .env
# Add API keys to .env

# 4. Test
uv run python -c "from src.config import validate_config; print(validate_config())"
```

## Code Walkthrough Order

### 1. Start with `main.py`
Show how it orchestrates everything

### 2. Show `src/agents.py`
- Point out agent backstories (best practice)
- Show how role/goal/tools work
- Highlight one agent in detail

### 3. Show `src/tasks.py`
- Explain task descriptions (prompts)
- Show context chaining
- Point out expected_output

### 4. Show `src/tools.py`
- Explain the Adzuna integration
- Show error handling
- Discuss XML formatting

### 5. Highlight `src/config.py`
- Easy customization points
- Environment variables

## Hands-on Activities

### Activity 1: Run Default (5 min)
```bash
uv run main.py
```
Students observe the output, see agents working.

### Activity 2: Customize Search (10 min)
Students edit `main.py` lines 40-45:
```python
JOB_ROLE = "Software Engineer"  # Change this
LOCATION = "San Francisco"       # Change this
NUM_RESULTS = 10                 # Change this
```

### Activity 3: Modify Agent (15 min)
Students edit an agent backstory in `src/agents.py` to change focus.

**Example challenge:**
"Make the Skills Advisor only recommend free resources"

**Solution location:** `docs/CUSTOMIZATION.md`

### Activity 4: Extension (10 min)
**Choose one:**
- Add command-line arguments
- Make search interactive (use `input()`)
- Change output format
- Reduce verbosity

## Common Student Issues

### "My API key isn't working"
- Check for extra spaces in `.env`
- Verify key format (Anthropic starts with `sk-ant-`)
- Try regenerating the key

### "It's too slow"
- Reduce `NUM_RESULTS` to 3
- Set `AGENT_VERBOSE = False`
- Expected: 3-5 minutes per run

### "Import errors"
- Run `uv sync` again
- Check they're in the right directory
- Verify Python 3.10+

### "No jobs found"
- Try broader search terms
- Different location
- Check Adzuna API is working

## Demo Script

### Opening Demo (5 min)

```bash
# Show this on screen
uv run main.py

# While it runs, explain:
# "This is searching for Data Science Intern jobs in LA..."
# "Now the Skills Advisor is analyzing required skills..."
# "Interview Coach is generating questions..."
# "Career Advisor is providing application strategies..."

# Show the final report
cat outputs/job_search_report_*.txt | less
```

### Live Coding Demo (10 min)

```python
# Show how to customize an agent
# File: src/agents.py

def create_skills_advisor_agent() -> Agent:
    return Agent(
        role='Skills Development Advisor',
        goal='...',
        backstory=(
            # MODIFY THIS LIVE
            'You are super enthusiastic and use lots of emojis! '
            'You make learning fun and exciting! 🎉📚✨\n\n'
            # ... rest
        ),
    )
```

Run again and show the difference!

## Key Talking Points

### Why This Matters
- **Practical:** Students can actually use this for job searches
- **Educational:** Learn real multi-agent patterns
- **Production-ready:** Error handling, testing, best practices
- **Extensible:** Easy to add features

### Best Practices to Highlight
1. **Clear prompts** - Specific instructions get better results
2. **XML tags** - Structure helps Claude parse better
3. **Agent backstories** - Rich context improves output
4. **Error handling** - Production code needs retries
5. **Modular design** - Easy to extend and maintain

### What Students Learn
- Multi-agent collaboration
- Prompt engineering
- API integration
- Real-world project structure
- Claude best practices

## Extension Ideas for Advanced Students

1. Add more job boards (Indeed, LinkedIn)
2. Add resume parser tool
3. Create web UI with Streamlit
4. Add salary research agent
5. Export to PDF
6. Email the report
7. Schedule weekly searches

## Resources to Share

- **This repo:** GitHub link
- **CrewAI docs:** https://docs.crewai.com/
- **Anthropic docs:** https://docs.anthropic.com/
- **Workshop Discord:** [Link]
- **Office hours:** Fridays 2-4 PM

## Post-Workshop

### Share with students:
- Link to completed code
- Recording (if available)
- Additional resources in `docs/BEST_PRACTICES.md`
- Encourage them to customize and share

### Feedback Form
- What worked well?
- What was confusing?
- What would they like to learn next?

## Backup Plans

### If API is down:
- Show pre-recorded demo
- Walk through code without running
- Use example output file

### If students can't get setup working:
- Pair up students (working setup shares screen)
- Use GitHub Codespaces
- Provide backup environment

### If running long:
- Skip Activity 4 (extension)
- Condense Q&A
- Share resources for later

## Success Metrics

Students should be able to:
- ✅ Run the system successfully
- ✅ Customize search parameters
- ✅ Understand agent roles
- ✅ Modify at least one agent
- ✅ Explain how multi-agent collaboration works

## Contact

Questions? Reach out:
- Workshop Discord
- GitHub issues
- Office hours

---

**Good luck with the workshop! 🚀**

This is a great introduction to AI agents. Keep it fun and practical!
