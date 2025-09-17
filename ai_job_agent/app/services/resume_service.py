import os
import json
from typing import List, Dict, Any, Optional
from datetime import datetime
import PyPDF2
from docx import Document
from ..models.schemas import Resume, ResumeSection
from .ai_service import AIService


class ResumeService:
    def __init__(self):
        self.ai_service = AIService()
        self.resume_storage_path = "data/resumes"
        os.makedirs(self.resume_storage_path, exist_ok=True)
    
    async def parse_resume_file(self, file_path: str, user_id: str) -> Resume:
        """Parse resume from PDF or DOCX file."""
        content = ""
        
        if file_path.endswith('.pdf'):
            content = self._extract_text_from_pdf(file_path)
        elif file_path.endswith('.docx'):
            content = self._extract_text_from_docx(file_path)
        else:
            raise ValueError("Unsupported file format. Please use PDF or DOCX.")
        
        # Use AI to structure the resume
        structured_data = await self.ai_service.analyze_resume(content)
        
        # Create sections
        sections = self._create_sections_from_content(content)
        
        resume = Resume(
            id=f"resume_{hash(user_id + str(datetime.now()))}",
            user_id=user_id,
            title=f"Resume - {datetime.now().strftime('%Y-%m-%d')}",
            content=content,
            sections=sections,
            skills=structured_data.get('skills', []),
            experience=self._extract_experience(content),
            education=self._extract_education(content),
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        # Save resume
        await self.save_resume(resume)
        return resume
    
    def _extract_text_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF file."""
        text = ""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
        except Exception as e:
            raise ValueError(f"Error reading PDF file: {str(e)}")
        
        return text.strip()
    
    def _extract_text_from_docx(self, file_path: str) -> str:
        """Extract text from DOCX file."""
        text = ""
        try:
            doc = Document(file_path)
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
        except Exception as e:
            raise ValueError(f"Error reading DOCX file: {str(e)}")
        
        return text.strip()
    
    def _create_sections_from_content(self, content: str) -> List[ResumeSection]:
        """Create structured sections from resume content."""
        sections = []
        
        # Common section headers
        section_headers = [
            ("Summary", ["summary", "profile", "objective"]),
            ("Experience", ["experience", "work history", "employment"]),
            ("Education", ["education", "academic", "qualifications"]),
            ("Skills", ["skills", "technical skills", "competencies"]),
            ("Projects", ["projects", "portfolio"]),
            ("Certifications", ["certifications", "certificates"]),
            ("Awards", ["awards", "achievements", "honors"])
        ]
        
        lines = content.split('\n')
        current_section = None
        current_content = []
        order = 1
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if line is a section header
            is_header = False
            for section_name, keywords in section_headers:
                if any(keyword.lower() in line.lower() for keyword in keywords):
                    # Save previous section
                    if current_section and current_content:
                        sections.append(ResumeSection(
                            section_name=current_section,
                            content='\n'.join(current_content),
                            order=order
                        ))
                        order += 1
                    
                    current_section = section_name
                    current_content = []
                    is_header = True
                    break
            
            if not is_header and current_section:
                current_content.append(line)
        
        # Add final section
        if current_section and current_content:
            sections.append(ResumeSection(
                section_name=current_section,
                content='\n'.join(current_content),
                order=order
            ))
        
        return sections
    
    def _extract_experience(self, content: str) -> List[Dict[str, Any]]:
        """Extract work experience from resume content."""
        # This is a simplified extraction - in reality, you'd use more sophisticated parsing
        experience = []
        
        # Look for patterns like "Company Name - Job Title (Dates)"
        lines = content.split('\n')
        in_experience_section = False
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if we're in experience section
            if any(keyword in line.lower() for keyword in ["experience", "work history", "employment"]):
                in_experience_section = True
                continue
            
            # Check if we're leaving experience section
            if in_experience_section and any(keyword in line.lower() for keyword in ["education", "skills", "projects"]):
                in_experience_section = False
                continue
            
            if in_experience_section:
                # Simple pattern matching for job entries
                if '-' in line and ('(' in line or any(year in line for year in ['2020', '2021', '2022', '2023', '2024'])):
                    parts = line.split('-', 1)
                    if len(parts) == 2:
                        company = parts[0].strip()
                        title_and_dates = parts[1].strip()
                        
                        experience.append({
                            "company": company,
                            "title": title_and_dates,
                            "description": "",
                            "duration": "Date range to be parsed"
                        })
        
        return experience
    
    def _extract_education(self, content: str) -> List[Dict[str, Any]]:
        """Extract education information from resume content."""
        education = []
        
        # Look for education section
        lines = content.split('\n')
        in_education_section = False
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if we're in education section
            if any(keyword in line.lower() for keyword in ["education", "academic", "qualifications"]):
                in_education_section = True
                continue
            
            # Check if we're leaving education section
            if in_education_section and any(keyword in line.lower() for keyword in ["experience", "skills", "projects"]):
                in_education_section = False
                continue
            
            if in_education_section:
                # Look for degree patterns
                if any(degree in line.lower() for degree in ["bachelor", "master", "phd", "doctorate", "degree"]):
                    education.append({
                        "institution": "Institution to be parsed",
                        "degree": line,
                        "year": "Year to be parsed",
                        "gpa": ""
                    })
        
        return education
    
    async def save_resume(self, resume: Resume) -> str:
        """Save resume to storage."""
        file_path = os.path.join(self.resume_storage_path, f"{resume.id}.json")
        
        resume_dict = resume.dict()
        # Convert datetime objects to strings for JSON serialization
        if resume_dict.get('created_at'):
            resume_dict['created_at'] = resume_dict['created_at'].isoformat()
        if resume_dict.get('updated_at'):
            resume_dict['updated_at'] = resume_dict['updated_at'].isoformat()
        
        with open(file_path, 'w') as f:
            json.dump(resume_dict, f, indent=2)
        
        return file_path
    
    async def load_resume(self, resume_id: str) -> Optional[Resume]:
        """Load resume from storage."""
        file_path = os.path.join(self.resume_storage_path, f"{resume_id}.json")
        
        if not os.path.exists(file_path):
            return None
        
        with open(file_path, 'r') as f:
            resume_dict = json.load(f)
        
        # Convert string dates back to datetime objects
        if resume_dict.get('created_at'):
            resume_dict['created_at'] = datetime.fromisoformat(resume_dict['created_at'])
        if resume_dict.get('updated_at'):
            resume_dict['updated_at'] = datetime.fromisoformat(resume_dict['updated_at'])
        
        return Resume(**resume_dict)
    
    async def update_resume(self, resume_id: str, updates: Dict[str, Any]) -> Resume:
        """Update existing resume."""
        resume = await self.load_resume(resume_id)
        if not resume:
            raise ValueError(f"Resume {resume_id} not found")
        
        # Update fields
        for key, value in updates.items():
            if hasattr(resume, key):
                setattr(resume, key, value)
        
        resume.updated_at = datetime.now()
        await self.save_resume(resume)
        return resume
    
    async def optimize_resume_for_job(self, resume_id: str, job_description: str) -> Resume:
        """Optimize resume for a specific job."""
        resume = await self.load_resume(resume_id)
        if not resume:
            raise ValueError(f"Resume {resume_id} not found")
        
        # Create a mock job object for optimization
        from ..models.schemas import Job, JobType, JobLevel
        job = Job(
            title="Target Job",
            company="Target Company",
            location="Location",
            job_type=JobType.FULL_TIME,
            level=JobLevel.MID,
            description=job_description,
            requirements=[],
            application_url=""
        )
        
        # Use AI service to optimize
        optimized_content = await self.ai_service.optimize_resume_for_job(resume, job)
        
        # Create new optimized resume
        optimized_resume = Resume(
            id=f"resume_optimized_{hash(resume_id + job_description)}",
            user_id=resume.user_id,
            title=f"{resume.title} - Optimized",
            content=optimized_content,
            sections=resume.sections,  # Keep original sections for now
            skills=resume.skills,
            experience=resume.experience,
            education=resume.education,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        await self.save_resume(optimized_resume)
        return optimized_resume
    
    async def get_user_resumes(self, user_id: str) -> List[Resume]:
        """Get all resumes for a user."""
        resumes = []
        
        for filename in os.listdir(self.resume_storage_path):
            if filename.endswith('.json'):
                resume_id = filename[:-5]  # Remove .json extension
                resume = await self.load_resume(resume_id)
                if resume and resume.user_id == user_id:
                    resumes.append(resume)
        
        return sorted(resumes, key=lambda x: x.created_at or datetime.min, reverse=True)
    
    async def create_sample_resume(self, user_id: str = "user_001") -> Resume:
        """Create a sample resume for testing."""
        sample_content = """
        Ashritha Battula
        Data Engineer | AI/ML Enthusiast | Cloud Learner
        work.ashrithabattula@gmail.com
        
        SUMMARY
        Passionate Data Engineer with Master's in Computer Science from University of North Texas (GPA: 3.94). 
        Experienced in building real-time data pipelines, scalable backend systems, and AI-powered applications.
        
        EXPERIENCE
        Data Engineering Intern - TechCorp (2023-2024)
        • Built real-time data pipelines using Apache Kafka and Spark
        • Developed ETL processes for processing 1M+ records daily
        • Implemented data quality monitoring and alerting systems
        
        Software Developer - StartupXYZ (2022-2023)
        • Developed backend APIs using Python and FastAPI
        • Optimized database queries resulting in 40% performance improvement
        • Implemented microservices architecture using Docker containers
        
        EDUCATION
        Master of Science in Computer Science
        University of North Texas - GPA: 3.94 (2022-2024)
        
        SKILLS
        • Programming: Python, SQL, JavaScript, Go
        • Data Engineering: Apache Kafka, Apache Spark, ETL pipelines
        • Cloud: Microsoft Azure, AWS, PostgreSQL, MongoDB
        • Frameworks: FastAPI, Flask, React
        • AI/ML: TensorFlow, scikit-learn, HuggingFace
        • Tools: Git, Docker, Jupyter, Postman
        
        PROJECTS
        Real-time Analytics Pipeline
        • Built end-to-end data pipeline using Kafka, Spark, and Azure
        • Processed streaming data from multiple sources
        • Created interactive dashboards for business insights
        
        AI-Powered Job Recommendation System
        • Developed ML model for job-candidate matching
        • Used NLP techniques for resume and job description analysis
        • Achieved 85% accuracy in job recommendations
        """
        
        sections = [
            ResumeSection(section_name="Summary", content="Passionate Data Engineer with Master's in Computer Science from University of North Texas (GPA: 3.94). Experienced in building real-time data pipelines, scalable backend systems, and AI-powered applications.", order=1),
            ResumeSection(section_name="Experience", content="Data Engineering Intern - TechCorp (2023-2024)\n• Built real-time data pipelines using Apache Kafka and Spark\n• Developed ETL processes for processing 1M+ records daily\n• Implemented data quality monitoring and alerting systems\n\nSoftware Developer - StartupXYZ (2022-2023)\n• Developed backend APIs using Python and FastAPI\n• Optimized database queries resulting in 40% performance improvement\n• Implemented microservices architecture using Docker containers", order=2),
            ResumeSection(section_name="Education", content="Master of Science in Computer Science\nUniversity of North Texas - GPA: 3.94 (2022-2024)", order=3),
            ResumeSection(section_name="Skills", content="• Programming: Python, SQL, JavaScript, Go\n• Data Engineering: Apache Kafka, Apache Spark, ETL pipelines\n• Cloud: Microsoft Azure, AWS, PostgreSQL, MongoDB\n• Frameworks: FastAPI, Flask, React\n• AI/ML: TensorFlow, scikit-learn, HuggingFace\n• Tools: Git, Docker, Jupyter, Postman", order=4),
            ResumeSection(section_name="Projects", content="Real-time Analytics Pipeline\n• Built end-to-end data pipeline using Kafka, Spark, and Azure\n• Processed streaming data from multiple sources\n• Created interactive dashboards for business insights\n\nAI-Powered Job Recommendation System\n• Developed ML model for job-candidate matching\n• Used NLP techniques for resume and job description analysis\n• Achieved 85% accuracy in job recommendations", order=5)
        ]
        
        resume = Resume(
            id=f"sample_resume_{user_id}",
            user_id=user_id,
            title="Ashritha Battula - Data Engineer Resume",
            content=sample_content.strip(),
            sections=sections,
            skills=["Python", "SQL", "JavaScript", "Go", "Apache Kafka", "Apache Spark", "Microsoft Azure", "AWS", "FastAPI", "Flask", "React", "TensorFlow", "scikit-learn", "HuggingFace"],
            experience=[
                {
                    "company": "TechCorp",
                    "title": "Data Engineering Intern",
                    "description": "Built real-time data pipelines using Apache Kafka and Spark. Developed ETL processes for processing 1M+ records daily.",
                    "duration": "2023-2024"
                },
                {
                    "company": "StartupXYZ",
                    "title": "Software Developer",
                    "description": "Developed backend APIs using Python and FastAPI. Optimized database queries resulting in 40% performance improvement.",
                    "duration": "2022-2023"
                }
            ],
            education=[
                {
                    "institution": "University of North Texas",
                    "degree": "Master of Science in Computer Science",
                    "year": "2022-2024",
                    "gpa": "3.94"
                }
            ],
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        await self.save_resume(resume)
        return resume