# Troubleshooting Guide

Common issues and quick fixes.

## Setup Issues

### "ANTHROPIC_API_KEY is not set"
**Fix:** Create `.env` file: `cp .env.example .env` and add your API keys

### "uv: command not found"
**Fix:** Install uv: `curl -LsSf https://astral.sh/uv/install.sh | sh`, then restart terminal

### "Module not found" errors
**Fix:** Install dependencies: `uv sync`

## API Issues

### "HTTP Error 401" from Adzuna
**Fix:** Check your Adzuna credentials in `.env` - App ID should be numbers only, API key is a long string

### "Rate limit exceeded"
**Fix:** Wait a few minutes. Anthropic free tier has rate limits. Reduce `NUM_RESULTS` to use fewer API calls.

### "Request timeout"
**Fix:** Increase timeout in `src/config.py`:
```python
API_TIMEOUT = 60  # seconds
```

### "No job listings found"
**Fix:** Try:
- Broader search term (e.g., "Data" instead of "Senior Data Scientist III")
- Different location
- Check if Adzuna API is working: https://developer.adzuna.com/

## Runtime Issues

### Agents taking too long
**Fix:**
- Reduce `NUM_RESULTS` to 3-5
- Set `AGENT_VERBOSE = False` in config.py (still works, just quieter)
- Check internet connection

### Out of memory
**Fix:** Close other applications, or reduce `NUM_RESULTS`

### Script crashes mid-run
**Fix:** Check `outputs/` folder - partial results may be saved. Look for error message and search above for solution.

## Still Stuck?

1. Check error message carefully
2. Search GitHub issues
3. Ask in workshop Discord
4. Office hours: Fridays 2-4 PM

---

**Pro tip:** Most issues are API keys or internet connection. Double-check those first!
