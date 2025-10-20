# 🤖 Job Search AI Agent System

> **Multi-agent job search automation using CrewAI + Claude**
>
> Built for UC Irvine Claude Builder Club's "Intro to AI Agents" workshop (October 20, 2025)

Stop manually searching for jobs, analyzing requirements, and preparing for interviews. Let AI agents do the heavy lifting while you focus on landing your dream role.

This system uses **4 specialized AI agents** that collaborate to give you:
- 🔍 **Current job listings** from real APIs (Adzuna)
- 📚 **Personalized skills roadmap** - what to learn and how
- 🎤 **Interview prep materials** - questions + strategies
- 💼 **Career advice** - resume, LinkedIn, and application tips

**All in one automated report. All tailored to your specific job search.**

---

## 🎯 What Makes This Cool?

1. **Real multi-agent collaboration** - Agents pass context to each other, building on previous work
2. **Powered by Claude (Anthropic)** - State-of-the-art AI with excellent reasoning
3. **Live job data** - Integrates with Adzuna API for real, current job listings
4. **Production-ready code** - Error handling, retries, logging, tests
5. **Actually useful** - Generate a report you can use for your real job search

### Example Output

After running `uv run main.py`, you get a comprehensive report with:

```
✅ 5 Data Science Intern jobs in Los Angeles
📊 Analysis of required skills across all listings
📚 Learning roadmap: "Start with Python basics (2-3 weeks), then..."
🎤 10 interview questions per role with STAR method guidance
💼 Resume keywords to add, LinkedIn optimization tips, networking strategies
```

See [examples/example_output.txt](examples/example_output.txt) for a full sample report.

---

## 🚀 Quick Start (5 Minutes)

### Prerequisites

