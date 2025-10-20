"""
Task definitions for the Job Search AI Agent System.

This module defines all tasks that agents will perform. In CrewAI, tasks
represent specific pieces of work with clear descriptions, expected outputs,
and assigned agents.

Think of tasks as work orders that tell agents:
- What to do (description)
- What the result should look like (expected_output)
- Which other tasks to consider (context)
- Where to save the results (output_file)

Author: Claude Builder Club @ UC Irvine
Workshop: Intro to AI Agents (October 20, 2025)

Best Practices Applied:
- Anthropic: Clear, specific task descriptions with step-by-step instructions
- Anthropic: Expected output format specified for consistent results
- CrewAI: Task chaining through context parameter
- CrewAI: File output for persistence and review
"""

from datetime import datetime
from pathlib import Path
from crewai import Task
from crewai.tasks.task_output import TaskOutput

from src.config import OUTPUT_DIR


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_timestamp() -> str:
    """Get current timestamp in a readable format."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def create_task_callback(task_name: str):
    """
    Create a callback function for saving task output.

    Following best practice: Callbacks allow us to save intermediate results
    from each agent, which is useful for debugging and review.

    Args:
        task_name: Name of the task (used in filename)

    Returns:
        Callback function that saves task output to file
    """
    def callback(output: TaskOutput) -> None:
        """Save task output to a file."""
        timestamp = get_timestamp()
        filename = f"{task_name}_{timestamp}.txt"
        filepath = OUTPUT_DIR / filename

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"Task: {task_name}\n")
            f.write(f"Timestamp: {timestamp}\n")
            f.write("=" * 80 + "\n\n")
            f.write(output.raw)
            f.write("\n\n" + "=" * 80 + "\n")

        print(f"💾 Saved {task_name} output to: {filepath.name}")

    return callback


# =============================================================================
# TASK 1: JOB SEARCH
# =============================================================================

def create_job_search_task(agent, role: str, location: str, num_results: int) -> Task:
    """
    Create the job search task.

    This is the first task in the pipeline. The Job Searcher agent will use
    the Adzuna API to find relevant job listings based on the search criteria.

    Following best practices:
    - Anthropic: Clear, explicit instructions with input format specified
    - Anthropic: Expected output structure defined
    - CrewAI: Tool usage instructions for the agent

    Args:
        agent: The Job Searcher agent
        role: Job role to search for
        location: Location to search in
        num_results: Number of results to retrieve

    Returns:
        Task configured for job searching
    """

    # Following Anthropic best practice: Use clear, specific task descriptions
    description = f"""
Search for current job openings for the "{role}" role in {location}.

<instructions>
1. Use the Job Search Tool to find {num_results} job listings
2. The tool requires JSON input with this exact format:
   {{
       "role": "{role}",
       "location": "{location}",
       "num_results": {num_results}
   }}
3. Review the search results to ensure they are relevant and high-quality
4. If the search returns no results or low-quality results, try adjusting the search terms
5. Provide a summary of the key insights from the job listings found
</instructions>

<focus_areas>
- Emphasize the key skills and qualifications mentioned across multiple listings
- Note any common requirements or patterns
- Identify the experience levels required
- Observe salary ranges if available
</focus_areas>

Remember: These job listings will be analyzed by other agents to provide skills advice,
interview preparation, and career guidance. Ensure the listings you retrieve have
detailed, informative descriptions.
"""

    # Following Anthropic best practice: Specify expected output format
    expected_output = f"""
A comprehensive report containing:

1. Search Summary
   - Number of jobs found
   - Search parameters used
   - Overall market observations

2. Detailed Job Listings ({num_results} jobs)
   For each job:
   - Title and company
   - Location
   - Salary range (if available)
   - Key required skills
   - Job description highlights
   - Application URL

3. Market Insights
   - Common skills across listings
   - Experience level patterns
   - Salary trends
   - Notable companies hiring

