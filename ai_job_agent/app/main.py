from fastapi import FastAPI, HTTPException, UploadFile, File, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from typing import List, Optional
import os
import tempfile
from datetime import datetime

from .models.schemas import (
    Job, Resume, CoverLetter, JobAlert, User,
    JobMatchRequest, ResumeUpdateRequest, CoverLetterRequest
)
from .services.ai_service import AIService
from .services.job_service import JobService
from .services.resume_service import ResumeService
from .services.notification_service import NotificationService

# Initialize FastAPI app
app = FastAPI(
    title="AI Job Agent",
    description="An intelligent system for job searching, resume optimization, and cover letter generation",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
ai_service = AIService()
job_service = JobService()
resume_service = ResumeService()
notification_service = NotificationService()

# Default user for demo purposes
DEFAULT_USER = User(
    id="user_001",
    name="Ashritha Battula",
    email="work.ashrithabattula@gmail.com",
    preferences={
        "job_types": ["full_time", "remote"],
        "locations": ["Dallas", "Austin", "Remote"],
        "salary_min": 80000
    }
)


@app.get("/", response_class=HTMLResponse)
async def root():
    """Root endpoint with welcome message."""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>AI Job Agent</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 40px; border-radius: 10px; }
            .header { text-align: center; color: #2563eb; margin-bottom: 30px; }
            .feature { margin: 20px 0; padding: 15px; background-color: #f8f9fa; border-radius: 5px; }
            .endpoint { background-color: #e3f2fd; padding: 10px; margin: 10px 0; border-radius: 5px; }
            .method { font-weight: bold; color: #1976d2; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🤖 AI Job Agent</h1>
                <p>Your intelligent career companion</p>
            </div>
            
            <div class="feature">
                <h3>🚀 Features</h3>
                <ul>
                    <li>Intelligent job search and matching</li>
                    <li>Resume optimization for specific jobs</li>
                    <li>AI-powered cover letter generation</li>
                    <li>Automated job alerts and notifications</li>
                    <li>Career advice and skill recommendations</li>
                </ul>
            </div>
            
            <div class="feature">
                <h3>📚 API Endpoints</h3>
                
                <div class="endpoint">
                    <span class="method">GET</span> /docs - Interactive API documentation
                </div>
                
                <div class="endpoint">
                    <span class="method">POST</span> /jobs/search - Search for jobs
                </div>
                
                <div class="endpoint">
                    <span class="method">POST</span> /resume/upload - Upload and parse resume
                </div>
                
                <div class="endpoint">
                    <span class="method">POST</span> /resume/optimize - Optimize resume for job
                </div>
                
                <div class="endpoint">
                    <span class="method">POST</span> /cover-letter/generate - Generate cover letter
                </div>
                
                <div class="endpoint">
                    <span class="method">POST</span> /alerts/create - Create job alert
                </div>
                
                <div class="endpoint">
                    <span class="method">GET</span> /demo/run - Run complete demo
                </div>
            </div>
            
            <div style="text-align: center; margin-top: 30px;">
                <a href="/docs" style="background-color: #2563eb; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">
                    Explore API Documentation
                </a>
            </div>
        </div>
    </body>
    </html>
    """


@app.post("/jobs/search", response_model=List[Job])
async def search_jobs(request: JobMatchRequest):
    """Search for jobs based on criteria."""
    try:
        # Get user's resume for better matching
        resume = await resume_service.load_resume(request.resume_id)
        if not resume:
            # Create sample resume if not found
            resume = await resume_service.create_sample_resume()
        
        # Search jobs
        jobs = await job_service.search_jobs(
            keywords=resume.skills[:5],  # Use top 5 skills as keywords
            location=request.location_preferences[0] if request.location_preferences else "Dallas, TX",
            max_results=request.max_results
        )
        
        # Match jobs to resume
        matched_jobs = await ai_service.match_jobs_to_resume(resume, jobs)
        
        return matched_jobs
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/resume/upload", response_model=Resume)
async def upload_resume(file: UploadFile = File(...), user_id: str = "user_001"):
    """Upload and parse a resume file."""
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        try:
            # Parse resume
            resume = await resume_service.parse_resume_file(temp_file_path, user_id)
            return resume
        finally:
            # Clean up temp file
            os.unlink(temp_file_path)
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/resume/optimize", response_model=Resume)
async def optimize_resume(request: ResumeUpdateRequest, background_tasks: BackgroundTasks):
    """Optimize resume for a specific job description."""
    try:
        optimized_resume = await resume_service.optimize_resume_for_job(
            request.resume_id, 
            request.job_description
        )
        
        # Send notification in background
        background_tasks.add_task(
            notification_service.send_resume_update_notification,
            DEFAULT_USER,
            request.resume_id,
            optimized_resume.id,
            "Target Job"
        )
        
        return optimized_resume
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/cover-letter/generate", response_model=CoverLetter)
async def generate_cover_letter(request: CoverLetterRequest, background_tasks: BackgroundTasks):
    """Generate a cover letter for a job application."""
    try:
        # Load resume
        resume = await resume_service.load_resume(request.resume_id)
        if not resume:
            raise HTTPException(status_code=404, detail="Resume not found")
        
        # For demo, create a mock job based on job_id
        from .models.schemas import JobType, JobLevel
        mock_job = Job(
            id=request.job_id,
            title="Senior Data Engineer",
            company="TechCorp Inc.",
            location="Dallas, TX",
            job_type=JobType.FULL_TIME,
            level=JobLevel.SENIOR,
            description="We are seeking a Senior Data Engineer with expertise in Apache Kafka, Spark, and cloud technologies.",
            requirements=["5+ years experience", "Python", "Kafka", "Spark", "Cloud platforms"],
            application_url="https://example.com/apply"
        )
        
        # Generate cover letter
        cover_letter_content = await ai_service.generate_cover_letter(
            resume, mock_job, request.tone
        )
        
        # Create cover letter object
        cover_letter = CoverLetter(
            id=f"cover_letter_{hash(request.resume_id + request.job_id)}",
            job_id=request.job_id,
            resume_id=request.resume_id,
            content=cover_letter_content,
            created_at=datetime.now()
        )
        
        # Send notification in background
        background_tasks.add_task(
            notification_service.send_cover_letter_notification,
            DEFAULT_USER,
            mock_job.title,
            mock_job.company,
            cover_letter.id
        )
        
        return cover_letter
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/alerts/create", response_model=str)
async def create_job_alert(alert: JobAlert):
    """Create a job alert for automated job searching."""
    try:
        alert_id = await job_service.create_job_alert(alert)
        return alert_id
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/alerts/check/{user_id}")
async def check_job_alerts(user_id: str, background_tasks: BackgroundTasks):
    """Check job alerts and send notifications if new jobs found."""
    try:
        new_jobs = await job_service.check_job_alerts(user_id)
        
        if new_jobs:
            # Create mock alert for notification
            mock_alert = JobAlert(
                user_id=user_id,
                keywords=["data engineer", "python"],
                locations=["Dallas", "Austin"],
                job_types=[],
                levels=[],
                is_active=True,
                created_at=datetime.now()
            )
            
            # Send notification in background
            background_tasks.add_task(
                notification_service.send_job_alert_email,
                DEFAULT_USER,
                new_jobs,
                mock_alert
            )
        
        return {"message": f"Found {len(new_jobs)} new jobs", "jobs": len(new_jobs)}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/resume/{resume_id}", response_model=Resume)
async def get_resume(resume_id: str):
    """Get a specific resume."""
    try:
        resume = await resume_service.load_resume(resume_id)
        if not resume:
            raise HTTPException(status_code=404, detail="Resume not found")
        return resume
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/resumes/{user_id}", response_model=List[Resume])
async def get_user_resumes(user_id: str):
    """Get all resumes for a user."""
    try:
        resumes = await resume_service.get_user_resumes(user_id)
        return resumes
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/skills/suggestions/{resume_id}")
async def get_skill_suggestions(resume_id: str):
    """Get skill improvement suggestions for a resume."""
    try:
        resume = await resume_service.load_resume(resume_id)
        if not resume:
            raise HTTPException(status_code=404, detail="Resume not found")
        
        # Get market trends
        trends = await job_service.get_job_market_trends(resume.skills)
        
        # Get AI suggestions
        suggestions = await ai_service.suggest_skill_improvements(resume, trends)
        
        return suggestions
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/demo/run")
async def run_demo():
    """Run a complete demo of the AI Job Agent system."""
    try:
        demo_results = {}
        
        # 1. Create sample resume
        demo_results["step_1"] = "Creating sample resume..."
        resume = await resume_service.create_sample_resume()
        demo_results["resume_created"] = {
            "id": resume.id,
            "title": resume.title,
            "skills_count": len(resume.skills)
        }
        
        # 2. Search for jobs
        demo_results["step_2"] = "Searching for matching jobs..."
        jobs = await job_service.search_jobs(
            keywords=resume.skills[:3],
            location="Dallas, TX",
            max_results=5
        )
        
        # 3. Match jobs to resume
        matched_jobs = await ai_service.match_jobs_to_resume(resume, jobs)
        demo_results["jobs_found"] = {
            "total_jobs": len(matched_jobs),
            "top_job": {
                "title": matched_jobs[0].title if matched_jobs else "No jobs found",
                "company": matched_jobs[0].company if matched_jobs else "",
                "match_score": matched_jobs[0].match_score if matched_jobs and matched_jobs[0].match_score else 0
            }
        }
        
        # 4. Optimize resume for top job
        if matched_jobs:
            demo_results["step_3"] = "Optimizing resume for top job..."
            top_job = matched_jobs[0]
            optimized_resume = await resume_service.optimize_resume_for_job(
                resume.id, 
                top_job.description
            )
            demo_results["resume_optimized"] = {
                "id": optimized_resume.id,
                "title": optimized_resume.title
            }
            
            # 5. Generate cover letter
            demo_results["step_4"] = "Generating cover letter..."
            cover_letter_content = await ai_service.generate_cover_letter(
                resume, top_job, "professional"
            )
            demo_results["cover_letter_generated"] = {
                "length": len(cover_letter_content),
                "preview": cover_letter_content[:200] + "..."
            }
        
        # 6. Get skill suggestions
        demo_results["step_5"] = "Analyzing skill gaps..."
        trends = await job_service.get_job_market_trends(resume.skills)
        suggestions = await ai_service.suggest_skill_improvements(resume, trends)
        demo_results["skill_suggestions"] = {
            "skills_to_add": suggestions.get("skills_to_add", [])[:3],
            "priority": suggestions.get("priority_level", "medium")
        }
        
        # 7. Create job alert
        demo_results["step_6"] = "Setting up job alert..."
        from .models.schemas import JobType, JobLevel
        alert = JobAlert(
            user_id="user_001",
            keywords=resume.skills[:3],
            locations=["Dallas", "Austin"],
            job_types=[JobType.FULL_TIME, JobType.REMOTE],
            levels=[JobLevel.MID, JobLevel.SENIOR],
            is_active=True
        )
        alert_id = await job_service.create_job_alert(alert)
        demo_results["alert_created"] = alert_id
        
        demo_results["demo_status"] = "✅ Complete! All AI Job Agent features demonstrated successfully."
        
        return demo_results
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Demo failed: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)