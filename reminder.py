import pandas as pd
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# ======================
# EMAIL CONFIG (FROM GITHUB SECRETS)
# ======================
SENDER_EMAIL = os.environ["EMAIL_USER"]
APP_PASSWORD = os.environ["EMAIL_PASS"]

# ======================
# SEND EMAIL FUNCTION
# ======================
def send_email(to_email, subject, html_body):
    msg = MIMEMultipart("alternative")
    msg["From"] = SENDER_EMAIL
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(msg)


# ======================
# READ EVENTS FILE
# ======================
df = pd.read_csv("events.csv")
today = datetime.today().date()

print("Today's date:", today)
print("-" * 50)


# ======================
# SUGGESTION ENGINE
# ======================
def get_suggestion(event_type):
    event_type = str(event_type).lower()

    if event_type == "birthday":
        return "🎁 Consider a thoughtful gift and a handwritten note"
    elif event_type == "anniversary":
        return "🍽️ Plan a meaningful dinner or quality time together"
    elif event_type == "goal":
        return "🚀 Stay consistent — you're close to your milestone!"
    else:
        return "✨ Take a moment to do something meaningful"


# ======================
# REMINDER LOGIC
# ======================
for _, row in df.iterrows():

    event_date = datetime.strptime(str(row["event_date"]).strip(), "%Y-%m-%d").date()
    days_left = (event_date - today).days

    print(f"{row['event_name']} -> days_left = {days_left}")

    # -------------------------------------------------
    # Decide whether to send reminder
    # -------------------------------------------------

    if days_left == 0:
        subject = f"🎉 Today: {row['event_name']}!"
        message_line = f"{row['event_name']} is TODAY! 🎉"

    elif days_left in [30, 15] or 1 <= days_left <= 7:
        subject = f"🔔 Reminder: {row['event_name']} in {days_left} day(s)"
        message_line = f"{row['event_name']} is coming in {days_left} day(s)."

    else:
        continue  # skip if not reminder day

    # -------------------------------------------------
    # Send email to each recipient
    # -------------------------------------------------

    recipients = str(row["recipients"]).split("|")

    for person in recipients:
        name, email = person.split(":")

        html_body = f"""
        <html>
        <body style="font-family:Arial; background:#f6f8fa; padding:20px;">
            <div style="max-width:600px; background:#ffffff; padding:20px; border-radius:8px;">
                <h2>Hi {name} 👋</h2>

                <p style="font-size:16px;">
                    <strong>{message_line}</strong>
                </p>

                <div style="margin:20px 0; padding:15px; background:#f1f3f5; border-left:4px solid #0d6efd;">
                    {get_suggestion(row['event_type'])}
                </div>

                <p style="font-size:13px; color:#666;">
                    Sent automatically by your Smart Reminder Bot 🤖
                </p>
            </div>
        </body>
        </html>
        """

        send_email(email.strip(), subject, html_body)
        print(f"Email sent to {name} ({email})")