Format the output clearly with sections and bullet points for easy reading.
"""

    return Task(
        description=description,
        expected_output=expected_output,
        agent=agent,
        callback=create_task_callback("job_search"),
    )


# =============================================================================
# TASK 2: SKILLS ANALYSIS
# =============================================================================

def create_skills_analysis_task(agent, job_search_task: Task, role: str) -> Task:
    """
    Create the skills analysis task.

    This task analyzes the job listings from Task 1 and provides actionable
    advice on skill development. It builds on the context from the job search.

    Following best practices:
    - Anthropic: Step-by-step instructions for systematic analysis
    - Anthropic: Structured output with categories
    - CrewAI: Context parameter links this task to the job search task

    Args:
        agent: The Skills Advisor agent
        job_search_task: The job search task (for context)
        role: Job role being analyzed

    Returns:
        Task configured for skills analysis
    """

    # Following Anthropic best practice: Chain-of-thought reasoning prompt
    description = f"""
Based on the job listings found for "{role}" positions, conduct a comprehensive
skills analysis and create a personalized learning roadmap.

<instructions>
Step 1: Extract ALL Skills
- Review each job listing carefully
- Extract technical skills (programming languages, frameworks, tools)
- Extract soft skills (communication, leadership, teamwork)
- Extract domain knowledge requirements
- Note certifications or education requirements

Step 2: Categorize and Prioritize
- Group skills by category (technical, tools, soft skills, domain knowledge)
- Identify skills mentioned in multiple listings (these are high priority)
- Separate "required" skills from "nice to have" skills
- Note the relative importance of each skill

Step 3: Create Learning Roadmap
For each high-priority skill:
- Assess typical learning time (beginner, intermediate, advanced)
- Recommend specific learning resources:
  * Online courses (Coursera, Udemy, DataCamp, etc.)
  * Books and tutorials
  * Hands-on projects
  * Certifications
- Suggest a learning sequence (what to learn first, second, etc.)
- Provide realistic timelines

Step 4: Actionable Next Steps
- Prioritize top 5 skills to focus on immediately
- Suggest quick wins (skills that can be learned quickly)
- Recommend longer-term investments (skills requiring more time)
</instructions>

<analysis_framework>
For each skill category, provide:
1. Skill name
2. Frequency (how many jobs mentioned it)
3. Priority level (Critical / Important / Nice-to-have)
4. Current market demand
5. Recommended learning resources (be specific!)
6. Estimated learning time
7. Practical projects to demonstrate competency
</analysis_framework>

Make your recommendations specific, actionable, and encouraging. Help the candidate
see a clear path forward.
"""

    expected_output = f"""
A comprehensive skills development roadmap containing:

1. Skills Overview
   - Total unique skills identified across all listings
   - Breakdown by category (technical, tools, soft skills, domain)

2. Priority Skills Matrix
   For each priority skill:
   - Skill name and category
   - Frequency in job listings (X out of Y jobs)
   - Priority level (Critical/Important/Nice-to-have)
   - Why this skill matters for {role} roles

3. Learning Roadmap
   For each high-priority skill:
   - Specific courses or learning resources (with links when possible)
   - Recommended books or tutorials
   - Hands-on projects to build competency
   - Certifications to pursue
   - Realistic timeline (e.g., "2-3 months of dedicated study")

4. Quick Start Plan (Next 30 Days)
   - Top 3 skills to focus on immediately
   - Specific first steps for each
   - Resources to get started today

5. Long-term Development Plan (3-6 Months)
   - Skill progression sequence
   - Milestones to track progress
   - Portfolio projects to demonstrate skills

Format with clear sections, bullet points, and actionable advice.
"""

    return Task(
        description=description,
        expected_output=expected_output,
        agent=agent,
        context=[job_search_task],  # This task builds on job search results
        callback=create_task_callback("skills_analysis"),
    )


# =============================================================================
# TASK 3: INTERVIEW PREPARATION
# =============================================================================

def create_interview_prep_task(agent, job_search_task: Task, role: str) -> Task:
    """
    Create the interview preparation task.

    This task generates interview questions and preparation strategies based
    on the specific job listings found.

    Following best practices:
    - Anthropic: Few-shot prompting with question format examples
    - Anthropic: Structured output with XML-style tags
    - CrewAI: Context from job search for tailored preparation

    Args:
        agent: The Interview Coach agent
        job_search_task: The job search task (for context)
        role: Job role being prepared for

    Returns:
        Task configured for interview preparation
    """

    description = f"""
Prepare comprehensive interview preparation materials for "{role}" positions
based on the job listings found.

<instructions>
For each job listing:

1. Generate Interview Questions (8-10 questions per role)
   - Technical questions based on required skills
   - Behavioral questions (teamwork, leadership, conflict resolution)
   - Situational questions (problem-solving scenarios)
   - Role-specific questions (why this role, why this company)

