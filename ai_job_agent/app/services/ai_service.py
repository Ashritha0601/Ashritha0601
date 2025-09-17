import openai
import os
from typing import List, Dict, Any, Optional
from ..models.schemas import Resume, Job, CoverLetter


class AIService:
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    async def analyze_resume(self, resume_content: str) -> Dict[str, Any]:
        """Analyze resume content and extract key information."""
        prompt = f"""
        Analyze the following resume and extract:
        1. Key skills and technologies
        2. Experience level (entry, mid, senior, lead, executive)
        3. Career focus areas
        4. Strengths and improvement areas
        5. ATS-friendly score (1-10)
        
        Resume content:
        {resume_content}
        
        Please respond in JSON format with the following structure:
        {{
            "skills": ["skill1", "skill2", ...],
            "experience_level": "entry|mid|senior|lead|executive",
            "career_focus": ["area1", "area2", ...],
            "strengths": ["strength1", "strength2", ...],
            "improvement_areas": ["area1", "area2", ...],
            "ats_score": 8,
            "summary": "Brief analysis summary"
        }}
        """
        
        try:
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            
            import json
            analysis = json.loads(response.choices[0].message.content)
            return analysis
        except Exception as e:
            return {
                "error": str(e),
                "skills": [],
                "experience_level": "mid",
                "career_focus": [],
                "strengths": [],
                "improvement_areas": [],
                "ats_score": 5,
                "summary": "Analysis failed"
            }
    
    async def match_jobs_to_resume(self, resume: Resume, jobs: List[Job]) -> List[Job]:
        """Match jobs to resume based on skills and experience."""
        resume_analysis = await self.analyze_resume(resume.content)
        
        for job in jobs:
            match_score = await self._calculate_match_score(
                resume_analysis, job
            )
            job.match_score = match_score
        
        # Sort by match score descending
        return sorted(jobs, key=lambda x: x.match_score or 0, reverse=True)
    
    async def _calculate_match_score(self, resume_analysis: Dict, job: Job) -> float:
        """Calculate match score between resume and job."""
        prompt = f"""
        Calculate a match score (0-100) between a candidate and job based on:
        
        Candidate Profile:
        - Skills: {resume_analysis.get('skills', [])}
        - Experience Level: {resume_analysis.get('experience_level', 'mid')}
        - Career Focus: {resume_analysis.get('career_focus', [])}
        
        Job Details:
        - Title: {job.title}
        - Level: {job.level}
        - Requirements: {job.requirements}
        - Description: {job.description[:500]}...
        
        Consider:
        1. Skills alignment (40%)
        2. Experience level match (25%)
        3. Career focus alignment (20%)
        4. Overall fit (15%)
        
        Return only a number between 0-100.
        """
        
        try:
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1
            )
            
            score = float(response.choices[0].message.content.strip())
            return min(max(score, 0), 100)  # Ensure score is between 0-100
        except:
            return 50.0  # Default score if calculation fails
    
    async def optimize_resume_for_job(self, resume: Resume, job: Job) -> str:
        """Optimize resume content for a specific job."""
        prompt = f"""
        Optimize the following resume for this specific job posting. Keep the same format but:
        1. Highlight relevant skills and experience
        2. Adjust keywords to match job requirements
        3. Emphasize achievements that align with the role
        4. Maintain truthfulness - don't add false information
        
        Original Resume:
        {resume.content}
        
        Target Job:
        Title: {job.title}
        Company: {job.company}
        Requirements: {job.requirements}
        Description: {job.description}
        
        Return the optimized resume content:
        """
        
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            
            return response.choices[0].message.content
        except Exception as e:
            return f"Optimization failed: {str(e)}"
    
    async def generate_cover_letter(self, resume: Resume, job: Job, tone: str = "professional") -> str:
        """Generate a cover letter for a specific job application."""
        prompt = f"""
        Write a compelling cover letter for this job application with a {tone} tone.
        
        Job Details:
        - Title: {job.title}
        - Company: {job.company}
        - Requirements: {job.requirements}
        - Description: {job.description[:500]}...
        
        Candidate Profile (from resume):
        {resume.content[:1000]}...
        
        The cover letter should:
        1. Be 3-4 paragraphs
        2. Show enthusiasm for the role
        3. Highlight relevant experience and skills
        4. Demonstrate knowledge of the company
        5. Include a strong call to action
        
        Format it as a professional business letter.
        """
        
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5
            )
            
            return response.choices[0].message.content
        except Exception as e:
            return f"Cover letter generation failed: {str(e)}"
    
    async def suggest_skill_improvements(self, resume: Resume, job_market_trends: List[str]) -> Dict[str, Any]:
        """Suggest skills to add or improve based on market trends."""
        prompt = f"""
        Based on this resume and current job market trends, suggest skill improvements:
        
        Current Resume Skills:
        {resume.skills}
        
        Market Trends:
        {job_market_trends}
        
        Resume Content:
        {resume.content[:1000]}...
        
        Provide recommendations in JSON format:
        {{
            "skills_to_add": ["skill1", "skill2", ...],
            "skills_to_improve": ["skill1", "skill2", ...],
            "certifications_to_consider": ["cert1", "cert2", ...],
            "learning_resources": [
                {{"skill": "skill_name", "resources": ["resource1", "resource2"]}}
            ],
            "priority_level": "high|medium|low",
            "explanation": "Why these improvements are recommended"
        }}
        """
        
        try:
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.4
            )
            
            import json
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            return {
                "error": str(e),
                "skills_to_add": [],
                "skills_to_improve": [],
                "certifications_to_consider": [],
                "learning_resources": [],
                "priority_level": "medium",
                "explanation": "Analysis failed"
            }