import aiosmtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import Optional
from config import settings

logger = logging.getLogger(__name__)

# Service for sending emails with mockup attachments via SMTP"
class EmailService:

    def __init__(self):
        # Initialize SMTP configuration from settings
        self.smtp_server = settings.SMTP_SERVER
        self.smtp_user = settings.SMTP_USERNAME
        self.smtp_password = settings.SMTP_PASSWORD
        self.sender_email = settings.SENDER_EMAIL
        self.smtp_port = settings.SMTP_PORT

    async def send_mockup_email(self, recipient_email: str, image_data: bytes, image_filename: str, keyword: str, industry: str):
        # Send email with generated mockup image as attachment
        message = MIMEMultipart("alternative")
        message["Subject"] = f"PixelDuetWeb: Generator wizualizacji stron AI | '{keyword}'"
        message["From"] = self.sender_email
        message["To"] = recipient_email
        
        # HTML body
        html = f"""
                <html>
                            <body>
                                <h2>Your Website Mockup</h2>
                                <p>Hello,</p>
                                <p>We've generated a website mockup based on your request:</p>
                                <ul>
                                    <li><strong>Keyword:</strong> {keyword}</li>
                                    <li><strong>Industry:</strong> {industry}</li>
                                    <li><strong>Generated:</strong> Just now</li>
                                </ul>
                                
                                <h3>Your Mockup Preview:</h3>
                                <img src="cid:{image_filename}" alt="Website Mockup" style="max-width: 100%; height: auto;">
                                
                                <p>Best regards,<br>
                                Mockup Generator Team</p>
                            </body>
                        </html>
                """

        # Attach HTML content
        part = MIMEText(html, "html")
        message.attach(part)
        
        # Attach image file
        part = MIMEBase("application", "octet-stream")
        part.set_payload(image_data)
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {image_filename}"
        )
        message.attach(part)
        
        try:
            async with aiosmtplib.SMTP(
                hostname=self.smtp_server,
                port=self.smtp_port,
                use_tls=True
            ) as smtp:
                await smtp.login(self.smtp_user, self.smtp_password)
                await smtp.send_message(message)
            
            logger.info(f"Email sent successfully to: {recipient_email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email to {recipient_email}: {str(e)}")
            return False

email_service = EmailService()