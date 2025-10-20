# Setup Guide

## Quick Setup (5 Minutes)

### 1. Prerequisites
- Python 3.10+ ([Download](https://www.python.org/downloads/))
- uv package manager ([Install](https://docs.astral.sh/uv/getting-started/installation/))

### 2. Install uv

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows:**
```powershell
irm https://astral.sh/uv/install.ps1 | iex
```

### 3. Get API Keys

**Anthropic Claude:**
1. Go to https://console.anthropic.com/
2. Sign up and navigate to "API Keys"
3. Create new key (starts with `sk-ant-`)
4. Copy it

**Adzuna Jobs:**
1. Go to https://developer.adzuna.com/
2. Register for free API access
3. Get your App ID (number) and API Key (string)

### 4. Clone and Install

```bash
git clone https://github.com/your-username/job-search-agent.git
cd job-search-agent
uv sync
```

### 5. Configure

```bash
cp .env.example .env
# Edit .env and add your API keys
```

Your `.env` should look like:
```bash
ANTHROPIC_API_KEY=sk-ant-your-key-here
ADZUNA_APP_ID=12345678
ADZUNA_API_KEY=your-adzuna-key-here
```

### 6. Run!

```bash
uv run main.py
```

## Verify Setup

```bash
# Check configuration
uv run python -c "from src.config import validate_config; print(validate_config())"

# Run tests
uv run pytest
```

## Common Issues

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for solutions.

---

That's it! You're ready to go. 🚀
