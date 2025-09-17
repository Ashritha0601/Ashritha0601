import re
from typing import List, Dict, Any
from datetime import datetime, timedelta


def extract_skills_from_text(text: str) -> List[str]:
    """Extract potential skills from text using keyword matching."""
    
    # Common technical skills keywords
    technical_skills = [
        'python', 'java', 'javascript', 'typescript', 'go', 'rust', 'c++', 'c#',
        'sql', 'postgresql', 'mysql', 'mongodb', 'redis', 'elasticsearch',
        'kafka', 'spark', 'hadoop', 'airflow', 'kubernetes', 'docker',
        'aws', 'azure', 'gcp', 'terraform', 'ansible',
        'react', 'angular', 'vue', 'nodejs', 'express', 'django', 'flask', 'fastapi',
        'tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy',
        'git', 'jenkins', 'gitlab', 'github', 'ci/cd'
    ]
    
    found_skills = []
    text_lower = text.lower()
    
    for skill in technical_skills:
        if skill in text_lower:
            found_skills.append(skill.title())
    
    return list(set(found_skills))  # Remove duplicates


def calculate_text_similarity(text1: str, text2: str) -> float:
    """Calculate basic text similarity using word overlap."""
    
    words1 = set(re.findall(r'\w+', text1.lower()))
    words2 = set(re.findall(r'\w+', text2.lower()))
    
    if not words1 or not words2:
        return 0.0
    
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    
    return len(intersection) / len(union) if union else 0.0


def format_salary_range(min_salary: int, max_salary: int) -> str:
    """Format salary range for display."""
    return f"${min_salary:,} - ${max_salary:,}"


def extract_years_of_experience(text: str) -> int:
    """Extract years of experience from text."""
    
    # Look for patterns like "5 years", "3+ years", "2-4 years"
    patterns = [
        r'(\d+)\+?\s*years?\s*(?:of\s*)?experience',
        r'(\d+)\+?\s*years?\s*(?:in|with)',
        r'experience.*?(\d+)\+?\s*years?'
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text.lower())
        if matches:
            return int(matches[0])
    
    return 0


def clean_company_name(company_name: str) -> str:
    """Clean and standardize company name."""
    
    # Remove common suffixes
    suffixes = ['inc', 'llc', 'corp', 'corporation', 'ltd', 'limited', 'co']
    
    cleaned = company_name.strip()
    
    for suffix in suffixes:
        pattern = rf'\b{suffix}\.?\b'
        cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE)
    
    return cleaned.strip()


def generate_resume_filename(name: str, timestamp: datetime = None) -> str:
    """Generate a standardized resume filename."""
    
    if timestamp is None:
        timestamp = datetime.now()
    
    # Clean name for filename
    clean_name = re.sub(r'[^\w\s-]', '', name)
    clean_name = re.sub(r'\s+', '_', clean_name)
    
    date_str = timestamp.strftime('%Y%m%d')
    
    return f"{clean_name}_Resume_{date_str}.pdf"


def parse_job_location(location_str: str) -> Dict[str, str]:
    """Parse job location string into components."""
    
    # Handle common formats like "Dallas, TX", "Remote", "New York, NY (Remote)"
    
    result = {
        'city': '',
        'state': '',
        'country': 'US',
        'remote': False
    }
    
    location_str = location_str.strip()
    
    # Check for remote indicators
    if 'remote' in location_str.lower():
        result['remote'] = True
        location_str = re.sub(r'\(?remote\)?', '', location_str, flags=re.IGNORECASE).strip()
    
    # Parse city, state format
    if ',' in location_str:
        parts = [part.strip() for part in location_str.split(',')]
        if len(parts) >= 2:
            result['city'] = parts[0]
            result['state'] = parts[1]
    elif location_str and not result['remote']:
        result['city'] = location_str
    
    return result


def calculate_job_freshness_score(posted_date: datetime) -> float:
    """Calculate job freshness score (0-1, higher is fresher)."""
    
    if not posted_date:
        return 0.5  # Default score for unknown date
    
    days_old = (datetime.now() - posted_date).days
    
    if days_old <= 1:
        return 1.0
    elif days_old <= 7:
        return 0.8
    elif days_old <= 14:
        return 0.6
    elif days_old <= 30:
        return 0.4
    else:
        return 0.2


def extract_contact_info(text: str) -> Dict[str, str]:
    """Extract contact information from text."""
    
    contact_info = {
        'email': '',
        'phone': '',
        'linkedin': '',
        'github': ''
    }
    
    # Email pattern
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    email_match = re.search(email_pattern, text)
    if email_match:
        contact_info['email'] = email_match.group()
    
    # Phone pattern (US format)
    phone_pattern = r'\b(?:\+?1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})\b'
    phone_match = re.search(phone_pattern, text)
    if phone_match:
        contact_info['phone'] = phone_match.group()
    
    # LinkedIn pattern
    linkedin_pattern = r'linkedin\.com/in/([A-Za-z0-9-]+)'
    linkedin_match = re.search(linkedin_pattern, text)
    if linkedin_match:
        contact_info['linkedin'] = f"https://linkedin.com/in/{linkedin_match.group(1)}"
    
    # GitHub pattern
    github_pattern = r'github\.com/([A-Za-z0-9-]+)'
    github_match = re.search(github_pattern, text)
    if github_match:
        contact_info['github'] = f"https://github.com/{github_match.group(1)}"
    
    return contact_info


def validate_resume_completeness(resume_content: str) -> Dict[str, Any]:
    """Validate resume completeness and provide suggestions."""
    
    sections_found = {
        'contact_info': bool(extract_contact_info(resume_content)['email']),
        'summary': any(keyword in resume_content.lower() for keyword in ['summary', 'objective', 'profile']),
        'experience': any(keyword in resume_content.lower() for keyword in ['experience', 'work', 'employment']),
        'education': any(keyword in resume_content.lower() for keyword in ['education', 'degree', 'university']),
        'skills': any(keyword in resume_content.lower() for keyword in ['skills', 'technical', 'technologies']),
    }
    
    completeness_score = sum(sections_found.values()) / len(sections_found)
    
    missing_sections = [section for section, found in sections_found.items() if not found]
    
    suggestions = []
    if not sections_found['contact_info']:
        suggestions.append("Add contact information (email, phone, LinkedIn)")
    if not sections_found['summary']:
        suggestions.append("Add a professional summary or objective")
    if not sections_found['experience']:
        suggestions.append("Include work experience section")
    if not sections_found['education']:
        suggestions.append("Add education background")
    if not sections_found['skills']:
        suggestions.append("List relevant technical skills")
    
    return {
        'completeness_score': completeness_score,
        'sections_found': sections_found,
        'missing_sections': missing_sections,
        'suggestions': suggestions,
        'is_complete': completeness_score >= 0.8
    }