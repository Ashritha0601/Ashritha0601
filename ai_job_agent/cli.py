#!/usr/bin/env python3
"""
CLI interface for the AI Job Agent system.
"""

import asyncio
import click
import json
import os
from datetime import datetime
from typing import List

from app.services.ai_service import AIService
from app.services.job_service import JobService
from app.services.resume_service import ResumeService
from app.services.notification_service import NotificationService
from app.models.schemas import JobAlert, JobType, JobLevel, User


class JobAgentCLI:
    def __init__(self):
        self.ai_service = AIService()
        self.job_service = JobService()
        self.resume_service = ResumeService()
        self.notification_service = NotificationService()
        
        # Default user
        self.user = User(
            id="cli_user",
            name="CLI User",
            email=os.getenv("USER_EMAIL", "user@example.com")
        )


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """AI Job Agent - Your intelligent career companion."""
    pass


@cli.command()
@click.option('--keywords', '-k', multiple=True, required=True, 
              help='Keywords to search for (can specify multiple times)')
@click.option('--location', '-l', default='Dallas, TX', 
              help='Job location (default: Dallas, TX)')
@click.option('--max-results', '-n', default=10, 
              help='Maximum number of results (default: 10)')
def search_jobs(keywords: List[str], location: str, max_results: int):
    """Search for jobs based on keywords and location."""
    
    async def _search():
        agent = JobAgentCLI()
        
        click.echo(f"🔍 Searching for jobs with keywords: {', '.join(keywords)}")
        click.echo(f"📍 Location: {location}")
        click.echo(f"📊 Max results: {max_results}")
        click.echo()
        
        jobs = await agent.job_service.search_jobs(
            keywords=list(keywords),
            location=location,
            max_results=max_results
        )
        
        if not jobs:
            click.echo("❌ No jobs found matching your criteria.")
            return
        
        click.echo(f"✅ Found {len(jobs)} job opportunities:")
        click.echo("=" * 80)
        
        for i, job in enumerate(jobs, 1):
            click.echo(f"\n{i}. {job.title}")
            click.echo(f"   Company: {job.company}")
            click.echo(f"   Location: {job.location}")
            click.echo(f"   Type: {job.job_type.value}")
            click.echo(f"   Level: {job.level.value}")
            click.echo(f"   Salary: {job.salary_range or 'Not specified'}")
            if job.match_score:
                click.echo(f"   Match Score: {job.match_score:.1f}%")
            click.echo(f"   Apply: {job.application_url}")
            click.echo("-" * 40)
    
    asyncio.run(_search())


@cli.command()
@click.option('--file-path', '-f', required=True, type=click.Path(exists=True),
              help='Path to resume file (PDF or DOCX)')
@click.option('--user-id', '-u', default='cli_user',
              help='User ID (default: cli_user)')
def upload_resume(file_path: str, user_id: str):
    """Upload and parse a resume file."""
    
    async def _upload():
        agent = JobAgentCLI()
        
        click.echo(f"📄 Parsing resume: {file_path}")
        
        try:
            resume = await agent.resume_service.parse_resume_file(file_path, user_id)
            
            click.echo("✅ Resume parsed successfully!")
            click.echo(f"   Resume ID: {resume.id}")
            click.echo(f"   Title: {resume.title}")
            click.echo(f"   Skills found: {len(resume.skills)}")
            click.echo(f"   Experience entries: {len(resume.experience)}")
            click.echo(f"   Education entries: {len(resume.education)}")
            
            # Display skills
            if resume.skills:
                click.echo("\n🛠️  Skills identified:")
                for skill in resume.skills[:10]:  # Show first 10 skills
                    click.echo(f"   • {skill}")
                if len(resume.skills) > 10:
                    click.echo(f"   ... and {len(resume.skills) - 10} more")
            
        except Exception as e:
            click.echo(f"❌ Failed to parse resume: {str(e)}")
    
    asyncio.run(_upload())


@cli.command()
@click.option('--resume-id', '-r', required=True,
              help='Resume ID to optimize')
@click.option('--job-description', '-j', required=True,
              help='Job description to optimize for')
def optimize_resume(resume_id: str, job_description: str):
    """Optimize resume for a specific job description."""
    
    async def _optimize():
        agent = JobAgentCLI()
        
        click.echo(f"🔧 Optimizing resume {resume_id} for target job...")
        
        try:
            optimized_resume = await agent.resume_service.optimize_resume_for_job(
                resume_id, job_description
            )
            
            click.echo("✅ Resume optimization complete!")
            click.echo(f"   Optimized Resume ID: {optimized_resume.id}")
            click.echo(f"   Title: {optimized_resume.title}")
            
            # Save optimized content to file
            output_file = f"optimized_resume_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(output_file, 'w') as f:
                f.write(optimized_resume.content)
            
            click.echo(f"   Saved to: {output_file}")
            
        except Exception as e:
            click.echo(f"❌ Failed to optimize resume: {str(e)}")
    
    asyncio.run(_optimize())


