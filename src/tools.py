"""
Custom tools for the Job Search AI Agent System.

This module contains the JobSearchTool that integrates with the Adzuna API
to fetch real-time job listings. Tools in CrewAI are functions that agents
can use to interact with external systems.

Author: Claude Builder Club @ UC Irvine
Workshop: Intro to AI Agents (October 20, 2025)

Best Practices Applied:
- Anthropic: Clear error handling with structured responses
- CrewAI: Tool pattern with explicit input/output schemas
- Python: Type hints and comprehensive docstrings
"""

import json
import time
import requests
from typing import Any, Dict, List, Optional
from crewai.tools import tool

from src.config import (
    ADZUNA_APP_ID,
    ADZUNA_API_KEY,
    ADZUNA_BASE_URL,
    ADZUNA_COUNTRY,
    API_TIMEOUT,
    API_MAX_RETRIES,
    API_RETRY_DELAY,
)


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def _make_api_request_with_retry(
    url: str,
    max_retries: int = API_MAX_RETRIES,
    timeout: int = API_TIMEOUT
) -> Optional[Dict[str, Any]]:
    """
    Make an API request with retry logic for robustness.

    Following best practice: Graceful error handling for production systems.

    Args:
        url: The full URL to request
        max_retries: Maximum number of retry attempts
        timeout: Request timeout in seconds

    Returns:
        JSON response as dictionary, or None if all retries fail
    """
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()  # Raises HTTPError for bad status codes
            return response.json()

        except requests.exceptions.HTTPError as e:
            # HTTP errors (4xx, 5xx)
            if response.status_code == 429:  # Rate limit
                print(f"⚠️  Rate limited. Waiting {API_RETRY_DELAY}s before retry {attempt + 1}/{max_retries}...")
                time.sleep(API_RETRY_DELAY)
                continue
            elif response.status_code >= 500:  # Server error
                print(f"⚠️  Server error. Retry {attempt + 1}/{max_retries}...")
                time.sleep(API_RETRY_DELAY)
                continue
            else:
                print(f"❌ HTTP Error {response.status_code}: {str(e)}")
                return None

        except requests.exceptions.Timeout:
            print(f"⚠️  Request timeout. Retry {attempt + 1}/{max_retries}...")
            if attempt < max_retries - 1:
                time.sleep(API_RETRY_DELAY)
                continue
            else:
                print("❌ Max retries reached. Request timed out.")
                return None

        except requests.exceptions.ConnectionError:
            print(f"⚠️  Connection error. Retry {attempt + 1}/{max_retries}...")
            if attempt < max_retries - 1:
                time.sleep(API_RETRY_DELAY)
                continue
            else:
                print("❌ Max retries reached. Connection failed.")
                return None

        except requests.exceptions.RequestException as e:
            print(f"❌ Request error: {str(e)}")
            return None

        except json.JSONDecodeError:
            print("❌ Invalid JSON response from API")
            return None

    return None


def _format_job_listing(job: Dict[str, Any]) -> str:
    """
    Format a single job listing into a readable string.

    Following Anthropic best practice: Structured output with XML-style tags
    for better parsing by LLMs.

    Args:
        job: Job data dictionary from Adzuna API

    Returns:
        Formatted job listing string
    """
    # Extract fields safely with defaults
    title = job.get('title', 'N/A')
    company = job.get('company', {}).get('display_name', 'N/A')
    location = job.get('location', {}).get('display_name', 'N/A')
    description = job.get('description', 'No description available')
    salary_min = job.get('salary_min')
    salary_max = job.get('salary_max')
    url = job.get('redirect_url', 'N/A')
    created = job.get('created', 'N/A')

    # Format salary information
    salary_info = "Not specified"
    if salary_min and salary_max:
        salary_info = f"${salary_min:,.0f} - ${salary_max:,.0f}"
    elif salary_min:
        salary_info = f"From ${salary_min:,.0f}"
    elif salary_max:
        salary_info = f"Up to ${salary_max:,.0f}"

    # Truncate description to keep output manageable
    max_description_length = 500
    if len(description) > max_description_length:
        description = description[:max_description_length] + "..."

    # Format using XML-style tags (Claude best practice)
    formatted = f"""
<job>
    <title>{title}</title>
    <company>{company}</company>
    <location>{location}</location>
    <salary>{salary_info}</salary>
    <posted_date>{created}</posted_date>
    <description>
        {description}
    </description>
    <apply_url>{url}</apply_url>
</job>
"""
    return formatted.strip()


def _validate_search_input(input_data: Dict[str, Any]) -> tuple[bool, str]:
    """
    Validate job search input parameters.

    Args:
        input_data: Dictionary with role, location, num_results

    Returns:
        Tuple of (is_valid, error_message)
    """
    required_fields = ['role', 'location', 'num_results']

    # Check all required fields are present
    for field in required_fields:
        if field not in input_data:
            return False, f"Missing required field: '{field}'"

    # Validate role
    role = input_data['role']
    if not isinstance(role, str) or len(role.strip()) == 0:
        return False, "Role must be a non-empty string"

    # Validate location
    location = input_data['location']
    if not isinstance(location, str) or len(location.strip()) == 0:
        return False, "Location must be a non-empty string"

    # Validate num_results
    num_results = input_data['num_results']
    if not isinstance(num_results, int):
        return False, "num_results must be an integer"
    if num_results < 1 or num_results > 50:
        return False, "num_results must be between 1 and 50"

    return True, ""


