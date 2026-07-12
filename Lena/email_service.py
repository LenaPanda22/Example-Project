# SCHICHT: Infrastruktur — Benachrichtigungen

from logger import log, log_error
from config import SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS


class EmailService:
    def __init__(self):
        self.host = SMTP_HOST
        self.port = SMTP_PORT
        self.user = SMTP_USER
        self.password = SMTP_PASS
        log("EmailService verbindet zu " + self.host)

    def send(self, to, subject, body):
        if to is None or "@" not in to:
            log_error("Ungueltige E-Mail: " + str(to))
            return False
        if subject is None or subject == "":
            log_error("Subject darf nicht leer sein")
            return False
        if body is None or body == "":
            log_error("Body darf nicht leer sein")
            return False
        log("MAIL -> " + to + " | " + subject)
        print("    " + body.replace("\n", "\n    "))
        return True

    def send_sms(self, number, message):
        if number is None or len(number) < 5:
            log_error("Ungueltige Telefonnummer")
            return False
        log("SMS -> " + number + " | " + message)
        return True

    def send_push(self, device_id, message):
        log("PUSH -> " + device_id + " | " + message)
        return True
