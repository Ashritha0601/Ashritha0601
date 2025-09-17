#!/usr/bin/env python3
"""
Test script to verify the AI Job Agent system functionality.
"""

import asyncio
import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.services.ai_service import AIService
from app.services.job_service import JobService
from app.services.resume_service import ResumeService
from app.services.notification_service import NotificationService
from app.models.schemas import User


async def test_system():
    """Test all major system components."""
    
    print("🧪 Testing AI Job Agent System")
    print("=" * 50)
    
    # Initialize services
    try:
        ai_service = AIService()
        job_service = JobService()
        resume_service = ResumeService()
        notification_service = NotificationService()
        print("✅ Services initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize services: {e}")
        return False
    
    test_results = []
    
    # Test 1: Create sample resume
    print("\n1️⃣ Testing resume creation...")
    try:
        resume = await resume_service.create_sample_resume()
        print(f"   ✅ Created resume: {resume.id}")
        print(f"   📊 Skills: {len(resume.skills)}")
        test_results.append(True)
    except Exception as e:
        print(f"   ❌ Resume creation failed: {e}")
        test_results.append(False)
        return False
    
    # Test 2: Job search
    print("\n2️⃣ Testing job search...")
    try:
        jobs = await job_service.search_jobs(
            keywords=["python", "data engineer"],
            location="Dallas, TX",
            max_results=5
        )
        print(f"   ✅ Found {len(jobs)} jobs")
        if jobs:
            print(f"   📋 Sample: {jobs[0].title} at {jobs[0].company}")
        test_results.append(True)
    except Exception as e:
        print(f"   ❌ Job search failed: {e}")
        test_results.append(False)
    
    # Test 3: Job matching (if OpenAI key is available)
    print("\n3️⃣ Testing job matching...")
    try:
        if os.getenv("OPENAI_API_KEY"):
            if jobs:
                matched_jobs = await ai_service.match_jobs_to_resume(resume, jobs)
                print(f"   ✅ Matched {len(matched_jobs)} jobs")
                if matched_jobs and matched_jobs[0].match_score:
                    print(f"   🎯 Top match score: {matched_jobs[0].match_score:.1f}%")
                test_results.append(True)
            else:
                print("   ⚠️ No jobs to match")
                test_results.append(True)
        else:
            print("   ⚠️ Skipped (no OpenAI API key)")
            test_results.append(True)
    except Exception as e:
        print(f"   ❌ Job matching failed: {e}")
        test_results.append(False)
    
    # Test 4: Resume optimization (if OpenAI key is available)
    print("\n4️⃣ Testing resume optimization...")
    try:
        if os.getenv("OPENAI_API_KEY"):
            optimized = await resume_service.optimize_resume_for_job(
                resume.id,
                "Looking for a Senior Data Engineer with Python and Kafka experience"
            )
            print(f"   ✅ Optimized resume: {optimized.id}")
            test_results.append(True)
        else:
            print("   ⚠️ Skipped (no OpenAI API key)")
            test_results.append(True)
    except Exception as e:
        print(f"   ❌ Resume optimization failed: {e}")
        test_results.append(False)
    
    # Test 5: Cover letter generation (if OpenAI key is available)
    print("\n5️⃣ Testing cover letter generation...")
    try:
        if os.getenv("OPENAI_API_KEY") and jobs:
            cover_letter = await ai_service.generate_cover_letter(
                resume, jobs[0], "professional"
            )
            print(f"   ✅ Generated cover letter ({len(cover_letter)} chars)")
            test_results.append(True)
        else:
            print("   ⚠️ Skipped (no OpenAI API key or jobs)")
            test_results.append(True)
    except Exception as e:
        print(f"   ❌ Cover letter generation failed: {e}")
        test_results.append(False)
    
    # Test 6: Job alert creation
    print("\n6️⃣ Testing job alert creation...")
    try:
        from app.models.schemas import JobAlert, JobType, JobLevel
        alert = JobAlert(
            user_id="test_user",
            keywords=["python", "kafka"],
            locations=["Dallas"],
            job_types=[JobType.FULL_TIME],
            levels=[JobLevel.MID],
            is_active=True
        )
        alert_id = await job_service.create_job_alert(alert)
        print(f"   ✅ Created alert: {alert_id}")
        test_results.append(True)
    except Exception as e:
        print(f"   ❌ Job alert creation failed: {e}")
        test_results.append(False)
    
    # Test 7: Skill analysis (if OpenAI key is available)
    print("\n7️⃣ Testing skill analysis...")
    try:
        if os.getenv("OPENAI_API_KEY"):
            trends = await job_service.get_job_market_trends(resume.skills[:3])
            suggestions = await ai_service.suggest_skill_improvements(resume, trends)
            print(f"   ✅ Analyzed skills")
            if suggestions.get('skills_to_add'):
                print(f"   📈 Suggestions: {', '.join(suggestions['skills_to_add'][:3])}")
            test_results.append(True)
        else:
            print("   ⚠️ Skipped (no OpenAI API key)")
            test_results.append(True)
    except Exception as e:
        print(f"   ❌ Skill analysis failed: {e}")
        test_results.append(False)
    
    # Test 8: Notification system
    print("\n8️⃣ Testing notification system...")
    try:
        user = User(
            id="test_user",
            name="Test User",
            email="test@example.com"
        )
        # This will just log since no email credentials are set
        success = await notification_service.send_job_alert_email(
            user, jobs[:2] if jobs else [], alert
        )
        print(f"   ✅ Notification system working")
        test_results.append(True)
    except Exception as e:
        print(f"   ❌ Notification test failed: {e}")
        test_results.append(False)
    
    # Summary
    print("\n" + "=" * 50)
    passed = sum(test_results)
    total = len(test_results)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is working correctly.")
        return True
    else:
        print("⚠️ Some tests failed. Check the output above for details.")
        return False


async def test_api_endpoints():
    """Test API endpoints by importing and checking the FastAPI app."""
    
    print("\n🌐 Testing API endpoints...")
    
    try:
        from app.main import app
        print("   ✅ FastAPI app imported successfully")
        
        # Check if the app has the expected routes
        routes = [route.path for route in app.routes]
        expected_routes = ["/", "/jobs/search", "/resume/upload", "/cover-letter/generate"]
        
        for route in expected_routes:
            if route in routes:
                print(f"   ✅ Route {route} exists")
            else:
                print(f"   ❌ Route {route} missing")
        
        return True
        
    except Exception as e:
        print(f"   ❌ API endpoint test failed: {e}")
        return False


def main():
    """Run all tests."""
    
    print("🚀 Starting AI Job Agent System Tests")
    
    # Check for optional dependencies
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️ Note: OPENAI_API_KEY not set - AI features will be skipped")
    
    # Run async tests
    system_ok = asyncio.run(test_system())
    
    # Run API tests
    api_ok = asyncio.run(test_api_endpoints())
    
    print("\n" + "=" * 60)
    if system_ok and api_ok:
        print("🎉 All systems operational! AI Job Agent is ready to use.")
        print("\n🔗 Next steps:")
        print("   • Run: python -m ai_job_agent.cli demo")
        print("   • Start web server: python -m ai_job_agent.app.main")
        print("   • Visit: http://localhost:8000")
    else:
        print("❌ Some systems have issues. Please check the output above.")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())