- **Python 3.10+** ([Download](https://www.python.org/downloads/))
- **uv package manager** ([Install](https://docs.astral.sh/uv/getting-started/installation/))
- **Anthropic API key** ([Get one](https://console.anthropic.com/))
- **Adzuna API credentials** ([Sign up - free](https://developer.adzuna.com/))

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-username/job-search-agent.git
cd job-search-agent

# 2. Install dependencies with uv
uv sync

# 3. Set up environment variables
cp .env.example .env
# Edit .env and add your API keys

# 4. Run the system!
uv run main.py
```

That's it! The system will:
1. Search for jobs (default: "Data Science Intern" in "Los Angeles")
2. Analyze required skills
3. Generate interview prep materials
4. Provide career strategy advice
5. Save everything to `outputs/job_search_report_[timestamp].txt`

---

## 📋 Detailed Setup

### Step 1: Get API Keys

#### Anthropic Claude API

1. Go to [console.anthropic.com](https://console.anthropic.com/)
2. Sign up for an account
3. Navigate to "API Keys"
4. Create a new API key
5. Copy the key (starts with `sk-ant-...`)
6. **Note:** You may need to add credits ($5 minimum). First-time users often get free credits.

#### Adzuna Job Search API

1. Go to [developer.adzuna.com](https://developer.adzuna.com/)
2. Click "Register for API access"
3. Fill out the form (it's free!)
4. You'll receive:
   - App ID (a number)
   - API Key (a long string)
5. **Free tier:** 250 API calls/month (more than enough for this workshop)

### Step 2: Configure Environment

```bash
# Copy the example environment file
cp .env.example .env
```

Edit `.env` in your text editor:

```bash
# Add your actual keys here
ANTHROPIC_API_KEY=sk-ant-your-key-here
ADZUNA_APP_ID=12345
ADZUNA_API_KEY=your-adzuna-key-here
```

**Important:** Never commit `.env` to Git! It's already in `.gitignore` for safety.

### Step 3: Install Dependencies

Using uv (recommended):
```bash
uv sync
```

Or using traditional pip:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 4: Verify Setup

Test that everything is configured correctly:

```bash
uv run python -c "from src.config import validate_config, print_config; print_config(); print(validate_config())"
```

You should see your configuration printed with ✓ marks for all API keys.

---

## 🎮 Usage

### Basic Usage

Run with default settings (Data Science Intern in Los Angeles):

```bash
uv run main.py
```

### Customize Your Search

Edit `main.py` to change search parameters:

```python
# At the top of main.py, change these:
JOB_ROLE = "Machine Learning Engineer"  # Your desired role
LOCATION = "San Francisco"               # Your target location
NUM_RESULTS = 10                         # How many jobs to analyze
```

Then run:
```bash
uv run main.py
```

### What You'll See

The system runs for 3-5 minutes, showing:
1. ✅ Configuration validation
2. 🤖 Agent creation
3. 📋 Task setup
4. 🚀 Execution with detailed agent outputs
5. 💾 Final report saved

### Output Files

All outputs saved to `outputs/` folder:
- `job_search_report_[timestamp].txt` - **Full combined report**
- `job_search_[timestamp].txt` - Job listings only
- `skills_analysis_[timestamp].txt` - Skills roadmap only
- `interview_prep_[timestamp].txt` - Interview questions only
- `career_advisory_[timestamp].txt` - Career advice only

---

## 🛠️ Customization

### Change Job Search Parameters

**Option 1:** Edit `main.py` directly

```python
JOB_ROLE = "Product Manager"
LOCATION = "Remote"
NUM_RESULTS = 15
```

**Option 2:** Edit `src/config.py` to change defaults

```python
DEFAULT_JOB_ROLE = "Software Engineer"
DEFAULT_LOCATION = "New York"
DEFAULT_NUM_RESULTS = 10
```

### Modify Agent Behavior

Want agents to focus on different things? Edit agent backstories in `src/agents.py`:

```python
# Example: Make Skills Advisor focus on online courses
backstory=(
    'You are a learning specialist who specializes in online education '
    'platforms like Coursera, Udemy, and DataCamp. You always recommend '
    'specific courses with links...'
)
```

### Add New Agents

Want a 5th agent (e.g., Salary Negotiation Coach)? See [docs/CUSTOMIZATION.md](docs/CUSTOMIZATION.md) for a step-by-step guide.

### Change LLM Model

Using a different Claude model:

```python
# src/config.py
CLAUDE_MODEL = "claude-opus-4-20250514"  # More powerful but slower
# or
CLAUDE_MODEL = "claude-haiku-4-5-20250815"  # Faster and cheaper
```

---

## 📁 Project Structure

```
job-search-agent/
├── README.md                 # You are here!
├── pyproject.toml           # uv project configuration
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
├── .gitignore              # Git ignore rules
│
├── main.py                 # 🚀 Main entry point - RUN THIS!
│
├── src/                    # Source code
│   ├── __init__.py
│   ├── config.py          # Configuration and settings
│   ├── agents.py          # 4 AI agent definitions
│   ├── tasks.py           # 4 task definitions
│   └── tools.py           # Adzuna API integration
│
├── tests/                  # Test files
│   ├── __init__.py
│   └── test_tools.py      # Unit tests for tools
│
├── outputs/                # Generated reports go here
│   └── .gitkeep
│
├── examples/               # Example files
│   └── example_output.txt # Sample report
│
└── docs/                   # Documentation
    ├── BEST_PRACTICES.md  # Design patterns used
    ├── SETUP.md           # Detailed setup guide
    ├── CUSTOMIZATION.md   # How to customize
    └── TROUBLESHOOTING.md # Common issues + fixes
```

---

## 🧪 Running Tests

Verify your setup with tests:

```bash
# Run all tests
uv run pytest

# Run tests with verbose output
uv run pytest -v

# Run only tool tests
uv run pytest tests/test_tools.py

# Run with coverage report
uv run pytest --cov=src
```

---

## 🐛 Troubleshooting

### "Configuration Error: ANTHROPIC_API_KEY is not set"

**Solution:** Make sure you've created `.env` file (copy from `.env.example`) and added your API key.

### "HTTP Error 401" from Adzuna API

**Solution:** Check that your Adzuna credentials are correct in `.env`. The App ID should be just numbers, the API key is a long string.

### "Module not found" errors

**Solution:** Make sure you've installed dependencies:
```bash
uv sync
```

### Agents are taking too long / timing out

**Solution:**
1. Reduce `NUM_RESULTS` to 3-5 jobs
2. Check your internet connection
3. Adzuna API might be slow - wait and retry

### "Rate limit exceeded" from Anthropic

**Solution:** You've hit the API rate limit. Wait a few minutes or upgrade your Anthropic plan.

For more issues, see [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)

---

## 📚 How It Works

### Architecture Overview

```
┌─────────────┐
│   main.py   │  Entry point, orchestrates everything
└──────┬──────┘
       │
       ├─> Creates Agents (from agents.py)
       │   ├── Job Searcher (uses Adzuna API tool)
       │   ├── Skills Advisor (analyzes jobs)
       │   ├── Interview Coach (generates questions)
       │   └── Career Advisor (strategic advice)
       │
       ├─> Creates Tasks (from tasks.py)
       │   ├── Job Search Task → Skills Task
       │   ├── Skills Task   → Interview Task
       │   └── Interview Task → Career Task
       │
       └─> Creates Crew (CrewAI)
           └─> Sequential execution
               └─> Each agent completes their task
                   └─> Results saved & passed to next
```

### Agent Flow

1. **Job Searcher Agent** calls Adzuna API → finds 5 jobs in Los Angeles
2. **Skills Advisor Agent** receives job listings → analyzes required skills → creates learning roadmap
3. **Interview Coach Agent** receives job listings → generates 8-10 questions per role → provides STAR method guidance
4. **Career Advisor Agent** receives job listings → gives resume tips, LinkedIn optimization, networking strategies

All agents use **Claude (Anthropic)** as their LLM brain.

### Key Technologies

- **CrewAI** - Multi-agent orchestration framework
- **LangChain** - LLM framework integration layer
- **Anthropic Claude** - Latest Sonnet 4.5 model for reasoning
- **Adzuna API** - Real job search data
- **Python 3.10+** - Modern Python with type hints

---

## 🎓 Learning Resources

### Understand the Code

1. **Start with:** [docs/BEST_PRACTICES.md](docs/BEST_PRACTICES.md) - Learn the design patterns used
2. **Read the code:** Start with `main.py`, then `agents.py`, then `tasks.py`
3. **Experiment:** Change one thing, run it, see what happens

### Learn More About AI Agents

- **CrewAI Docs:** https://docs.crewai.com/
- **Anthropic Prompt Engineering:** https://docs.anthropic.com/prompt-engineering
- **DeepLearning.AI Course:** [Multi-Agent Systems with CrewAI](https://www.deeplearning.ai/short-courses/multi-ai-agent-systems-with-crewai/)

### Learn More About the APIs

- **Adzuna API Docs:** https://developer.adzuna.com/
- **Anthropic API Reference:** https://docs.anthropic.com/claude/reference

---

## 🤝 Contributing

Want to improve this project? Contributions welcome!

### Ideas for Enhancements

- [ ] Add more job boards (Indeed, LinkedIn, Glassdoor)
- [ ] Salary analysis agent
- [ ] Company culture research agent
- [ ] Resume parser tool (upload your resume, get personalized advice)
- [ ] Email cover letter generator
- [ ] Job application tracker
- [ ] Interview scheduling assistant
- [ ] Web UI with Streamlit or Gradio

### How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests if applicable
5. Update documentation
6. Submit a pull request

---

## 📄 License

MIT License - Feel free to use this for learning, projects, or your actual job search!

---

## 🙏 Acknowledgments

- **UC Irvine Claude Builder Club** - For organizing the workshop
- **Anthropic** - For Claude and excellent documentation
- **CrewAI** - For making multi-agent systems accessible
- **Adzuna** - For providing free job search API access
- **All workshop participants** - For being awesome!

---

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/your-username/job-search-agent/issues)
- **Discussions:** [GitHub Discussions](https://github.com/your-username/job-search-agent/discussions)
- **Workshop Discord:** [Join here]
- **Office Hours:** Fridays 2-4 PM at UCI

---

## 🎉 Next Steps

After completing the workshop:

1. ✅ Run the system with your own job search criteria
2. ✅ Read the generated report and use it for your real job search
3. ✅ Customize one agent to better match your needs
4. ✅ Add a new feature (maybe a 5th agent?)
5. ✅ Share your improvements with the community!
6. ✅ Land your dream job! 🚀

---

**Built with ❤️ for UC Irvine Claude Builder Club**

*Happy job hunting! May your agents find you the perfect role.* 🎯

---

**Workshop Date:** October 20, 2025
**Version:** 1.0.0
**Last Updated:** October 19, 2025
