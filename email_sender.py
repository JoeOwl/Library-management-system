import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email_validator import validate_email, EmailNotValidError
from datetime import datetime

class EmailSender:
    def __init__(self):
        self.sender_email = "mohmad.walid.m4.555@gmail.com"  # Corrected domain
        self.sender_password = "mw632221mwm4mw555125"
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587

    def send_email(self, student, book, issue_time, end_time):
        try:
            receiver_email = student[3]

            # Email details
            subject = f"Book Issued: {book[1]}"

            # Email body
            body = f"""
            Dear {student[1]},\n
            The following book has been issued to you:\n
            Student Details:
            - ID: {student[0]}
            - Name: {student[1]}
            - Class: {student[2]}
            - Email: {student[3]}\n
            Book Details:
            - ID: {book[0]}
            - Title: {book[1]}
            - Author: {book[2]}
            - Price: ${book[3]:.2f}
            - Issue Time: {issue_time.strftime('%Y-%m-%d %H:%M:%S')}
            - Due Time: {end_time.strftime('%Y-%m-%d %H:%M:%S')}\n
            Please return the book on time to avoid penalties.
            Regards,
            Library Management System
            """

            # Email message
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = receiver_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

            # SMTP server setup
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            server.send_message(msg)
            server.quit()

            print("Email sent successfully!")

        except EmailNotValidError as e:
            print(f"Invalid email address: {e}")
        except Exception as e:
            print(f"Failed to send email: {e}")