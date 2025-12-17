import base64
import json
import os
import traceback
import functions_framework

def send_email(to_email, subject, message):
    """Send email using SMTP."""
    try:
        print(f"📧 Attempting to send email to: {to_email}")
        
        # Get credentials from environment
        gmail_user = os.getenv("GMAIL_USER")
        gmail_pass = os.getenv("GMAIL_PASS")
        
        if not gmail_user or not gmail_pass:
            raise ValueError("GMAIL_USER or GMAIL_PASS environment variables not set")
        
        # Email sending code
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        import smtplib
        
        msg = MIMEMultipart()
        msg["From"] = gmail_user
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(message, "plain"))
        
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(gmail_user, gmail_pass)
        server.sendmail(gmail_user, to_email, msg.as_string())
        server.quit()
        
        print("✅ Email sent successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send email: {str(e)}")
        traceback.print_exc()
        return False

@functions_framework.cloud_event
def pubsub_handler(cloud_event):
    """Cloud Event Function for Pub/Sub."""
    print("🚀 Cloud Function started!")
    print(f"📦 Event type: {type(cloud_event)}")
    print(f"📦 Event data: {cloud_event.data}")
    
    try:
        # Get data from cloud event
        data_dict = cloud_event.data if hasattr(cloud_event, 'data') else {}
        
        # For Pub/Sub messages, data is in data['message']['data']
        if isinstance(data_dict, dict) and 'message' in data_dict:
            message_data = data_dict['message']
            
            if 'data' in message_data:
                encoded_data = message_data['data']
                print(f"🔤 Encoded data: {encoded_data[:100]}...")
                
                # Decode from base64
                decoded_bytes = base64.b64decode(encoded_data)
                message_str = decoded_bytes.decode('utf-8')
                print(f"📩 Decoded message: {message_str}")
                
                # Parse JSON
                try:
                    data = json.loads(message_str)
                    print(f"📊 Parsed JSON data: {data}")
                except json.JSONDecodeError as e:
                    print(f"❌ JSON decode error: {e}")
                    return
                
                # Extract information
                event_type = data.get("event", "")
                filename = data.get("filename", "")
                
                print(f"📄 Filename: {filename}")
                print(f"🎯 Event type: {event_type}")
                
                # Determine subject and body
                if event_type == "upload":
                    subject = "✅ GCS File Uploaded"
                    body = f"File '{filename}' was uploaded successfully."
                elif event_type == "delete":
                    subject = "🗑️ GCS File Deleted"
                    body = f"File '{filename}' was deleted."
                elif event_type == "read":
                    subject = "📖 GCS File Read"
                    body = f"File '{filename}' was read/downloaded."
                else:
                    subject = "📢 GCS Event"
                    body = f"Event '{event_type}' occurred for file: {filename}"
                
                # Send email
                to_email = os.getenv("GMAIL_USER")
                if not to_email:
                    print("⚠ GMAIL_USER environment variable not set")
                    return
                
                email_sent = send_email(to_email, subject, body)
                
                if email_sent:
                    print("✅ Function completed successfully!")
                else:
                    print("❌ Function completed with errors")
        else:
            print("⚠ No valid Pub/Sub message found")
            
    except Exception as e:
        print(f"💥 Unexpected error: {str(e)}")
        traceback.print_exc()