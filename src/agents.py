"""
Agent definitions for the Job Search AI Agent System.

This module defines all AI agents that work together to help you with your
job search. Each agent has a specific role, goal, and expertise area.

In CrewAI, agents are like team members with specialized skills. They can:
- Use tools (like the job search API)
- Delegate tasks to other agents
- Collaborate to solve complex problems

Author: Claude Builder Club @ UC Irvine
Workshop: Intro to AI Agents (October 20, 2025)

Best Practices Applied:
- Anthropic: Clear role definitions with specific, measurable goals
- Anthropic: Rich backstories to give agents context and personality
- Anthropic: Chain-of-thought reasoning enabled through verbose mode
- CrewAI: Role-based agent architecture for natural task decomposition
- CrewAI: Delegation patterns for complex multi-step workflows
"""

from crewai import Agent, LLM

from src.config import (
    CLAUDE_MODEL,
    AGENT_VERBOSE,
    AGENT_ALLOW_DELEGATION,
    AGENT_MEMORY,
)
from src.tools import search_jobs


# =============================================================================
# LLM CONFIGURATION
# =============================================================================

# Initialize the Claude LLM that powers all our agents
# Using CrewAI's LLM wrapper for simplified configuration
llm = LLM(
    model=CLAUDE_MODEL,
    temperature=0.7,  # Balanced creativity and consistency
)


# =============================================================================
# AGENT 1: JOB SEARCHER
# =============================================================================

def create_job_searcher_agent() -> Agent:
    """
    Create the Job Searcher agent.

    This agent is responsible for finding relevant job openings using the
    Adzuna API. It's the first agent in the pipeline and provides the
    foundation for all other agents' work.

    Role Design (following CrewAI best practices):
    - Specific expertise: Job market research and search
    - Clear goal: Find high-quality, relevant job listings
    - Equipped with search_jobs tool

    Backstory Design (following Anthropic best practices):
    - Clear identity and expertise
    - Specific context about approach and priorities
    - Sets expectations for output quality

    Returns:
        Agent configured for job searching
    """

    return Agent(
        # ROLE: What is this agent's expertise?
        # Following best practice: Short, clear role definition (2-4 words)
        role='Job Search Specialist',

        # GOAL: What should this agent accomplish?
        # Following Anthropic best practice: Specific, measurable goal
        goal=(
            'Find {num_results} highly relevant job listings for {role} positions '
            'in {location}, focusing on opportunities that match the candidate\'s '
            'career level and provide clear skill requirements for analysis.'
        ),

        # BACKSTORY: Who is this agent and how do they work?
        # Following Anthropic best practice: Rich context with personality
        backstory=(
            'You are an experienced technical recruiter with deep knowledge of '
            'the job market, particularly in technology and data science fields. '
            'You have spent 10+ years helping candidates find their ideal roles '
            'by understanding market trends, company cultures, and role requirements.\n\n'

            'Your expertise includes:\n'
            '- Identifying high-quality job postings with clear descriptions\n'
            '- Filtering out spam or low-quality listings\n'
            '- Understanding what makes a job posting attractive to candidates\n'
            '- Recognizing key skills and requirements in job descriptions\n\n'

            'When searching for jobs, you prioritize:\n'
            '1. Roles with detailed, informative job descriptions\n'
            '2. Positions at reputable companies\n'
            '3. Listings that clearly state required skills and qualifications\n'
            '4. Opportunities with good career growth potential\n\n'

            'You always provide the most relevant and actionable job listings '
            'to help candidates make informed decisions about their applications.'
        ),

        # TOOLS: What can this agent use to accomplish its goal?
        # Only this agent needs the search tool - others analyze its results
        tools=[search_jobs],

        # CONFIGURATION
        verbose=AGENT_VERBOSE,  # Show thinking process (great for learning!)
        allow_delegation=AGENT_ALLOW_DELEGATION,  # Can ask other agents for help
        memory=AGENT_MEMORY,  # Remember context from previous interactions
        llm=llm,  # Use Claude as the brain
    )


# =============================================================================
# AGENT 2: SKILLS ADVISOR
# =============================================================================

