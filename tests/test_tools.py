"""
Tests for the Job Search tools.

This file contains basic tests for the Adzuna API integration.
Students can run these tests to verify their setup is working.

Usage:
    pytest tests/test_tools.py
    or
    uv run pytest tests/test_tools.py

Author: Claude Builder Club @ UC Irvine
Workshop: Intro to AI Agents (October 20, 2025)
"""

import json
import pytest
from unittest.mock import patch, MagicMock

from src.tools import search_jobs, _validate_search_input, _format_job_listing


# =============================================================================
# TEST INPUT VALIDATION
# =============================================================================

def test_validate_search_input_valid():
    """Test that valid input passes validation."""
    input_data = {
        "role": "Data Scientist",
        "location": "Los Angeles",
        "num_results": 5
    }
    is_valid, error_message = _validate_search_input(input_data)
    assert is_valid is True
    assert error_message == ""


def test_validate_search_input_missing_field():
    """Test that missing required fields are caught."""
    input_data = {
        "role": "Data Scientist",
        "location": "Los Angeles"
        # missing num_results
    }
    is_valid, error_message = _validate_search_input(input_data)
    assert is_valid is False
    assert "num_results" in error_message


def test_validate_search_input_empty_role():
    """Test that empty role string is caught."""
    input_data = {
        "role": "",
        "location": "Los Angeles",
        "num_results": 5
    }
    is_valid, error_message = _validate_search_input(input_data)
    assert is_valid is False
    assert "role" in error_message.lower()


def test_validate_search_input_invalid_num_results():
    """Test that invalid num_results are caught."""
    # Test too low
    input_data = {
        "role": "Data Scientist",
        "location": "Los Angeles",
        "num_results": 0
    }
    is_valid, error_message = _validate_search_input(input_data)
    assert is_valid is False
    assert "num_results" in error_message

    # Test too high
    input_data["num_results"] = 100
    is_valid, error_message = _validate_search_input(input_data)
    assert is_valid is False
    assert "num_results" in error_message


# =============================================================================
# TEST JOB FORMATTING
# =============================================================================

def test_format_job_listing():
    """Test that job listings are formatted correctly."""
    job_data = {
        "title": "Senior Data Scientist",
        "company": {"display_name": "Tech Corp"},
        "location": {"display_name": "San Francisco, CA"},
        "description": "Great opportunity for a data scientist...",
        "salary_min": 120000,
        "salary_max": 180000,
        "redirect_url": "https://example.com/job/123",
        "created": "2025-10-15"
    }

    formatted = _format_job_listing(job_data)

    # Check that key information is in the output
    assert "Senior Data Scientist" in formatted
    assert "Tech Corp" in formatted
    assert "San Francisco, CA" in formatted
    assert "$120,000 - $180,000" in formatted
    assert "https://example.com/job/123" in formatted

    # Check XML-style structure
    assert "<job>" in formatted
    assert "<title>" in formatted
    assert "</job>" in formatted


def test_format_job_listing_missing_salary():
    """Test formatting when salary information is missing."""
    job_data = {
        "title": "Data Analyst",
        "company": {"display_name": "Startup Inc"},
        "location": {"display_name": "Remote"},
        "description": "Remote position...",
        "redirect_url": "https://example.com/job/456",
        "created": "2025-10-18"
    }

    formatted = _format_job_listing(job_data)

    assert "Data Analyst" in formatted
    assert "Not specified" in formatted  # Default salary text


# =============================================================================
# TEST SEARCH JOBS TOOL
# =============================================================================

def test_search_jobs_invalid_json():
    """Test that invalid JSON input is handled gracefully."""
    result = search_jobs("this is not json")
    assert "ERROR" in result
    assert "JSON" in result


def test_search_jobs_missing_parameters():
    """Test that missing parameters are caught."""
    input_json = json.dumps({
        "role": "Data Scientist",
        # missing location and num_results
    })
    result = search_jobs(input_json)
    assert "ERROR" in result
    assert "location" in result.lower()