@cli.command()
@click.option('--resume-id', '-r', required=True,
              help='Resume ID to use')
@click.option('--job-title', '-t', required=True,
              help='Job title')
@click.option('--company', '-c', required=True,
              help='Company name')
@click.option('--tone', default='professional',
              type=click.Choice(['professional', 'enthusiastic', 'creative']),
              help='Cover letter tone (default: professional)')
def generate_cover_letter(resume_id: str, job_title: str, company: str, tone: str):
    """Generate a cover letter for a job application."""
    
    async def _generate():
        agent = JobAgentCLI()
        
        click.echo(f"📝 Generating {tone} cover letter...")
        click.echo(f"   Position: {job_title}")
        click.echo(f"   Company: {company}")
        
        try:
            # Load resume
            resume = await agent.resume_service.load_resume(resume_id)
            if not resume:
                click.echo(f"❌ Resume {resume_id} not found")
                return
            
            # Create mock job
            from app.models.schemas import Job, JobType, JobLevel
            mock_job = Job(
                id="cli_job",
                title=job_title,
                company=company,
                location="Location",
                job_type=JobType.FULL_TIME,
                level=JobLevel.MID,
                description=f"We are looking for a {job_title} to join our team at {company}.",
                requirements=[],
                application_url="https://example.com/apply"
            )
            
            # Generate cover letter
            cover_letter_content = await agent.ai_service.generate_cover_letter(
                resume, mock_job, tone
            )
            
            # Save to file
            output_file = f"cover_letter_{company}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(output_file, 'w') as f:
                f.write(cover_letter_content)
            
            click.echo("✅ Cover letter generated successfully!")
            click.echo(f"   Saved to: {output_file}")
            
            # Preview first few lines
            lines = cover_letter_content.split('\n')[:5]
            click.echo("\n📖 Preview:")
            for line in lines:
                if line.strip():
                    click.echo(f"   {line}")
            click.echo("   ...")
            
        except Exception as e:
            click.echo(f"❌ Failed to generate cover letter: {str(e)}")
    
    asyncio.run(_generate())


@cli.command()
@click.option('--keywords', '-k', multiple=True, required=True,
              help='Keywords to alert for')
@click.option('--locations', '-l', multiple=True, required=True,
              help='Locations to search in')
@click.option('--user-id', '-u', default='cli_user',
              help='User ID (default: cli_user)')
def create_alert(keywords: List[str], locations: List[str], user_id: str):
    """Create a job alert for automated job searching."""
    
    async def _create_alert():
        agent = JobAgentCLI()
        
        click.echo("🔔 Creating job alert...")
        click.echo(f"   Keywords: {', '.join(keywords)}")
        click.echo(f"   Locations: {', '.join(locations)}")
        
        try:
            alert = JobAlert(
                user_id=user_id,
                keywords=list(keywords),
                locations=list(locations),
                job_types=[JobType.FULL_TIME, JobType.REMOTE],
                levels=[JobLevel.MID, JobLevel.SENIOR],
                is_active=True
            )
            
            alert_id = await agent.job_service.create_job_alert(alert)
            
            click.echo("✅ Job alert created successfully!")
            click.echo(f"   Alert ID: {alert_id}")
            
        except Exception as e:
            click.echo(f"❌ Failed to create alert: {str(e)}")
    
    asyncio.run(_create_alert())


@cli.command()
@click.option('--user-id', '-u', default='cli_user',
              help='User ID to check alerts for')
def check_alerts(user_id: str):
    """Check job alerts and display new matches."""
    
    async def _check_alerts():
        agent = JobAgentCLI()
        
        click.echo(f"🔍 Checking job alerts for user {user_id}...")
        
        try:
            new_jobs = await agent.job_service.check_job_alerts(user_id)
            
            if not new_jobs:
                click.echo("📭 No new job matches found.")
                return
            
            click.echo(f"🎉 Found {len(new_jobs)} new job matches!")
            click.echo("=" * 60)
            
            for i, job in enumerate(new_jobs[:5], 1):  # Show top 5
                click.echo(f"\n{i}. {job.title} at {job.company}")
                click.echo(f"   📍 {job.location}")
                click.echo(f"   💰 {job.salary_range or 'Salary not specified'}")
                if job.match_score:
                    click.echo(f"   🎯 Match: {job.match_score:.1f}%")
                click.echo(f"   🔗 {job.application_url}")
            
            if len(new_jobs) > 5:
                click.echo(f"\n... and {len(new_jobs) - 5} more matches!")
            
        except Exception as e:
            click.echo(f"❌ Failed to check alerts: {str(e)}")
    
    asyncio.run(_check_alerts())


