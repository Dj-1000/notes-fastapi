from twilio.rest import Client
from app.core.config import settings

def send_sms(to_phone: str, body: str):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=body,
        from_=settings.TWILIO_PHONE_NUMBER,
        to=to_phone
    )
    print(f"SMS sent successfully to {to_phone}")
    return message.sid