2. Provide Answer Guidance
   For each question:
   - What the interviewer is evaluating
   - How to structure your answer (frameworks like STAR)
   - Key points to mention
   - Example talking points
   - Common pitfalls to avoid

3. Company Research Tips
   - What to research about each company
   - How to demonstrate culture fit
   - Intelligent questions to ask the interviewer

4. General Interview Strategy
   - Opening and closing statements
   - How to discuss experience and projects
   - Salary negotiation preparation
</instructions>

<question_format_example>
Following best practice, structure each question like this:

<question>
  <type>Technical / Behavioral / Situational / Role-specific</type>
  <text>The actual interview question</text>
  <guidance>
    <evaluating>What skill or quality they're assessing</evaluating>
    <structure>How to organize your answer (e.g., STAR method)</structure>
    <key_points>
      - Critical point 1 to mention
      - Critical point 2 to mention
    </key_points>
    <example>Sample talking points or answer framework</example>
    <avoid>Common mistakes or pitfalls</avoid>
  </guidance>
</question>
</question_format_example>

Make this practical and confidence-building. Candidates should feel prepared
and ready to showcase their best selves.
"""

    expected_output = f"""
A comprehensive interview preparation guide containing:

1. Interview Overview
   - Number of roles being prepared for
   - Common interview formats to expect
   - General preparation timeline

2. Role-Specific Interview Questions
   For each job listing:

   A. Job Details Recap
      - Company and role title
      - Key requirements to address

   B. Technical Questions (3-4 questions)
      - Question text
      - What they're evaluating
      - Answer structure and key points
      - Example responses

   C. Behavioral Questions (2-3 questions)
      - Question text
      - STAR framework guidance
      - Example stories to prepare

   D. Situational Questions (2-3 questions)
      - Scenario description
      - How to approach the problem
      - What to emphasize in your answer

   E. Role/Company-Specific Questions (1-2 questions)
      - Why this company
      - Why this role
      - How to demonstrate fit

3. Company Research Guide
   For each company:
   - What to research (products, culture, recent news)
   - How to reference this in interviews
   - Intelligent questions to ask

4. General Interview Strategy
   - Opening statement framework
   - How to discuss technical projects
   - How to discuss soft skills and teamwork
   - Closing statement and follow-up approach
   - Salary discussion preparation

5. Practice Plan
   - Which questions to practice first
   - Mock interview suggestions
   - Resources for additional practice

Format with clear sections and actionable guidance for each question.
"""

    return Task(
        description=description,
        expected_output=expected_output,
        agent=agent,
        context=[job_search_task],
        callback=create_task_callback("interview_prep"),
    )


# =============================================================================
# TASK 4: CAREER ADVISORY
# =============================================================================

def create_career_advisory_task(agent, job_search_task: Task, role: str) -> Task:
    """
    Create the career advisory task.

    This task provides strategic advice on resumes, LinkedIn profiles,
    networking, and application strategies tailored to the specific job listings.

    Following best practices:
    - Anthropic: Structured recommendations by category
    - Anthropic: Specific, actionable advice with examples
    - CrewAI: Holistic view considering all aspects of job search

    Args:
        agent: The Career Advisor agent
        job_search_task: The job search task (for context)
        role: Job role being applied for

    Returns:
        Task configured for career advisory
    """

    description = f"""
Provide strategic career advice for successfully applying to "{role}" positions
based on the job listings found.

<instructions>
1. Resume Optimization
   - Identify critical keywords from ALL job descriptions
   - Recommend resume structure and sections
   - Suggest how to frame experience using achievement-focused bullets
   - Provide examples of strong bullet points for this role
   - Advise on ATS (Applicant Tracking System) optimization

2. LinkedIn Profile Optimization
   - Headline recommendations (keywords for recruiter searches)
   - About section talking points
   - Experience descriptions (integrate keywords naturally)
   - Skills to highlight and endorse
   - Recommendation strategy

3. Networking Strategy
   For each company/role:
   - How to find employee connections
   - LinkedIn outreach message templates
   - Networking groups or events to attend
   - Alumni networks to leverage

4. Application Strategy
   For each job listing:
   - Best application approach (referral, direct, recruiter)
   - Cover letter key talking points
   - When to apply (timing matters!)
   - Follow-up timeline and approach
   - How to demonstrate culture fit

