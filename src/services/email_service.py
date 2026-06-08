import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()


class EmailService:
    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER", "mail.komtur.org")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.sender_email = os.getenv("SMTP_SENDER", "travelinfo@komtur.org")
        self.sender_password = os.getenv("SMTP_PASSWORD", "travelinfo")

    def send_travel_confirmation(self, recipient: str, subject: str, body: str, event_details: dict) -> str:
        ics_content = self._build_ics(event_details)
        if not ics_content:
            return "Failed to create calendar file."
        try:
            msg = MIMEMultipart()
            msg["From"] = self.sender_email
            msg["To"] = recipient
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain"))
            attachment = MIMEBase("text", "calendar")
            attachment.set_payload(ics_content)
            encoders.encode_base64(attachment)
            attachment.add_header("Content-Disposition", 'attachment; filename="travel_plan.ics"')
            msg.attach(attachment)
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            return "Travel confirmation email sent successfully."
        except Exception as exc:
            return f"Email could not be sent: {exc}"

    def _build_ics(self, event_details: dict) -> str | None:
        try:
            def clean(value):
                return str(value).replace("\\", "\\\\").replace("\n", "\\n").replace(",", "\\,").replace(";", "\\;")

            start = event_details["start"].replace("-", "").replace(":", "")
            end = event_details["end"].replace("-", "").replace(":", "")

            return "\n".join([
                "BEGIN:VCALENDAR",
                "VERSION:2.0",
                "PRODID:-//Smart Journey AI//Travel Assistant//EN",
                "BEGIN:VEVENT",
                f"SUMMARY:{clean(event_details.get('title', 'Travel Plan'))}",
                f"DTSTART:{start}",
                f"DTEND:{end}",
                f"LOCATION:{clean(event_details.get('location', ''))}",
                f"DESCRIPTION:{clean(event_details.get('description', ''))}",
                "END:VEVENT",
                "END:VCALENDAR",
            ])
        except Exception:
            return None