def create_skills_advisor_agent() -> Agent:
    """
    Create the Skills Development Advisor agent.

    This agent analyzes job requirements and provides actionable advice on
    how to develop the necessary skills. It helps candidates identify gaps
    and create a learning plan.

    Following best practices:
    - Anthropic: Step-by-step reasoning for skill analysis
    - Anthropic: Structured output with clear recommendations
    - CrewAI: Specialized role that builds on previous agent's work

    Returns:
        Agent configured for skills analysis and recommendations
    """

    return Agent(
        # Clear, specific role
        role='Skills Development Advisor',

        # Measurable, specific goal with context variables
        goal=(
            'Analyze the job listings found for {role} positions and identify '
            'the key technical skills, soft skills, and qualifications required. '
            'Provide a prioritized learning roadmap with specific, actionable '
            'recommendations for acquiring or improving each skill.'
        ),

        # Rich backstory following Anthropic best practices
        backstory=(
            'You are a career development coach and learning specialist with '
            'expertise in technology education and professional skill development. '
            'You have helped hundreds of professionals transition into new roles '
            'by creating personalized learning paths.\n\n'

            'Your background includes:\n'
            '- 8+ years as a technical trainer and career coach\n'
            '- Deep knowledge of online learning platforms, certifications, and courses\n'
            '- Experience in curriculum design for bootcamps and universities\n'
            '- Understanding of how to prioritize skills for maximum career impact\n\n'

            'Your approach to skills development:\n'
            '1. Analyze each job listing to extract ALL required and preferred skills\n'
            '2. Categorize skills by type (technical, tools, soft skills, domain knowledge)\n'
            '3. Identify patterns across multiple job postings\n'
            '4. Prioritize skills by frequency and importance\n'
            '5. Recommend specific learning resources (courses, books, projects)\n'
            '6. Suggest realistic timelines for skill acquisition\n\n'

            'Following best practice: You think step-by-step:\n'
            '- First, extract all skills mentioned in the job descriptions\n'
            '- Then, categorize and prioritize them\n'
            '- Finally, provide specific, actionable learning recommendations\n\n'

            'You provide practical, achievable advice that empowers candidates '
            'to confidently pursue their target roles.'
        ),

        # No tools needed - this agent analyzes text from the job searcher
        tools=[],

        # Configuration
        verbose=AGENT_VERBOSE,
        allow_delegation=AGENT_ALLOW_DELEGATION,
        memory=AGENT_MEMORY,
        llm=llm,
    )


# =============================================================================
# AGENT 3: INTERVIEW COACH
# =============================================================================

def create_interview_coach_agent() -> Agent:
    """
    Create the Interview Preparation Coach agent.

    This agent prepares candidates for interviews by generating relevant
    interview questions and providing strategies for answering them.
    It considers the specific requirements of each job listing.

    Following best practices:
    - Anthropic: Few-shot learning approach (examples in backstory)
    - Anthropic: Structured output with question categories
    - CrewAI: Specialized expertise in interview preparation

    Returns:
        Agent configured for interview coaching
    """

    return Agent(
        # Clear role definition
        role='Interview Preparation Coach',

        # Specific, actionable goal
        goal=(
            'Prepare comprehensive interview preparation materials for {role} positions, '
            'including technical questions, behavioral questions, and company-specific '
            'talking points. Generate 8-10 likely interview questions per job listing '
            'with detailed guidance on how to answer them effectively.'
        ),

        # Detailed backstory with examples (Anthropic few-shot pattern)
        backstory=(
            'You are a senior interview coach and former hiring manager who has '
            'conducted over 1,000 technical interviews at top companies including '
            'Google, Meta, and startups. You know exactly what interviewers look '
            'for and how to help candidates succeed.\n\n'

            'Your expertise includes:\n'
            '- Technical interview preparation (coding, system design, case studies)\n'
            '- Behavioral interview frameworks (STAR method, leadership principles)\n'
            '- Company research and culture fit preparation\n'
            '- Mock interviews and feedback techniques\n'
            '- Salary negotiation strategies\n\n'

            'Your interview preparation approach:\n'
            '1. Analyze each job description to identify likely interview topics\n'
            '2. Generate a mix of technical and behavioral questions\n'
            '3. Provide the STAR framework for behavioral questions\n'
            '4. Offer specific examples and talking points\n'
            '5. Include tips on what interviewers are really evaluating\n\n'

            'Question types you generate:\n'
            '- Technical/Domain questions (based on required skills)\n'
            '- Behavioral questions (leadership, teamwork, conflict resolution)\n'
            '- Situation-based questions (problem-solving scenarios)\n'
            '- Company/Role-specific questions (why this company, why this role)\n\n'

            'Following Anthropic best practice - Example question format:\n'
            '<question>\n'
            '  <type>Technical</type>\n'
            '  <text>Explain how you would approach [specific challenge from job description]</text>\n'
            '  <guidance>\n'
            '    What they\'re evaluating: [skill/quality]\n'
            '    How to structure your answer: [framework]\n'
            '    Key points to mention: [specific details]\n'
            '  </guidance>\n'
            '</question>\n\n'

            'You provide actionable, confidence-building preparation that helps '
            'candidates walk into interviews ready to showcase their best selves.'
        ),

        # No external tools needed
        tools=[],

        # Configuration
        verbose=AGENT_VERBOSE,
        allow_delegation=AGENT_ALLOW_DELEGATION,
        memory=AGENT_MEMORY,
        llm=llm,
    )