5. Personal Branding
   - Professional story framework
   - Online presence optimization
   - Portfolio/GitHub recommendations
   - Thought leadership opportunities
</instructions>

<recommendation_format>
Structure recommendations clearly:

<recommendation category="Resume | LinkedIn | Networking | Application | Branding">
  <priority>High | Medium | Low</priority>
  <action>Specific action to take</action>
  <rationale>Why this matters for these roles</rationale>
  <example>Concrete example or template</example>
  <timeline>When to do this</timeline>
</recommendation>
</recommendation_format>

Provide practical, immediately actionable advice that will make a real difference
in the candidate's job search success.
"""

    expected_output = f"""
A comprehensive career strategy guide containing:

1. Executive Summary
   - Overview of the {role} job market
   - Key differentiators to emphasize
   - Overall application strategy

2. Resume Optimization Strategy

   A. Keywords to Integrate
      - List of critical keywords from job descriptions
      - Where to place them naturally

   B. Resume Structure Recommendations
      - Sections to include/emphasize
      - Order of sections
      - Length and format guidance

   C. Experience Bullet Points
      - Framework for achievement-focused bullets
      - 5-10 example bullets tailored to {role}
      - Quantification strategies

   D. ATS Optimization Tips
      - Formatting dos and don'ts
      - Keyword density recommendations
      - File format advice

3. LinkedIn Profile Optimization

   A. Headline
      - 3-5 headline options with keywords

   B. About Section
      - Professional story framework
      - Key phrases to include
      - Call-to-action suggestions

   C. Experience Descriptions
      - How to repurpose resume bullets
      - Keyword integration strategies

   D. Skills & Endorsements
      - Top 10 skills to list
      - How to get endorsements

   E. Recommendations Strategy
      - Who to ask
      - What to ask for

4. Networking Strategy

   For each company:
   - Employee connection strategy
   - Outreach message templates
   - Information interview approach

   General networking:
   - Groups to join (LinkedIn, Slack, Discord)
   - Events to attend
   - Online communities to engage with

5. Application Strategy

   For each job listing:
   - Recommended application approach
   - Cover letter key points (3-5 points)
   - Best time to apply
   - Follow-up timeline (when to follow up)

   General application tips:
   - Application tracker recommendations
   - Follow-up email templates
   - How to handle rejections

6. Personal Branding
   - Professional story to tell
   - Portfolio/project recommendations
   - Content to share on LinkedIn
   - Thought leadership opportunities

7. Action Plan (Next 7 Days)
   - Day-by-day checklist
   - Prioritized tasks
   - Quick wins to start immediately

Format with clear sections, specific examples, and actionable checklists.
"""

    return Task(
        description=description,
        expected_output=expected_output,
        agent=agent,
        context=[job_search_task],
        callback=create_task_callback("career_advisory"),
    )


# =============================================================================
# TASK FACTORY FUNCTION
# =============================================================================

def create_all_tasks(
    agents: dict,
    role: str,
    location: str,
    num_results: int
) -> list[Task]:
    """
    Create all tasks for the job search system in the correct order.

    This factory function creates all tasks with proper dependencies
    (context) and returns them in execution order.

    Following best practice: Centralized task creation ensures consistency
    and makes it easy to modify the workflow.

    Args:
        agents: Dictionary of agent instances from create_all_agents()
        role: Job role to search for
        location: Location to search in
        num_results: Number of job results to retrieve

    Returns:
        List of Task instances in execution order
    """

    # Create job search task first (no dependencies)
    job_search_task = create_job_search_task(
        agent=agents['job_searcher'],
        role=role,
        location=location,
        num_results=num_results
    )

    # Create dependent tasks (they all depend on job search)
    skills_task = create_skills_analysis_task(
        agent=agents['skills_advisor'],
        job_search_task=job_search_task,
        role=role
    )

    interview_task = create_interview_prep_task(
        agent=agents['interview_coach'],
        job_search_task=job_search_task,
        role=role
    )

    career_task = create_career_advisory_task(
        agent=agents['career_advisor'],
        job_search_task=job_search_task,
        role=role
    )

    # Return in execution order
    return [
        job_search_task,
        skills_task,
        interview_task,
        career_task,
    ]


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    'create_job_search_task',
    'create_skills_analysis_task',
    'create_interview_prep_task',
    'create_career_advisory_task',
    'create_all_tasks',
]