@patch('src.tools.ADZUNA_APP_ID', None)
@patch('src.tools.ADZUNA_API_KEY', None)
def test_search_jobs_missing_credentials():
    """Test that missing API credentials are detected."""
    input_json = json.dumps({
        "role": "Data Scientist",
        "location": "Los Angeles",
        "num_results": 5
    })
    result = search_jobs(input_json)
    assert "ERROR" in result
    assert "credentials" in result.lower()


@patch('src.tools._make_api_request_with_retry')
@patch('src.tools.ADZUNA_APP_ID', 'test_id')
@patch('src.tools.ADZUNA_API_KEY', 'test_key')
def test_search_jobs_success(mock_api_request):
    """Test successful job search with mocked API response."""
    # Mock API response
    mock_api_request.return_value = {
        "count": 100,
        "results": [
            {
                "title": "Data Scientist",
                "company": {"display_name": "Tech Company"},
                "location": {"display_name": "Los Angeles, CA"},
                "description": "Looking for an experienced data scientist...",
                "salary_min": 100000,
                "salary_max": 150000,
                "redirect_url": "https://example.com/job/1",
                "created": "2025-10-15"
            },
            {
                "title": "Senior Data Scientist",
                "company": {"display_name": "Startup Inc"},
                "location": {"display_name": "Santa Monica, CA"},
                "description": "Lead our data science team...",
                "redirect_url": "https://example.com/job/2",
                "created": "2025-10-16"
            }
        ]
    }

    input_json = json.dumps({
        "role": "Data Scientist",
        "location": "Los Angeles",
        "num_results": 2
    })

    result = search_jobs(input_json)

    # Check success indicators
    assert "ERROR" not in result
    assert "Successfully found" in result
    assert "Data Scientist" in result
    assert "Tech Company" in result
    assert "Startup Inc" in result


@patch('src.tools._make_api_request_with_retry')
@patch('src.tools.ADZUNA_APP_ID', 'test_id')
@patch('src.tools.ADZUNA_API_KEY', 'test_key')
def test_search_jobs_no_results(mock_api_request):
    """Test handling of search with no results."""
    # Mock API response with no results
    mock_api_request.return_value = {
        "count": 0,
        "results": []
    }

    input_json = json.dumps({
        "role": "Extremely Rare Job Title",
        "location": "Middle of Nowhere",
        "num_results": 5
    })

    result = search_jobs(input_json)

    assert "No job listings found" in result
    assert "Suggestions" in result


@patch('src.tools._make_api_request_with_retry')
@patch('src.tools.ADZUNA_APP_ID', 'test_id')
@patch('src.tools.ADZUNA_API_KEY', 'test_key')
def test_search_jobs_api_failure(mock_api_request):
    """Test handling of API request failures."""
    # Mock API failure
    mock_api_request.return_value = None

    input_json = json.dumps({
        "role": "Data Scientist",
        "location": "Los Angeles",
        "num_results": 5
    })

    result = search_jobs(input_json)

    assert "ERROR" in result
    assert "Failed to fetch" in result


# =============================================================================
# INTEGRATION TEST (Optional - requires actual API keys)
# =============================================================================

@pytest.mark.integration
@pytest.mark.skipif(
    True,  # Set to False to run integration tests
    reason="Integration test requires actual API keys"
)
def test_search_jobs_integration():
    """
    Integration test with real API call.

    To run this test:
    1. Set your API keys in .env
    2. Change skipif to False above
    3. Run: pytest tests/test_tools.py -m integration
    """
    input_json = json.dumps({
        "role": "Data Scientist",
        "location": "Los Angeles",
        "num_results": 2
    })

    result = search_jobs(input_json)

    # Should get real results
    assert "ERROR" not in result
    assert "Successfully found" in result or "No job listings found" in result


# =============================================================================
# RUN TESTS
# =============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