# =============================================================================
# CREWAI TOOL: JOB SEARCH
# =============================================================================

@tool("Job Search Tool")
def search_jobs(role: str, location: str, num_results: int) -> str:
    """
    Search for job listings using the Adzuna API.

    This tool is designed to be used by AI agents in the CrewAI framework.
    It accepts job search parameters and returns formatted job listings.

    Following best practices:
    - CrewAI Tool Pattern: Clear input/output schema with direct parameters
    - Anthropic: Structured prompts with XML tags for better parsing
    - Python: Robust error handling and type safety

    Args:
        role: Job title/role to search for (e.g., "Data Scientist")
        location: Location to search in (e.g., "Los Angeles")
        num_results: Number of job listings to return (1-50)

    Returns:
        Formatted string containing job listings or error message

    Example:
        >>> result = search_jobs(role="Data Scientist", location="Los Angeles", num_results=5)
        >>> print(result)
        <job>
            <title>Senior Data Scientist</title>
            ...
        </job>
    """

    # -------------------------------------------------------------------------
    # Step 1: Validate input parameters
    # -------------------------------------------------------------------------

    # Build input data dict for validation
    input_data = {
        'role': role,
        'location': location,
        'num_results': num_results
    }

    # Validate input parameters
    is_valid, error_message = _validate_search_input(input_data)
    if not is_valid:
        return f"""
❌ ERROR: Invalid input parameters.

{error_message}

Please provide valid parameters:
- role: Job title (non-empty string)
- location: Search location (non-empty string)
- num_results: Number of results (1-50)
"""

    # -------------------------------------------------------------------------
    # Step 2: Check API credentials
    # -------------------------------------------------------------------------

    if not ADZUNA_APP_ID or not ADZUNA_API_KEY:
        return """
❌ ERROR: Adzuna API credentials not configured.

Please set the following environment variables:
- ADZUNA_APP_ID
- ADZUNA_API_KEY

See the .env.example file for details.
"""

    # -------------------------------------------------------------------------
    # Step 3: Build API request URL
    # -------------------------------------------------------------------------

    # Adzuna API documentation: https://developer.adzuna.com/docs/search
    url = (
        f"{ADZUNA_BASE_URL}/{ADZUNA_COUNTRY}/search/1"
        f"?app_id={ADZUNA_APP_ID}"
        f"&app_key={ADZUNA_API_KEY}"
        f"&results_per_page={num_results}"
        f"&what={role}"
        f"&where={location}"
        f"&content-type=application/json"
    )

    print(f"\n🔍 Searching for {num_results} '{role}' jobs in {location}...")

    # -------------------------------------------------------------------------
    # Step 4: Make API request with retry logic
    # -------------------------------------------------------------------------

    jobs_data = _make_api_request_with_retry(url)

    if jobs_data is None:
        return """
❌ ERROR: Failed to fetch job listings from Adzuna API.

Possible causes:
- Network connection issues
- API service temporarily unavailable
- Rate limit exceeded

Please try again in a few moments.
"""

    # -------------------------------------------------------------------------
    # Step 5: Parse and format results
    # -------------------------------------------------------------------------

    results = jobs_data.get('results', [])

    if not results or len(results) == 0:
        return f"""
ℹ️  No job listings found for '{role}' in {location}.

Suggestions:
- Try a broader search term (e.g., "Data" instead of "Senior Data Scientist")
- Try a different location
- Try searching for related roles
"""

    # Format each job listing
    formatted_jobs = []
    for i, job in enumerate(results, 1):
        formatted_job = _format_job_listing(job)
        formatted_jobs.append(f"[Job {i}/{len(results)}]\n{formatted_job}")

    # Combine all jobs with metadata
    total_count = jobs_data.get('count', len(results))
    output = f"""
✅ Successfully found {len(results)} job listings (out of {total_count} total matches)

Search Parameters:
- Role: {role}
- Location: {location}

Job Listings:
{"=" * 80}

{"=" * 80}

""".join(formatted_jobs)

    print(f"✅ Found {len(results)} job listings!")

    return output


# =============================================================================
# ADDITIONAL TOOLS (For future expansion)
# =============================================================================

# Students can add more tools here, such as:
# - Resume parser tool
# - LinkedIn profile scraper tool
# - Salary comparison tool
# - Company research tool

# Example template for a new tool:
#
# @tool("Tool Name")
# def my_custom_tool(input_param: str) -> str:
#     """
#     Tool description here.
#
#     Args:
#         input_param: Description
#
#     Returns:
#         Description of return value
#     """
#     # Implementation here
#     pass


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    "search_jobs",
]
