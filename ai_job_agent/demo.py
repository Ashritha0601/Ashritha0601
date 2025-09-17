#!/usr/bin/env python3
"""
Demo script for AI Job Agent - works without external dependencies.
"""

import json
import os
from datetime import datetime


def create_sample_data():
    """Create sample data for demonstration."""
    
    print("📊 Creating sample data...")
    
    # Sample resume data
    resume_data = {
        "id": "demo_resume_001",
        "user_id": "demo_user",
        "title": "Ashritha Battula - Data Engineer Resume",
        "content": """
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
        """.strip(),
        "skills": ["Python", "SQL", "JavaScript", "Go", "Apache Kafka", "Apache Spark", 
                  "Microsoft Azure", "AWS", "FastAPI", "Flask", "React", "TensorFlow"],
        "experience": [
            {
                "company": "TechCorp",
                "title": "Data Engineering Intern",
                "description": "Built real-time data pipelines using Apache Kafka and Spark",
                "duration": "2023-2024"
            }
        ],
        "education": [
            {
                "institution": "University of North Texas",
                "degree": "Master of Science in Computer Science",
                "year": "2022-2024",
                "gpa": "3.94"
            }
        ],
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    
    # Sample job data
    job_data = [
        {
            "id": "job_001",
            "title": "Senior Data Engineer",
            "company": "TechCorp Inc.",
            "location": "Dallas, TX",
            "job_type": "full_time",
            "level": "senior",
            "description": "We are seeking a Senior Data Engineer with expertise in Apache Kafka, Spark, and cloud technologies.",
            "requirements": ["5+ years experience", "Python", "Kafka", "Spark", "Cloud platforms"],
            "salary_range": "$120,000 - $160,000",
            "application_url": "https://example.com/job/1",
            "match_score": 92.5
        },
        {
            "id": "job_002", 
            "title": "Machine Learning Engineer",
            "company": "AI Solutions Ltd.",
            "location": "Austin, TX",
            "job_type": "full_time",
            "level": "mid",
            "description": "Join our ML team to build cutting-edge AI applications.",
            "requirements": ["3+ years ML experience", "Python", "TensorFlow", "MLOps"],
            "salary_range": "$90,000 - $130,000",
            "application_url": "https://example.com/job/2",
            "match_score": 88.0
        }
    ]
    
    # Save data
    os.makedirs("data/resumes", exist_ok=True)
    os.makedirs("data/jobs", exist_ok=True)
    
    with open("data/resumes/demo_resume.json", "w") as f:
        json.dump(resume_data, f, indent=2)
    
    with open("data/jobs/demo_jobs.json", "w") as f:
        json.dump(job_data, f, indent=2)
    
    print("✅ Sample data created successfully!")
    return resume_data, job_data


def demonstrate_job_matching(resume_data, job_data):
    """Demonstrate job matching logic."""
    
    print("\n🎯 Demonstrating Job Matching...")
    
    resume_skills = set(skill.lower() for skill in resume_data["skills"])
    
    for job in job_data:
        # Simple matching based on skill overlap
        job_requirements = set(req.lower() for req in job["requirements"])
        
        # Calculate overlap
        overlap = resume_skills.intersection(job_requirements)
        match_percentage = (len(overlap) / len(job_requirements)) * 100 if job_requirements else 0
        
        print(f"\n📋 {job['title']} at {job['company']}")
        print(f"   📍 {job['location']}")
        print(f"   💰 {job['salary_range']}")
        print(f"   🎯 Match Score: {match_percentage:.1f}%")
        print(f"   🔗 {job['application_url']}")
        
        if overlap:
            print(f"   ✅ Matching Skills: {', '.join(overlap)}")


def demonstrate_resume_optimization(resume_data, target_job):
    """Demonstrate resume optimization."""
    
    print(f"\n🔧 Optimizing Resume for: {target_job['title']}")
    
    # Simulate optimization by highlighting relevant skills
    relevant_skills = []
    for skill in resume_data["skills"]:
        if any(skill.lower() in req.lower() for req in target_job["requirements"]):
            relevant_skills.append(skill)
    
    print("✅ Optimization Complete!")
    print(f"   🎯 Highlighted Skills: {', '.join(relevant_skills)}")
    print(f"   📈 Tailored for: {target_job['company']}")
    print("   💡 Added relevant keywords from job description")


def demonstrate_cover_letter_generation(resume_data, target_job):
    """Demonstrate cover letter generation."""
    
    print(f"\n📝 Generating Cover Letter for: {target_job['title']}")
    
    cover_letter = f"""
Dear Hiring Manager,

I am writing to express my strong interest in the {target_job['title']} position at {target_job['company']}. With my background in data engineering and experience with Python, Kafka, and Spark, I am confident that I would be a valuable addition to your team.

In my recent role as a Data Engineering Intern at TechCorp, I built real-time data pipelines using Apache Kafka and Spark, processing over 1M records daily. This experience directly aligns with your requirements for expertise in these technologies.

I am particularly excited about {target_job['company']}'s innovative approach to data engineering and would love to contribute to your team's success.

Thank you for considering my application. I look forward to discussing how my skills and experience can benefit {target_job['company']}.

Sincerely,
Ashritha Battula
    """.strip()
    
    print("✅ Cover Letter Generated!")
    print(f"   📄 Length: {len(cover_letter)} characters")
    print("   🎨 Tone: Professional")
    print("   📋 Customized for specific job and company")
    
    # Save cover letter
    os.makedirs("data/cover_letters", exist_ok=True)
    filename = f"cover_letter_{target_job['company'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.txt"
    with open(f"data/cover_letters/{filename}", "w") as f:
        f.write(cover_letter)
    
    print(f"   💾 Saved as: {filename}")


def demonstrate_skill_analysis(resume_data):
    """Demonstrate skill gap analysis."""
    
    print("\n📊 Analyzing Skills and Market Trends...")
    
    current_skills = resume_data["skills"]
    
    # Mock trending skills
    trending_skills = [
        "Kubernetes", "Docker", "Terraform", "Snowflake", 
        "dbt", "Airflow", "Apache Beam", "GCP BigQuery"
    ]
    
    # Find skill gaps
    skill_gaps = [skill for skill in trending_skills if skill not in current_skills]
    
    print("✅ Skill Analysis Complete!")
    print(f"   🛠️ Current Skills: {len(current_skills)}")
    print(f"   📈 Trending Skills You Should Learn: {', '.join(skill_gaps[:4])}")
    print("   🏆 Recommended Certifications:")
    print("      • AWS Certified Data Engineer")
    print("      • Azure Data Engineer Associate")
    print("      • Google Cloud Professional Data Engineer")


def demonstrate_job_alerts():
    """Demonstrate job alert functionality."""
    
    print("\n🔔 Setting Up Job Alerts...")
    
    alert_config = {
        "id": "alert_001",
        "user_id": "demo_user",
        "keywords": ["data engineer", "python", "kafka"],
        "locations": ["Dallas", "Austin", "Remote"],
        "job_types": ["full_time", "remote"],
        "salary_min": 80000,
        "is_active": True,
        "created_at": datetime.now().isoformat()
    }
    
    os.makedirs("data/alerts", exist_ok=True)
    with open("data/alerts/demo_alert.json", "w") as f:
        json.dump(alert_config, f, indent=2)
    
    print("✅ Job Alert Created!")
    print(f"   🔍 Keywords: {', '.join(alert_config['keywords'])}")
    print(f"   📍 Locations: {', '.join(alert_config['locations'])}")
    print(f"   💰 Min Salary: ${alert_config['salary_min']:,}")
    print("   📧 Email notifications will be sent for new matches")


def main():
    """Run the complete AI Job Agent demo."""
    
    print("🤖 AI Job Agent - Complete System Demo")
    print("=" * 60)
    print("This demo showcases all AI Job Agent features without external dependencies.\n")
    
    # Create sample data
    resume_data, job_data = create_sample_data()
    
    # Demonstrate core features
    demonstrate_job_matching(resume_data, job_data)
    demonstrate_resume_optimization(resume_data, job_data[0])
    demonstrate_cover_letter_generation(resume_data, job_data[0])
    demonstrate_skill_analysis(resume_data)
    demonstrate_job_alerts()
    
    print("\n" + "=" * 60)
    print("🎉 Demo Complete! AI Job Agent Features Demonstrated:")
    print("   ✅ Job Search and Matching")
    print("   ✅ Resume Optimization")
    print("   ✅ Cover Letter Generation")
    print("   ✅ Skills Gap Analysis")
    print("   ✅ Job Alert System")
    
    print("\n🔗 Next Steps:")
    print("   • Install dependencies: pip install -r requirements.txt")
    print("   • Add OpenAI API key for AI features")
    print("   • Run web interface: python -m app.main")
    print("   • Use CLI: python cli.py --help")
    
    print(f"\n📊 Files created in demo:")
    print("   • data/resumes/demo_resume.json")
    print("   • data/jobs/demo_jobs.json") 
    print("   • data/cover_letters/ (cover letter files)")
    print("   • data/alerts/demo_alert.json")


if __name__ == "__main__":
    main()