"""
Cover letter templates for different tones and industries.
"""

PROFESSIONAL_TEMPLATE = """
Dear Hiring Manager,

I am writing to express my strong interest in the {job_title} position at {company_name}. With my background in {relevant_experience}, I am confident that I would be a valuable addition to your team.

{experience_paragraph}

{skills_paragraph}

{company_interest_paragraph}

I would welcome the opportunity to discuss how my experience and enthusiasm can contribute to {company_name}'s continued success. Thank you for considering my application. I look forward to hearing from you soon.

Sincerely,
{candidate_name}
"""

ENTHUSIASTIC_TEMPLATE = """
Dear {company_name} Team,

I am thrilled to apply for the {job_title} position! Your company's mission to {company_mission} deeply resonates with my passion for {relevant_field}, and I am excited about the possibility of contributing to your innovative work.

{experience_paragraph}

{skills_paragraph}

What particularly excites me about {company_name} is {specific_company_interest}. I am eager to bring my {key_strengths} to help drive your team's success and make a meaningful impact.

{closing_enthusiasm}

I can't wait to discuss how we can work together to achieve great things. Thank you for your time and consideration!

Best regards,
{candidate_name}
"""

CREATIVE_TEMPLATE = """
Hello {company_name} Innovators,

When I discovered the {job_title} opening at {company_name}, I knew I had found my next adventure. Your reputation for {company_strength} and commitment to {company_values} align perfectly with my professional journey and personal values.

{storytelling_paragraph}

{experience_paragraph}

{unique_value_proposition}

I believe that great work happens when passion meets opportunity, and I see this role as the perfect intersection of both. I'm excited about the possibility of joining your team and contributing to {company_name}'s continued innovation.

Let's create something amazing together!

Warm regards,
{candidate_name}
"""

TECHNICAL_TEMPLATE = """
Dear Technical Hiring Team,

I am excited to submit my application for the {job_title} position at {company_name}. As a {professional_title} with {years_experience} years of experience in {technical_domain}, I am well-positioned to contribute to your technical objectives.

Technical Expertise:
{technical_skills_list}

Professional Experience:
{technical_experience}

{project_highlights}

I am particularly drawn to {company_name} because of your work in {technical_area} and your commitment to {technical_values}. I am confident that my technical skills and problem-solving approach would be valuable assets to your engineering team.

I would appreciate the opportunity to discuss how my technical background aligns with your needs. Thank you for your consideration.

Best regards,
{candidate_name}
"""

EXECUTIVE_TEMPLATE = """
Dear Executive Leadership Team,

I am pleased to submit my candidacy for the {job_title} position at {company_name}. Throughout my {years_experience} years of leadership experience in {industry}, I have consistently delivered results that drive organizational growth and operational excellence.

Strategic Leadership:
{leadership_achievements}

Key Accomplishments:
{quantified_results}

Vision for {company_name}:
{strategic_vision}

I am excited about the opportunity to leverage my experience in {expertise_areas} to help {company_name} achieve its strategic objectives. I believe my track record of {key_achievements} positions me well to make an immediate impact.

I look forward to discussing how my leadership philosophy and proven results can contribute to your organization's continued success.

Respectfully,
{candidate_name}
"""

def get_template_by_tone(tone: str) -> str:
    """Get cover letter template by tone."""
    templates = {
        'professional': PROFESSIONAL_TEMPLATE,
        'enthusiastic': ENTHUSIASTIC_TEMPLATE,
        'creative': CREATIVE_TEMPLATE,
        'technical': TECHNICAL_TEMPLATE,
        'executive': EXECUTIVE_TEMPLATE
    }
    
    return templates.get(tone.lower(), PROFESSIONAL_TEMPLATE)

def get_template_variables() -> list:
    """Get list of template variables that need to be filled."""
    return [
        'job_title',
        'company_name', 
        'candidate_name',
        'relevant_experience',
        'experience_paragraph',
        'skills_paragraph',
        'company_interest_paragraph',
        'company_mission',
        'relevant_field',
        'specific_company_interest',
        'key_strengths',
        'closing_enthusiasm',
        'company_strength',
        'company_values',
        'storytelling_paragraph',
        'unique_value_proposition',
        'professional_title',
        'years_experience',
        'technical_domain',
        'technical_skills_list',
        'technical_experience',
        'project_highlights',
        'technical_area',
        'technical_values',
        'industry',
        'leadership_achievements',
        'quantified_results',
        'strategic_vision',
        'expertise_areas',
        'key_achievements'
    ]