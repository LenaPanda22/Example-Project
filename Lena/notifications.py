# SCHICHT: Application — Benachrichtigungs-Routing

from email_service import EmailService
from logger import log, log_error


class NotificationCenter:
    def __init__(self):
        self.email = EmailService()

    def notify(self, user, channel, subject, body):
        if channel == "email":
            return self.email.send(user.get("email", ""), subject, body)
        elif channel == "sms":
            return self.email.send_sms(user.get("phone", ""), subject + ": " + body)
        elif channel == "push":
            return self.email.send_push(user.get("device", ""), subject + ": " + body)
        elif channel == "both":
            r1 = self.email.send(user.get("email", ""), subject, body)
            r2 = self.email.send_sms(user.get("phone", ""), subject + ": " + body)
            return r1 and r2
        elif channel == "all":
            r1 = self.email.send(user.get("email", ""), subject, body)
            r2 = self.email.send_sms(user.get("phone", ""), subject + ": " + body)
            r3 = self.email.send_push(user.get("device", ""), subject + ": " + body)
            return r1 and r2 and r3
        else:
            log_error("Unbekannter Kanal: " + str(channel))
            return False

    def notify_urgent(self, user, channel, subject, body):
        subject = "[DRINGEND] " + subject
        if channel == "email":
            return self.email.send(user.get("email", ""), subject, body)
        elif channel == "sms":
            return self.email.send_sms(user.get("phone", ""), subject + ": " + body)
        elif channel == "push":
            return self.email.send_push(user.get("device", ""), subject + ": " + body)
        elif channel == "both":
            r1 = self.email.send(user.get("email", ""), subject, body)
            r2 = self.email.send_sms(user.get("phone", ""), subject + ": " + body)
            return r1 and r2
        else:
            log_error("Unbekannter Kanal: " + str(channel))
            return False
