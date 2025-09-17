#!/usr/bin/env python3
"""
Basic test script to verify the AI Job Agent system structure.
"""

import os
import sys
import json
from datetime import datetime

def test_project_structure():
    """Test that all required files and directories exist."""
    
    print("🧪 Testing AI Job Agent Project Structure")
    print("=" * 50)
    
    base_path = "/home/runner/work/Ashritha0601/Ashritha0601/ai_job_agent"
    
    # Required directories
    required_dirs = [
        "app",
        "app/models",
        "app/services", 
        "app/utils",
        "app/templates",
        "config",
        "data",
        "data/resumes",
        "data/templates"
    ]
    
    # Required files
    required_files = [
        "app/__init__.py",
        "app/main.py",
        "app/models/__init__.py",
        "app/models/schemas.py",
        "app/services/__init__.py",
        "app/services/ai_service.py",
        "app/services/job_service.py",
        "app/services/resume_service.py",
        "app/services/notification_service.py",
        "app/utils/__init__.py",
        "app/utils/helpers.py",
        "app/templates/__init__.py",
        "app/templates/cover_letter_templates.py",
        "config/settings.py",
        "cli.py",
        "README.md"
    ]
    
    all_good = True
    
    # Check directories
    print("\n📁 Checking directories...")
    for dir_path in required_dirs:
        full_path = os.path.join(base_path, dir_path)
        if os.path.exists(full_path) and os.path.isdir(full_path):
            print(f"   ✅ {dir_path}")
        else:
            print(f"   ❌ {dir_path} - Missing directory")
            all_good = False
    
    # Check files
    print("\n📄 Checking files...")
    for file_path in required_files:
        full_path = os.path.join(base_path, file_path)
        if os.path.exists(full_path) and os.path.isfile(full_path):
            size = os.path.getsize(full_path)
            print(f"   ✅ {file_path} ({size} bytes)")
        else:
            print(f"   ❌ {file_path} - Missing file")
            all_good = False
    
    return all_good


def test_file_contents():
    """Test that key files have expected content."""
    
    print("\n📖 Testing file contents...")
    
    base_path = "/home/runner/work/Ashritha0601/Ashritha0601/ai_job_agent"
    
    # Test main.py for FastAPI app
    main_path = os.path.join(base_path, "app/main.py")
    try:
        with open(main_path, 'r') as f:
            content = f.read()
            if "FastAPI" in content and "@app.get" in content:
                print("   ✅ main.py contains FastAPI app")
            else:
                print("   ❌ main.py missing FastAPI components")
                return False
    except Exception as e:
        print(f"   ❌ Error reading main.py: {e}")
        return False
    
    # Test schemas.py for Pydantic models
    schemas_path = os.path.join(base_path, "app/models/schemas.py")
    try:
        with open(schemas_path, 'r') as f:
            content = f.read()
            if "BaseModel" in content and "Job" in content and "Resume" in content:
                print("   ✅ schemas.py contains Pydantic models")
            else:
                print("   ❌ schemas.py missing expected models")
                return False
    except Exception as e:
        print(f"   ❌ Error reading schemas.py: {e}")
        return False
    
    # Test CLI
    cli_path = os.path.join(base_path, "cli.py")
    try:
        with open(cli_path, 'r') as f:
            content = f.read()
            if "click" in content and "@cli.command" in content:
                print("   ✅ cli.py contains Click CLI interface")
            else:
                print("   ❌ cli.py missing CLI components")
                return False
    except Exception as e:
        print(f"   ❌ Error reading cli.py: {e}")
        return False
    
    return True


