# System Architecture

Visual guide to how the Job Search AI Agent System works.

## High-Level Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Runs main.py                        │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │   Validate Config     │
                    │   (API keys, params)  │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │   Create 4 Agents     │
                    │   (powered by Claude) │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │   Create 4 Tasks      │
                    │   (with context)      │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │   CrewAI Executes     │
                    │   (Sequential)        │
                    └───────────┬───────────┘
                                │
                ┌───────────────┼───────────────┐
                ▼               ▼               ▼
        ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
        │  Task 1     │ │  Task 2     │ │  Task 3+4   │
        │  Job Search │→│  Skills     │→│  Interview  │
        │             │ │  Analysis   │ │  + Career   │
        └─────────────┘ └─────────────┘ └─────────────┘
                │
                ▼
    ┌───────────────────────────┐
    │  Final Report Saved       │
    │  outputs/report_*.txt     │
    └───────────────────────────┘
```

## Agent Details

```
┌──────────────────────────────────────────────────────────────────┐
│                        AGENT 1: Job Searcher                     │
├──────────────────────────────────────────────────────────────────┤
│ Role:      Job Search Specialist                                 │
│ Tools:     search_jobs (Adzuna API)                             │
│ Input:     Role, Location, Num Results                          │
│ Output:    5 formatted job listings with details                │
│ Context:   None (first in pipeline)                             │
└──────────────────────────────────────────────────────────────────┘
                                │
                                ▼ (job listings passed as context)
┌──────────────────────────────────────────────────────────────────┐
│                    AGENT 2: Skills Advisor                       │
├──────────────────────────────────────────────────────────────────┤
│ Role:      Skills Development Advisor                            │
│ Tools:     None (analyzes text)                                 │
│ Input:     Job listings from Agent 1                            │
│ Output:    Skills matrix + learning roadmap                     │
│ Context:   Job Search Task                                      │
└──────────────────────────────────────────────────────────────────┘
                                │
                                ▼ (job listings passed as context)
┌──────────────────────────────────────────────────────────────────┐
│                   AGENT 3: Interview Coach                       │
├──────────────────────────────────────────────────────────────────┤
│ Role:      Interview Preparation Coach                           │
│ Tools:     None (generates content)                             │
│ Input:     Job listings from Agent 1                            │
│ Output:    8-10 questions per job + guidance                    │
│ Context:   Job Search Task                                      │
└──────────────────────────────────────────────────────────────────┘
                                │
                                ▼ (job listings passed as context)
┌──────────────────────────────────────────────────────────────────┐
│                   AGENT 4: Career Advisor                        │
├──────────────────────────────────────────────────────────────────┤
│ Role:      Career Strategy Advisor                               │
│ Tools:     None (provides advice)                               │
│ Input:     Job listings from Agent 1                            │
│ Output:    Resume/LinkedIn tips + application strategy          │
│ Context:   Job Search Task                                      │
└──────────────────────────────────────────────────────────────────┘
```

## Data Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                        INPUTS (config.py)                        │
├─────────────────────────────────────────────────────────────────┤
│  • JOB_ROLE = "Data Science Intern"                            │
│  • LOCATION = "Los Angeles"                                     │
│  • NUM_RESULTS = 5                                              │
│  • ANTHROPIC_API_KEY (from .env)                               │
│  • ADZUNA_APP_ID, ADZUNA_API_KEY (from .env)                   │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    EXTERNAL API: Adzuna                          │
├─────────────────────────────────────────────────────────────────┤
│  GET https://api.adzuna.com/v1/api/jobs/us/search/1            │
│      ?app_id={id}&app_key={key}                                │
│      &what=Data Science Intern                                  │
│      &where=Los Angeles                                         │
│      &results_per_page=5                                        │
│                                                                  │
│  Response: JSON with job listings                               │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                  PROCESSING (tools.py)                           │
├─────────────────────────────────────────────────────────────────┤
│  • Parse JSON response                                          │
│  • Format each job with XML tags                                │
│  • Error handling & retries                                     │
│  • Return formatted string                                      │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│               AGENT PROCESSING (via Claude API)                  │
├─────────────────────────────────────────────────────────────────┤
│  Each agent:                                                     │
│  1. Receives task description + context                         │
│  2. Sends prompt to Claude API                                  │
│  3. Claude processes with agent's persona                       │
│  4. Returns structured response                                 │
│  5. Result saved to file (callback)                            │
│  6. Result passed to next agent (context)                      │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                        OUTPUTS                                   │
├─────────────────────────────────────────────────────────────────┤
│  outputs/                                                        │
│  ├── job_search_report_20251019_143000.txt (FULL REPORT)       │
│  ├── job_search_20251019_143000.txt                            │
│  ├── skills_analysis_20251019_143005.txt                       │
│  ├── interview_prep_20251019_143010.txt                        │
│  └── career_advisory_20251019_143015.txt                       │
└─────────────────────────────────────────────────────────────────┘
```

