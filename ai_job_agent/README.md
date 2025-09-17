# 🤖 AI Job Agent

An intelligent system for job searching, resume optimization, and cover letter generation, built specifically for data engineers and tech professionals.

## ✨ Features

- **🔍 Intelligent Job Search**: Find jobs that match your skills and experience
- **📄 Resume Optimization**: AI-powered resume optimization for specific job postings
- **📝 Cover Letter Generation**: Generate personalized cover letters with different tones
- **🔔 Job Alerts**: Automated job monitoring with email notifications
- **📊 Skills Analysis**: Get recommendations for skill improvements based on market trends
- **🎯 Job Matching**: AI-powered matching algorithm to find the best opportunities

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- OpenAI API key (optional, for AI features)
- Email credentials (optional, for notifications)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai_job_agent
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

4. **Run the demo**
   ```bash
   python -m ai_job_agent.cli demo
   ```

### Web Interface

Start the FastAPI server:
```bash
cd ai_job_agent
python -m app.main
```

Then visit http://localhost:8000 to access the web interface and API documentation.

### CLI Interface

The system includes a comprehensive command-line interface:

```bash
# Search for jobs
python -m ai_job_agent.cli search-jobs -k "data engineer" -k "python" -l "Dallas, TX"

# Upload and parse resume
python -m ai_job_agent.cli upload-resume -f /path/to/resume.pdf

# Generate cover letter
python -m ai_job_agent.cli generate-cover-letter -r resume_id -t "Data Engineer" -c "TechCorp"

# Create job alert
python -m ai_job_agent.cli create-alert -k "python" -k "kafka" -l "Dallas" -l "Austin"

# Check job alerts
python -m ai_job_agent.cli check-alerts

# Analyze skills
python -m ai_job_agent.cli analyze-skills -r resume_id

# Run complete demo
python -m ai_job_agent.cli demo
```

## 📊 API Endpoints

### Core Endpoints

- `GET /` - Welcome page with feature overview
- `GET /docs` - Interactive API documentation
- `POST /jobs/search` - Search for jobs with matching
- `POST /resume/upload` - Upload and parse resume
- `POST /resume/optimize` - Optimize resume for specific job
- `POST /cover-letter/generate` - Generate personalized cover letter
- `POST /alerts/create` - Create job alert
- `GET /alerts/check/{user_id}` - Check job alerts
- `GET /demo/run` - Run complete system demo

### Example API Usage

```python
import requests

# Search for jobs
response = requests.post("http://localhost:8000/jobs/search", json={
    "resume_id": "sample_resume_user_001",
    "location_preferences": ["Dallas, TX"],
    "max_results": 10
})

jobs = response.json()
```

## 🛠️ Configuration

The system uses environment variables for configuration. Key settings include:

```env
# OpenAI API for AI features
OPENAI_API_KEY=your_openai_api_key

# Email for notifications
EMAIL_USERNAME=your_email@gmail.com
EMAIL_PASSWORD=your_app_password

# User profile
USER_EMAIL=work.ashrithabattula@gmail.com
USER_NAME=Ashritha Battula
```

## 📁 Project Structure

```
ai_job_agent/
├── app/
│   ├── main.py              # FastAPI application
│   ├── models/
│   │   └── schemas.py       # Pydantic models
│   ├── services/
│   │   ├── ai_service.py    # AI/ML operations
│   │   ├── job_service.py   # Job search logic
│   │   ├── resume_service.py # Resume processing
│   │   └── notification_service.py # Email notifications
│   ├── utils/
│   │   └── helpers.py       # Utility functions
│   └── templates/
│       └── cover_letter_templates.py # Cover letter templates
├── config/
│   └── settings.py          # Configuration management
├── data/
│   ├── resumes/            # Stored resumes
│   └── templates/          # Document templates
├── cli.py                  # Command-line interface
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🎯 Use Cases

### For Job Seekers

1. **Resume Optimization**: Upload your resume and optimize it for specific job postings
2. **Job Discovery**: Find relevant opportunities based on your skills and preferences
3. **Application Materials**: Generate tailored cover letters for each application
4. **Market Intelligence**: Get insights on trending skills and market demands

### For Career Development

1. **Skills Gap Analysis**: Identify areas for professional growth
2. **Market Trends**: Stay updated on industry requirements
3. **Certification Recommendations**: Get suggestions for valuable certifications
4. **Career Progression**: Plan your next career moves strategically

## 🔧 Advanced Features

### Custom AI Prompts

The system uses sophisticated AI prompts for:
- Resume analysis and optimization
- Job matching algorithms
- Cover letter personalization
- Skills gap analysis

### Email Notifications

Automated email notifications for:
- New job matches
- Resume optimization completion
- Cover letter generation
- Daily job summaries

### Data Processing

- PDF and DOCX resume parsing
- Text extraction and analysis
- Skills identification
- Experience parsing

## 🧪 Testing

The system includes sample data for testing:

```bash
# Run the demo to see all features
python -m ai_job_agent.cli demo

# Test individual components
python -m ai_job_agent.cli search-jobs -k "python" -l "Dallas"
```

## 🔒 Privacy & Security

- All data is stored locally
- No personal information is shared with external services (except configured APIs)
- Resumes and personal data are encrypted at rest
- API keys and credentials are stored securely in environment variables

## 📈 Future Enhancements

- Integration with major job boards (LinkedIn, Indeed, Glassdoor)
- Advanced ML models for better job matching
- Interview preparation assistance
- Salary negotiation guidance
- Career path recommendations
- Portfolio and project showcase

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙋‍♀️ About

Created by **Ashritha Battula**, a Data Engineer and AI/ML Enthusiast passionate about building intelligent systems that help people advance their careers.

- 📧 Email: work.ashrithabattula@gmail.com
- 💼 LinkedIn: [ashrithabattula](https://linkedin.com/in/ashrithabattula/)
- 🎓 Master's in Computer Science, University of North Texas

---

*Made with ❤️ for the tech community*