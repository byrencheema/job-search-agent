"""
Configuration settings for the Job Search AI Agent System.

This file contains all configurable constants and settings that control
how the multi-agent system operates. Students can easily modify these
values to customize their job search.

Author: Claude Builder Club @ UC Irvine
Workshop: Intro to AI Agents (October 20, 2025)
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# =============================================================================
# API CONFIGURATION
# =============================================================================

# Anthropic Claude API Configuration
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
CLAUDE_MODEL = "anthropic/claude-3-5-sonnet-20241022"

# Adzuna Job Search API Configuration
ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID")
ADZUNA_API_KEY = os.getenv("ADZUNA_API_KEY")
ADZUNA_BASE_URL = "https://api.adzuna.com/v1/api/jobs"
ADZUNA_COUNTRY = "us"

# =============================================================================
# JOB SEARCH PARAMETERS (TODO: CUSTOMIZE THESE FOR YOUR JOB SEARCH!)
# =============================================================================

# Default job search configuration
# Students: Change these values to match your desired job search!
DEFAULT_JOB_ROLE = "Software Engineering Intern"
DEFAULT_LOCATION = "Los Angeles"
DEFAULT_NUM_RESULTS = 5  # Number of job listings to retrieve

# =============================================================================
# AGENT CONFIGURATION
# =============================================================================

# Agent verbosity - Set to True to see detailed agent thinking process
# This is helpful for learning and debugging!
AGENT_VERBOSE = True

# Agent delegation - Allow agents to delegate tasks to each other
AGENT_ALLOW_DELEGATION = False  # Disabled to reduce API calls and avoid rate limits

# Memory settings - Agents can remember context from previous interactions
AGENT_MEMORY = True

# =============================================================================
# OUTPUT CONFIGURATION
# =============================================================================

# Output directory for generated reports
OUTPUT_DIR = Path(__file__).parent.parent / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

# Report filename format (includes timestamp)
REPORT_FILENAME_FORMAT = "job_search_report_{timestamp}.txt"

# Console output settings
SHOW_PROGRESS_MESSAGES = True
SHOW_AGENT_OUTPUTS = True

# =============================================================================
# API SETTINGS & TIMEOUTS
# =============================================================================

# HTTP request timeout (seconds)
API_TIMEOUT = 30

# Number of retries for failed API calls
API_MAX_RETRIES = 3

# Delay between retries (seconds)
API_RETRY_DELAY = 2

# =============================================================================
# CREWAI PROCESS CONFIGURATION
# =============================================================================

# Process type: "sequential" or "hierarchical"
# Sequential: Agents work one after another in order
# Hierarchical: A manager agent coordinates worker agents
CREW_PROCESS = "sequential"

# =============================================================================
# VALIDATION FUNCTIONS
# =============================================================================

def validate_config() -> tuple[bool, list[str]]:
    """
    Validate that all required configuration is present and valid.

    Returns:
        tuple[bool, list[str]]: (is_valid, list of error messages)

    Following Anthropic best practice: Clear, explicit validation with
    structured error reporting.
    """
    errors = []

    # Check required API keys
    if not ANTHROPIC_API_KEY:
        errors.append("ANTHROPIC_API_KEY is not set. Please add it to your .env file.")

    if not ADZUNA_APP_ID:
        errors.append("ADZUNA_APP_ID is not set. Please add it to your .env file.")

    if not ADZUNA_API_KEY:
        errors.append("ADZUNA_API_KEY is not set. Please add it to your .env file.")

    # Validate job search parameters
    if not DEFAULT_JOB_ROLE or len(DEFAULT_JOB_ROLE.strip()) == 0:
        errors.append("DEFAULT_JOB_ROLE cannot be empty.")

    if not DEFAULT_LOCATION or len(DEFAULT_LOCATION.strip()) == 0:
        errors.append("DEFAULT_LOCATION cannot be empty.")

    if DEFAULT_NUM_RESULTS < 1 or DEFAULT_NUM_RESULTS > 50:
        errors.append("DEFAULT_NUM_RESULTS must be between 1 and 50.")

    # Validate model name
    if not CLAUDE_MODEL or not CLAUDE_MODEL.startswith("anthropic/"):
        errors.append("CLAUDE_MODEL must be a valid Claude model name with 'anthropic/' prefix.")

    is_valid = len(errors) == 0
    return is_valid, errors


def print_config() -> None:
    """
    Print current configuration (useful for debugging).

    Note: API keys are masked for security.
    """
    print("\n" + "="*70)
    print("JOB SEARCH AI AGENT - CONFIGURATION")
    print("="*70)
    print(f"\n📋 Job Search Settings:")
    print(f"   Role: {DEFAULT_JOB_ROLE}")
    print(f"   Location: {DEFAULT_LOCATION}")
    print(f"   Number of Results: {DEFAULT_NUM_RESULTS}")
    print(f"\n🤖 Agent Settings:")
    print(f"   Model: {CLAUDE_MODEL}")
    print(f"   Verbose: {AGENT_VERBOSE}")
    print(f"   Allow Delegation: {AGENT_ALLOW_DELEGATION}")
    print(f"\n🔑 API Keys:")
    print(f"   Anthropic API: {'✓ Set' if ANTHROPIC_API_KEY else '✗ Missing'}")
    print(f"   Adzuna App ID: {'✓ Set' if ADZUNA_APP_ID else '✗ Missing'}")
    print(f"   Adzuna API Key: {'✓ Set' if ADZUNA_API_KEY else '✗ Missing'}")
    print(f"\n📂 Output:")
    print(f"   Directory: {OUTPUT_DIR}")
    print("="*70 + "\n")


# =============================================================================
# EXPORT ALL SETTINGS
# =============================================================================

__all__ = [
    # API Settings
    "ANTHROPIC_API_KEY",
    "CLAUDE_MODEL",
    "ADZUNA_APP_ID",
    "ADZUNA_API_KEY",
    "ADZUNA_BASE_URL",
    "ADZUNA_COUNTRY",

    # Job Search Settings
    "DEFAULT_JOB_ROLE",
    "DEFAULT_LOCATION",
    "DEFAULT_NUM_RESULTS",

    # Agent Settings
    "AGENT_VERBOSE",
    "AGENT_ALLOW_DELEGATION",
    "AGENT_MEMORY",

    # Output Settings
    "OUTPUT_DIR",
    "REPORT_FILENAME_FORMAT",
    "SHOW_PROGRESS_MESSAGES",
    "SHOW_AGENT_OUTPUTS",

    # API Settings
    "API_TIMEOUT",
    "API_MAX_RETRIES",
    "API_RETRY_DELAY",

    # CrewAI Settings
    "CREW_PROCESS",

    # Functions
    "validate_config",
    "print_config",
]