## Component Dependencies

```
┌─────────────┐
│   main.py   │────────┐
└──────┬──────┘        │
       │               │
       ├───────────────┼──────────────┐
       │               │              │
       ▼               ▼              ▼
┌───────────┐   ┌───────────┐  ┌───────────┐
│ agents.py │   │ tasks.py  │  │ config.py │
└─────┬─────┘   └─────┬─────┘  └─────┬─────┘
      │               │              │
      │               │              │
      └───────┬───────┴──────────────┘
              │
              ▼
        ┌───────────┐
        │ tools.py  │
        └─────┬─────┘
              │
              ▼
        ┌────────────────┐
        │  External APIs │
        │  • Adzuna      │
        │  • Anthropic   │
        └────────────────┘
```

## Module Responsibilities

### main.py
- Entry point
- Orchestrates workflow
- Handles CLI output
- Saves final report

### src/config.py
- All configuration
- Environment variables
- Validation
- Constants

### src/agents.py
- Agent definitions
- Roles, goals, backstories
- LLM configuration
- Agent factory

### src/tasks.py
- Task descriptions
- Expected outputs
- Context chaining
- Callbacks
- Task factory

### src/tools.py
- Adzuna API integration
- Error handling
- Retry logic
- Response formatting

## Best Practices Map

```
┌─────────────────────────────────────────────────────────────────┐
│                  ANTHROPIC BEST PRACTICES                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Clear Instructions ────────────▶ tasks.py (task descriptions)  │
│  XML Tags ──────────────────────▶ tools.py (job formatting)     │
│  Few-shot Examples ─────────────▶ agents.py (backstories)       │
│  Chain-of-Thought ──────────────▶ tasks.py (step-by-step)       │
│  Rich Personas ─────────────────▶ agents.py (agent roles)       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                     CREWAI PATTERNS                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Role-based Agents ─────────────▶ agents.py (4 specialists)     │
│  Task Chaining ─────────────────▶ tasks.py (context param)      │
│  Tool Pattern ──────────────────▶ tools.py (@tool decorator)    │
│  Sequential Process ────────────▶ main.py (Crew config)         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Error Handling Flow

```
API Call Attempt
      │
      ▼
  Success? ─────Yes────▶ Return Result
      │
     No
      │
      ▼
  Timeout? ────Yes────▶ Retry (up to 3 times)
      │                      │
     No                      │
      │              ┌───────┘
      ▼              ▼
  Rate Limit? ──Yes──▶ Wait & Retry
      │
     No
      │
      ▼
  Server Error? ─Yes──▶ Retry
      │
     No
      │
      ▼
  Return Error Message
  (User-friendly)
```

## Configuration Flow

```
.env.example
      │
      ▼ (user copies)
    .env ────────────▶ Environment Variables
      │                      │
      │                      ▼
      │               ┌─────────────┐
      │               │  dotenv     │
      │               │  loads vars │
      │               └──────┬──────┘
      │                      │
      ▼                      ▼
src/config.py ◀───────  Constants
      │
      ▼
validate_config()
      │
      ├──Valid──▶ Continue
      │
      └──Invalid──▶ Error & Exit
```

## Workshop Learning Path

```
┌─────────────────┐
│  1. Run System  │  Observe multi-agent collaboration
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  2. Read main   │  Understand orchestration
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  3. Read agents │  Learn agent design patterns
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  4. Modify agent│  Practice prompt engineering
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  5. Add feature │  Build something new
└─────────────────┘
```

---

This architecture enables:
- ✅ Clear separation of concerns
- ✅ Easy to understand and modify
- ✅ Follows industry best practices
- ✅ Extensible for new features
- ✅ Production-ready code quality