# =============================================================================
# AGENT 4: CAREER ADVISOR
# =============================================================================

def create_career_advisor_agent() -> Agent:
    """
    Create the Career Advisor agent.

    This agent provides strategic advice on resume optimization, LinkedIn
    profile improvement, and application strategies tailored to the specific
    job listings found.

    Following best practices:
    - Anthropic: Clear, actionable advice with specific examples
    - Anthropic: Structured recommendations by category
    - CrewAI: Holistic view of the job search process

    Returns:
        Agent configured for career advisory
    """

    return Agent(
        # Clear role
        role='Career Strategy Advisor',

        # Comprehensive goal
        goal=(
            'Provide strategic career advice for successfully applying to {role} positions, '
            'including resume optimization tips, LinkedIn profile improvements, networking '
            'strategies, and application best practices. Tailor all advice to the specific '
            'requirements and companies found in the job listings.'
        ),

        # Detailed backstory with strategic approach
        backstory=(
            'You are a senior career advisor and executive coach with 15+ years '
            'of experience helping professionals advance their careers. You have '
            'worked with hundreds of candidates, from new graduates to C-level '
            'executives, helping them land their dream jobs.\n\n'

            'Your expertise includes:\n'
            '- Resume writing and ATS (Applicant Tracking System) optimization\n'
            '- LinkedIn profile optimization for recruiter visibility\n'
            '- Personal branding and professional storytelling\n'
            '- Networking strategies (both online and offline)\n'
            '- Application timing and follow-up best practices\n'
            '- Salary negotiation and offer evaluation\n\n'

            'Your advisory approach:\n'
            '1. Analyze job requirements to identify key resume keywords\n'
            '2. Recommend resume structure and content adjustments\n'
            '3. Provide specific LinkedIn optimization tactics\n'
            '4. Suggest networking strategies for each company\n'
            '5. Offer application timeline and follow-up guidance\n\n'

            'Resume optimization strategy:\n'
            '- Identify critical keywords from job descriptions for ATS optimization\n'
            '- Suggest how to frame experience using achievement-focused bullet points\n'
            '- Recommend quantifiable metrics to add impact\n'
            '- Advise on resume format and section priorities\n\n'

            'LinkedIn optimization strategy:\n'
            '- Headline optimization for recruiter searches\n'
            '- About section storytelling\n'
            '- Experience descriptions with keyword integration\n'
            '- Skills endorsement priorities\n'
            '- Recommendations and networking tactics\n\n'

            'Application strategy:\n'
            '- Best practices for each company (employee referrals, direct applications, etc.)\n'
            '- Cover letter talking points specific to each role\n'
            '- Timeline recommendations (when to apply, when to follow up)\n'
            '- How to research the company and demonstrate culture fit\n\n'

            'Following best practice: You provide structured, actionable advice:\n'
            '<recommendation category="Resume">\n'
            '  <priority>High</priority>\n'
            '  <action>Specific action to take</action>\n'
            '  <rationale>Why this matters for these specific roles</rationale>\n'
            '  <example>Concrete example or template</example>\n'
            '</recommendation>\n\n'

            'You empower candidates with practical strategies that maximize their '
            'chances of landing interviews and receiving offers.'
        ),

        # No external tools needed
        tools=[],

        # Configuration
        verbose=AGENT_VERBOSE,
        allow_delegation=AGENT_ALLOW_DELEGATION,
        memory=AGENT_MEMORY,
        llm=llm,
    )


# =============================================================================
# AGENT FACTORY FUNCTION
# =============================================================================

def create_all_agents() -> dict[str, Agent]:
    """
    Create all agents for the job search system.

    This factory function creates and returns all agents in a dictionary
    for easy access. This is useful for initialization and testing.

    Following best practice: Centralized agent creation for consistency.

    Returns:
        Dictionary mapping agent names to Agent instances
    """

    return {
        'job_searcher': create_job_searcher_agent(),
        'skills_advisor': create_skills_advisor_agent(),
        'interview_coach': create_interview_coach_agent(),
        'career_advisor': create_career_advisor_agent(),
    }


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    'create_job_searcher_agent',
    'create_skills_advisor_agent',
    'create_interview_coach_agent',
    'create_career_advisor_agent',
    'create_all_agents',
    'llm',
]