@cli.command()
@click.option('--resume-id', '-r', required=True,
              help='Resume ID to analyze')
def analyze_skills(resume_id: str):
    """Analyze skills and get improvement suggestions."""
    
    async def _analyze():
        agent = JobAgentCLI()
        
        click.echo(f"🔍 Analyzing skills for resume {resume_id}...")
        
        try:
            # Load resume
            resume = await agent.resume_service.load_resume(resume_id)
            if not resume:
                click.echo(f"❌ Resume {resume_id} not found")
                return
            
            # Get market trends
            trends = await agent.job_service.get_job_market_trends(resume.skills)
            
            # Get skill suggestions
            suggestions = await agent.ai_service.suggest_skill_improvements(resume, trends)
            
            click.echo("✅ Skills analysis complete!")
            click.echo("=" * 60)
            
            click.echo("\n🎯 Current Skills:")
            for skill in resume.skills[:10]:
                click.echo(f"   • {skill}")
            if len(resume.skills) > 10:
                click.echo(f"   ... and {len(resume.skills) - 10} more")
            
            if suggestions.get('skills_to_add'):
                click.echo("\n📈 Recommended Skills to Add:")
                for skill in suggestions['skills_to_add']:
                    click.echo(f"   + {skill}")
            
            if suggestions.get('skills_to_improve'):
                click.echo("\n🔧 Skills to Improve:")
                for skill in suggestions['skills_to_improve']:
                    click.echo(f"   ↗️ {skill}")
            
            if suggestions.get('certifications_to_consider'):
                click.echo("\n🏆 Certifications to Consider:")
                for cert in suggestions['certifications_to_consider']:
                    click.echo(f"   📜 {cert}")
            
            click.echo(f"\n📊 Priority Level: {suggestions.get('priority_level', 'Medium')}")
            
            if suggestions.get('explanation'):
                click.echo(f"\n💡 {suggestions['explanation']}")
            
        except Exception as e:
            click.echo(f"❌ Failed to analyze skills: {str(e)}")
    
    asyncio.run(_analyze())


@cli.command()
def demo():
    """Run a complete demo of the AI Job Agent system."""
    
    async def _demo():
        agent = JobAgentCLI()
        
        click.echo("🚀 Starting AI Job Agent Demo")
        click.echo("=" * 50)
        
        try:
            # Step 1: Create sample resume
            click.echo("\n1️⃣ Creating sample resume...")
            resume = await agent.resume_service.create_sample_resume()
            click.echo(f"   ✅ Created resume: {resume.id}")
            
            # Step 2: Search for jobs
            click.echo("\n2️⃣ Searching for matching jobs...")
            jobs = await agent.job_service.search_jobs(
                keywords=resume.skills[:3],
                location="Dallas, TX",
                max_results=5
            )
            click.echo(f"   ✅ Found {len(jobs)} job opportunities")
            
            # Step 3: Match jobs to resume
            click.echo("\n3️⃣ Calculating job matches...")
            matched_jobs = await agent.ai_service.match_jobs_to_resume(resume, jobs)
            if matched_jobs:
                top_job = matched_jobs[0]
                click.echo(f"   ✅ Top match: {top_job.title} at {top_job.company}")
                click.echo(f"   🎯 Match score: {top_job.match_score:.1f}%")
            
            # Step 4: Generate cover letter
            if matched_jobs:
                click.echo("\n4️⃣ Generating cover letter...")
                cover_letter = await agent.ai_service.generate_cover_letter(
                    resume, matched_jobs[0], "professional"
                )
                click.echo(f"   ✅ Cover letter generated ({len(cover_letter)} characters)")
            
            # Step 5: Get skill suggestions
            click.echo("\n5️⃣ Analyzing skill gaps...")
            trends = await agent.job_service.get_job_market_trends(resume.skills)
            suggestions = await agent.ai_service.suggest_skill_improvements(resume, trends)
            
            if suggestions.get('skills_to_add'):
                click.echo(f"   📈 Recommended skills: {', '.join(suggestions['skills_to_add'][:3])}")
            
            click.echo("\n🎉 Demo completed successfully!")
            click.echo("🔗 Try the web interface: python -m ai_job_agent.app.main")
            
        except Exception as e:
            click.echo(f"❌ Demo failed: {str(e)}")
    
    asyncio.run(_demo())


if __name__ == '__main__':
    cli()