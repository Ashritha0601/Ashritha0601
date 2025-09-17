import requests
import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime
from bs4 import BeautifulSoup
from ..models.schemas import Job, JobType, JobLevel, JobAlert


class JobService:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    async def search_jobs(self, keywords: List[str], location: str = "", 
                         job_type: Optional[JobType] = None, 
                         max_results: int = 50) -> List[Job]:
        """Search for jobs from multiple sources."""
        jobs = []
        
        # Search from different sources
        indeed_jobs = await self._search_indeed(keywords, location, max_results // 2)
        jobs.extend(indeed_jobs)
        
        # Add more job boards as needed
        # linkedin_jobs = await self._search_linkedin(keywords, location, max_results // 2)
        # jobs.extend(linkedin_jobs)
        
        # Remove duplicates and sort by relevance
        unique_jobs = self._remove_duplicates(jobs)
        return unique_jobs[:max_results]
    
    async def _search_indeed(self, keywords: List[str], location: str, max_results: int) -> List[Job]:
        """Search jobs from Indeed (simplified version for demo)."""
        jobs = []
        
        # This is a simplified mock implementation
        # In a real implementation, you would use Indeed's API or web scraping
        query = " ".join(keywords)
        
        # Mock job data for demonstration
        mock_jobs = [
            {
                "title": "Senior Data Engineer",
                "company": "TechCorp Inc.",
                "location": "Dallas, TX",
                "job_type": JobType.FULL_TIME,
                "level": JobLevel.SENIOR,
                "description": "We are seeking a Senior Data Engineer with expertise in Apache Kafka, Spark, and cloud technologies. The ideal candidate will have 5+ years of experience building scalable data pipelines and working with big data technologies.",
                "requirements": [
                    "5+ years of data engineering experience",
                    "Expertise in Apache Kafka and Apache Spark",
                    "Experience with cloud platforms (AWS, Azure, GCP)",
                    "Strong Python and SQL skills",
                    "Experience with data warehousing and ETL processes"
                ],
                "salary_range": "$120,000 - $160,000",
                "application_url": "https://example.com/job/1"
            },
            {
                "title": "Machine Learning Engineer",
                "company": "AI Solutions Ltd.",
                "location": "Austin, TX",
                "job_type": JobType.FULL_TIME,
                "level": JobLevel.MID,
                "description": "Join our ML team to build cutting-edge AI applications. Work with large datasets, implement ML models, and deploy them to production using modern MLOps practices.",
                "requirements": [
                    "3+ years of ML engineering experience",
                    "Strong Python programming skills",
                    "Experience with TensorFlow or PyTorch",
                    "Knowledge of MLOps tools and practices",
                    "Bachelor's degree in CS or related field"
                ],
                "salary_range": "$90,000 - $130,000",
                "application_url": "https://example.com/job/2"
            },
            {
                "title": "Backend Developer - Python/FastAPI",
                "company": "StartupXYZ",
                "location": "Remote",
                "job_type": JobType.REMOTE,
                "level": JobLevel.MID,
                "description": "Build scalable backend systems using Python and FastAPI. Work with microservices architecture and help scale our platform to handle millions of users.",
                "requirements": [
                    "3+ years of Python development experience",
                    "Experience with FastAPI or similar frameworks",
                    "Knowledge of database design and optimization",
                    "Experience with containerization (Docker)",
                    "Understanding of microservices architecture"
                ],
                "salary_range": "$80,000 - $120,000",
                "application_url": "https://example.com/job/3"
            },
            {
                "title": "Cloud Data Architect",
                "company": "Enterprise Solutions Inc.",
                "location": "Dallas, TX",
                "job_type": JobType.HYBRID,
                "level": JobLevel.SENIOR,
                "description": "Lead the design and implementation of cloud-based data architecture solutions. Work with Azure and AWS to build scalable, secure data platforms.",
                "requirements": [
                    "7+ years of data architecture experience",
                    "Expertise in Azure and AWS cloud platforms",
                    "Experience with data lakes and data warehouses",
                    "Strong knowledge of data governance and security",
                    "Leadership and mentoring experience"
                ],
                "salary_range": "$140,000 - $180,000",
                "application_url": "https://example.com/job/4"
            },
            {
                "title": "Data Scientist - AI/ML",
                "company": "Research Labs Co.",
                "location": "Plano, TX",
                "job_type": JobType.FULL_TIME,
                "level": JobLevel.MID,
                "description": "Apply advanced analytics and machine learning to solve business problems. Work with large datasets to extract insights and build predictive models.",
                "requirements": [
                    "Master's degree in Data Science or related field",
                    "4+ years of data science experience",
                    "Proficiency in Python, R, and SQL",
                    "Experience with scikit-learn, pandas, numpy",
                    "Strong statistical analysis skills"
                ],
                "salary_range": "$95,000 - $135,000",
                "application_url": "https://example.com/job/5"
            }
        ]
        
        for job_data in mock_jobs:
            if any(keyword.lower() in job_data["title"].lower() or 
                  keyword.lower() in job_data["description"].lower() 
                  for keyword in keywords):
                job = Job(
                    id=f"indeed_{hash(job_data['title'] + job_data['company'])}",
                    title=job_data["title"],
                    company=job_data["company"],
                    location=job_data["location"],
                    job_type=job_data["job_type"],
                    level=job_data["level"],
                    description=job_data["description"],
                    requirements=job_data["requirements"],
                    salary_range=job_data["salary_range"],
                    posted_date=datetime.now(),
                    application_url=job_data["application_url"]
                )
                jobs.append(job)
        
        return jobs
    
    def _remove_duplicates(self, jobs: List[Job]) -> List[Job]:
        """Remove duplicate jobs based on title and company."""
        seen = set()
        unique_jobs = []
        
        for job in jobs:
            key = f"{job.title.lower()}_{job.company.lower()}"
            if key not in seen:
                seen.add(key)
                unique_jobs.append(job)
        
        return unique_jobs
    
    async def create_job_alert(self, alert: JobAlert) -> str:
        """Create a job alert for automated job searching."""
        # In a real implementation, this would save to a database
        # and set up scheduled searches
        alert_id = f"alert_{hash(alert.user_id + str(alert.keywords))}"
        alert.id = alert_id
        alert.created_at = datetime.now()
        
        # Mock saving to database
        print(f"Created job alert {alert_id} for user {alert.user_id}")
        return alert_id
    
    async def check_job_alerts(self, user_id: str) -> List[Job]:
        """Check active job alerts and return new matching jobs."""
        # In a real implementation, this would:
        # 1. Fetch active alerts for the user
        # 2. Search for jobs matching each alert
        # 3. Filter out jobs that were already sent
        # 4. Return new matches
        
        # Mock implementation
        mock_alert = JobAlert(
            user_id=user_id,
            keywords=["data engineer", "python", "kafka"],
            locations=["Dallas", "Austin"],
            job_types=[JobType.FULL_TIME, JobType.REMOTE],
            levels=[JobLevel.MID, JobLevel.SENIOR],
            is_active=True
        )
        
        return await self.search_jobs(
            keywords=mock_alert.keywords,
            location="Dallas, TX",
            max_results=10
        )
    
    async def get_job_market_trends(self, skills: List[str]) -> List[str]:
        """Get current job market trends for specific skills."""
        # Mock implementation - in reality, this would analyze job postings
        # and provide insights about trending skills and requirements
        
        trends = [
            "Kubernetes and container orchestration skills are in high demand",
            "Cloud certifications (Azure, AWS) are increasingly required",
            "Real-time data processing with Kafka and Spark is trending",
            "MLOps and AI engineering roles are growing rapidly",
            "Python remains the most requested programming language",
            "Data governance and privacy skills are becoming essential",
            "DevOps practices are expected for data engineers",
            "NoSQL databases (MongoDB, Cassandra) are in demand"
        ]
        
        # Filter trends based on provided skills
        relevant_trends = []
        for trend in trends:
            if any(skill.lower() in trend.lower() for skill in skills):
                relevant_trends.append(trend)
        
        return relevant_trends[:5]  # Return top 5 relevant trends