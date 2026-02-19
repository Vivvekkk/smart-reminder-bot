import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# ======================
# EMAIL CONFIG
# ======================
SENDER_EMAIL = "richuuvivuu@gmail.com"
APP_PASSWORD = "sedb yyri zdov yfrl"

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
# READ EVENTS
# ======================
df = pd.read_csv("events.csv")
today = datetime.today().date()

print("Today's date:", today)
print("-" * 50)

# ======================
# SUGGESTION ENGINE
# ======================
def get_suggestion(event_type):
    if event_type.lower() == "birthday":
        return "🎁 Consider a thoughtful gift and a handwritten note"
    elif event_type.lower() == "anniversary":
        return "🍽️ Plan a meaningful dinner or quality time together"
    else:
        return "✨ Take a moment to do something meaningful"

# ======================
# REMINDER LOGIC
# ======================
for _, row in df.iterrows():
    event_date = datetime.strptime(row["event_date"], "%Y-%m-%d").date()
    days_left = (event_date - today).days

    print(f"{row['event_name']} -> days_left = {days_left}")

    if 1 <= days_left <= 90:
        subject = f"🔔 Reminder: {row['event_name']} in {days_left} day(s)"

        # Split recipients
        recipients = row["recipients"].split("|")

        for person in recipients:
            name, email = person.split(":")

            html_body = f"""
            <html>
            <body style="font-family:Arial; background:#f6f8fa; padding:20px;">
                <div style="max-width:600px; background:#ffffff; padding:20px; border-radius:8px;">
                    <h2>Hi {name} 👋</h2>

                    <p>
                        This is a reminder that
                        <strong>{row['event_name']}</strong>
                        is coming up in
                        <strong style="color:#d6336c;">{days_left} day(s)</strong>.
                    </p>

                    <div style="background:#f1f3f5; padding:12px; border-left:4px solid #0d6efd;">
                        {get_suggestion(row['event_type'])}
                    </div>

                    <p style="margin-top:20px; font-size:13px; color:#666;">
                        Sent by your Smart Reminder Bot 🤖
                    </p>
                </div>
            </body>
            </html>
            """

            send_email(email, subject, html_body)
            print(f"📧 Email sent to {name} ({email})")