def test_data_creation():
    """Test creating sample data without external dependencies."""
    
    print("\n📊 Testing data creation...")
    
    base_path = "/home/runner/work/Ashritha0601/Ashritha0601/ai_job_agent"
    
    # Test creating a sample resume JSON
    try:
        sample_resume = {
            "id": "test_resume_001",
            "user_id": "test_user",
            "title": "Test Resume",
            "content": "Sample resume content for testing",
            "sections": [
                {
                    "section_name": "Summary",
                    "content": "Experienced developer",
                    "order": 1
                }
            ],
            "skills": ["Python", "FastAPI", "Data Engineering"],
            "experience": [
                {
                    "company": "Test Corp",
                    "title": "Developer",
                    "description": "Built cool stuff",
                    "duration": "2022-2024"
                }
            ],
            "education": [
                {
                    "institution": "Test University",
                    "degree": "CS Degree", 
                    "year": "2022",
                    "gpa": "3.8"
                }
            ],
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        # Ensure data directory exists
        data_dir = os.path.join(base_path, "data/resumes")
        os.makedirs(data_dir, exist_ok=True)
        
        # Save sample resume
        resume_path = os.path.join(data_dir, "test_resume.json")
        with open(resume_path, 'w') as f:
            json.dump(sample_resume, f, indent=2)
        
        print(f"   ✅ Created sample resume: {resume_path}")
        
        # Verify it can be read back
        with open(resume_path, 'r') as f:
            loaded = json.load(f)
            if loaded["id"] == sample_resume["id"]:
                print("   ✅ Sample resume can be loaded successfully")
            else:
                print("   ❌ Sample resume data corrupted")
                return False
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error creating sample data: {e}")
        return False


def test_configuration():
    """Test configuration files."""
    
    print("\n⚙️ Testing configuration...")
    
    base_path = "/home/runner/work/Ashritha0601/Ashritha0601"
    
    # Check .env.example
    env_example_path = os.path.join(base_path, ".env.example")
    if os.path.exists(env_example_path):
        with open(env_example_path, 'r') as f:
            content = f.read()
            if "OPENAI_API_KEY" in content and "EMAIL_" in content:
                print("   ✅ .env.example contains required settings")
            else:
                print("   ❌ .env.example missing key settings")
                return False
    else:
        print("   ❌ .env.example not found")
        return False
    
    # Check requirements.txt
    req_path = os.path.join(base_path, "requirements.txt")
    if os.path.exists(req_path):
        with open(req_path, 'r') as f:
            content = f.read()
            if "fastapi" in content.lower() and "openai" in content.lower():
                print("   ✅ requirements.txt contains required packages")
            else:
                print("   ❌ requirements.txt missing key packages")
                return False
    else:
        print("   ❌ requirements.txt not found")
        return False
    
    return True


def test_documentation():
    """Test documentation quality."""
    
    print("\n📚 Testing documentation...")
    
    # Main README
    main_readme = "/home/runner/work/Ashritha0601/Ashritha0601/README.md"
    if os.path.exists(main_readme):
        with open(main_readme, 'r') as f:
            content = f.read()
            if len(content) > 1000:  # Basic content check
                print("   ✅ Main README.md exists and has content")
            else:
                print("   ⚠️ Main README.md is quite short")
    
    # AI Job Agent README
    agent_readme = "/home/runner/work/Ashritha0601/Ashritha0601/ai_job_agent/README.md"
    if os.path.exists(agent_readme):
        with open(agent_readme, 'r') as f:
            content = f.read()
            if "AI Job Agent" in content and "Features" in content and "Installation" in content:
                print("   ✅ AI Job Agent README.md is comprehensive")
                return True
            else:
                print("   ❌ AI Job Agent README.md missing key sections")
                return False
    else:
        print("   ❌ AI Job Agent README.md not found")
        return False


def main():
    """Run all basic tests."""
    
    print("🚀 Starting AI Job Agent Basic Tests")
    print("(Testing project structure without external dependencies)")
    
    tests = [
        ("Project Structure", test_project_structure),
        ("File Contents", test_file_contents),
        ("Data Creation", test_data_creation),
        ("Configuration", test_configuration),
        ("Documentation", test_documentation)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name} test...")
        try:
            result = test_func()
            results.append(result)
            if result:
                print(f"✅ {test_name} test passed")
            else:
                print(f"❌ {test_name} test failed")
        except Exception as e:
            print(f"❌ {test_name} test error: {e}")
            results.append(False)
    
    # Summary
    print("\n" + "=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All basic tests passed! Project structure is correct.")
        print("\n🔗 Next steps:")
        print("   • Install dependencies: pip install -r requirements.txt")
        print("   • Set up .env file with your API keys")
        print("   • Run: python -m ai_job_agent.cli demo")
        print("   • Start web server: python -m ai_job_agent.app.main")
        return 0
    else:
        print("⚠️ Some tests failed. Check the output above for details.")
        return 1


if __name__ == "__main__":
    exit(main())