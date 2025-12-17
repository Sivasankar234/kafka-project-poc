from notification.email_service import EmailService

email = EmailService()

print(email.send_email(
    to_email="your_target_email@gmail.com",
    subject="GCS Notification",
    message="File uploaded successfully!"
))
