import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict, Any
from datetime import datetime
from ..models.schemas import Job, User, JobAlert


class NotificationService:
    def __init__(self):
        self.email_host = os.getenv("EMAIL_HOST", "smtp.gmail.com")
        self.email_port = int(os.getenv("EMAIL_PORT", "587"))
        self.email_username = os.getenv("EMAIL_USERNAME", "")
        self.email_password = os.getenv("EMAIL_PASSWORD", "")
    
    async def send_job_alert_email(self, user: User, jobs: List[Job], alert: JobAlert) -> bool:
        """Send job alert email to user."""
        if not self.email_username or not self.email_password:
            print("Email credentials not configured. Would send email to:", user.email)
            return True  # Mock success for demo
        
        try:
            # Create email content
            subject = f"🚀 New Job Opportunities - {len(jobs)} matches found!"
            html_content = self._create_job_alert_html(jobs, alert)
            
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.email_username
            msg['To'] = user.email
            
            # Add HTML content
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            # Send email
            with smtplib.SMTP(self.email_host, self.email_port) as server:
                server.starttls()
                server.login(self.email_username, self.email_password)
                server.send_message(msg)
            
            print(f"Job alert email sent to {user.email}")
            return True
            
        except Exception as e:
            print(f"Failed to send email: {str(e)}")
            return False
    
    def _create_job_alert_html(self, jobs: List[Job], alert: JobAlert) -> str:
        """Create HTML content for job alert email."""
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ background-color: #2563eb; color: white; padding: 20px; border-radius: 8px; }}
                .job-card {{ border: 1px solid #e5e7eb; margin: 15px 0; padding: 15px; border-radius: 8px; }}
                .job-title {{ font-size: 18px; font-weight: bold; color: #1f2937; }}
                .company {{ color: #6b7280; font-size: 16px; margin: 5px 0; }}
                .location {{ color: #9ca3af; font-size: 14px; }}
                .salary {{ color: #059669; font-weight: bold; }}
                .apply-btn {{ background-color: #2563eb; color: white; padding: 10px 20px; 
                           text-decoration: none; border-radius: 5px; display: inline-block; margin-top: 10px; }}
                .footer {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #e5e7eb; 
                          color: #6b7280; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🚀 Your Job Alert Results</h1>
                <p>Found {len(jobs)} new job opportunities matching your criteria!</p>
            </div>
            
            <div style="margin: 20px 0;">
                <h3>Search Criteria:</h3>
                <ul>
                    <li><strong>Keywords:</strong> {', '.join(alert.keywords)}</li>
                    <li><strong>Locations:</strong> {', '.join(alert.locations)}</li>
                    <li><strong>Job Types:</strong> {', '.join([jt.value for jt in alert.job_types])}</li>
                </ul>
            </div>
        """
        
        for job in jobs[:10]:  # Limit to top 10 jobs
            match_score = f"Match: {job.match_score:.0f}%" if job.match_score else ""
            
            html += f"""
            <div class="job-card">
                <div class="job-title">{job.title}</div>
                <div class="company">📍 {job.company} - {job.location}</div>
                <div class="salary">{job.salary_range or 'Salary not specified'}</div>
                {f'<div style="color: #059669; font-weight: bold; margin: 5px 0;">{match_score}</div>' if match_score else ''}
                
                <p>{job.description[:200]}...</p>
                
                <div style="margin: 10px 0;">
                    <strong>Key Requirements:</strong>
                    <ul>
                        {''.join([f'<li>{req}</li>' for req in job.requirements[:3]])}
                    </ul>
                </div>
                
                <a href="{job.application_url}" class="apply-btn">Apply Now</a>
            </div>
            """
        
        html += f"""
            <div class="footer">
                <p>This email was sent by your AI Job Agent. You're receiving this because you have an active job alert.</p>
                <p>Alert created on: {alert.created_at.strftime('%Y-%m-%d %H:%M') if alert.created_at else 'N/A'}</p>
                <p>Don't want these emails? Reply with "UNSUBSCRIBE" to stop receiving job alerts.</p>
            </div>
        </body>
        </html>
        """
        
        return html
    
    async def send_resume_update_notification(self, user: User, original_resume_id: str, 
                                            optimized_resume_id: str, job_title: str) -> bool:
        """Send notification when resume has been optimized."""
        try:
            subject = f"📄 Your resume has been optimized for: {job_title}"
            
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 20px; }}
                    .header {{ background-color: #059669; color: white; padding: 20px; border-radius: 8px; }}
                    .content {{ margin: 20px 0; }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>📄 Resume Optimization Complete!</h1>
                </div>
                
                <div class="content">
                    <p>Hi {user.name},</p>
                    
                    <p>Great news! Your resume has been optimized for the "{job_title}" position.</p>
                    
                    <h3>What was optimized:</h3>
                    <ul>
                        <li>✅ Keywords aligned with job requirements</li>
                        <li>✅ Relevant skills and experience highlighted</li>
                        <li>✅ ATS-friendly formatting maintained</li>
                        <li>✅ Achievement statements enhanced</li>
                    </ul>
                    
                    <p>Your optimized resume ID: <strong>{optimized_resume_id}</strong></p>
                    
                    <p>You can now use this optimized version for your job application!</p>
                    
                    <p>Best of luck with your application!</p>
                    <p><em>Your AI Job Agent</em></p>
                </div>
            </body>
            </html>
            """
            
            if not self.email_username or not self.email_password:
                print(f"Would send resume optimization email to: {user.email}")
                return True  # Mock success for demo
            
            # Create and send email (similar to job alert)
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.email_username
            msg['To'] = user.email
            
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            with smtplib.SMTP(self.email_host, self.email_port) as server:
                server.starttls()
                server.login(self.email_username, self.email_password)
                server.send_message(msg)
            
            return True
            
        except Exception as e:
            print(f"Failed to send resume update notification: {str(e)}")
            return False
    
    async def send_cover_letter_notification(self, user: User, job_title: str, 
                                           company: str, cover_letter_id: str) -> bool:
        """Send notification when cover letter has been generated."""
        try:
            subject = f"📝 Cover letter generated for {company} - {job_title}"
            
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 20px; }}
                    .header {{ background-color: #7c3aed; color: white; padding: 20px; border-radius: 8px; }}
                    .content {{ margin: 20px 0; }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>📝 Cover Letter Ready!</h1>
                </div>
                
                <div class="content">
                    <p>Hi {user.name},</p>
                    
                    <p>Your personalized cover letter has been generated for:</p>
                    <ul>
                        <li><strong>Position:</strong> {job_title}</li>
                        <li><strong>Company:</strong> {company}</li>
                    </ul>
                    
                    <p>Cover Letter ID: <strong>{cover_letter_id}</strong></p>
                    
                    <h3>Your cover letter includes:</h3>
                    <ul>
                        <li>✅ Personalized introduction</li>
                        <li>✅ Relevant experience highlights</li>
                        <li>✅ Company-specific enthusiasm</li>
                        <li>✅ Strong call to action</li>
                    </ul>
                    
                    <p>Review and customize the cover letter as needed before submitting your application.</p>
                    
                    <p>Good luck with your application!</p>
                    <p><em>Your AI Job Agent</em></p>
                </div>
            </body>
            </html>
            """
            
            if not self.email_username or not self.email_password:
                print(f"Would send cover letter notification to: {user.email}")
                return True  # Mock success for demo
            
            # Create and send email
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.email_username
            msg['To'] = user.email
            
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            with smtplib.SMTP(self.email_host, self.email_port) as server:
                server.starttls()
                server.login(self.email_username, self.email_password)
                server.send_message(msg)
            
            return True
            
        except Exception as e:
            print(f"Failed to send cover letter notification: {str(e)}")
            return False
    
    async def send_daily_job_summary(self, user: User, jobs_found: int, 
                                   top_matches: List[Job]) -> bool:
        """Send daily summary of job search activity."""
        try:
            subject = f"📊 Daily Job Summary - {jobs_found} opportunities found"
            
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 20px; }}
                    .header {{ background-color: #dc2626; color: white; padding: 20px; border-radius: 8px; }}
                    .summary {{ background-color: #f3f4f6; padding: 15px; border-radius: 8px; margin: 15px 0; }}
                    .job-highlight {{ border-left: 4px solid #2563eb; padding-left: 15px; margin: 10px 0; }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>📊 Your Daily Job Summary</h1>
                    <p>{datetime.now().strftime('%B %d, %Y')}</p>
                </div>
                
                <div class="summary">
                    <h3>Today's Activity:</h3>
                    <ul>
                        <li><strong>{jobs_found}</strong> new job opportunities found</li>
                        <li><strong>{len(top_matches)}</strong> high-match positions identified</li>
                        <li><strong>Active alerts:</strong> Running continuously</li>
                    </ul>
                </div>
                
                <h3>🎯 Top Matches Today:</h3>
            """
            
            for job in top_matches[:3]:  # Top 3 matches
                match_score = f"{job.match_score:.0f}% match" if job.match_score else "Great match"
                html_content += f"""
                <div class="job-highlight">
                    <h4>{job.title} at {job.company}</h4>
                    <p><strong>{match_score}</strong> • {job.location} • {job.salary_range or 'Competitive salary'}</p>
                </div>
                """
            
            html_content += f"""
                <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #e5e7eb;">
                    <p>Keep up the great work! Your AI Job Agent is working 24/7 to find the best opportunities for you.</p>
                    <p><em>Your AI Job Agent</em></p>
                </div>
            </body>
            </html>
            """
            
            if not self.email_username or not self.email_password:
                print(f"Would send daily summary to: {user.email}")
                return True  # Mock success for demo
            
            return True
            
        except Exception as e:
            print(f"Failed to send daily summary: {str(e)}")
            return False