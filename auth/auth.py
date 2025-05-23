import os
import secrets
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import bcrypt  # type: ignore[import-not-found]
from dotenv import load_dotenv

from log.logger import log

from .exceptions import ConfirmCodeError, InvalidCredentialsError

load_dotenv()


class Auth:
    current_user: str | None = None
    confirmation_code: str | None = None
    ENCRYPTION_KEY_USER = None

    @staticmethod
    def generate_confirmation_code() -> str:
        return str(secrets.randbelow(1000000))

    @staticmethod
    def hash_password(password: str) -> str:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    @staticmethod
    def check_password(stored_hash: str, password: str) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), stored_hash.encode("utf-8"))

    @staticmethod
    def send_confirmation_email(email: str) -> None:
        Auth.confirmation_code = Auth.generate_confirmation_code()
        sender_email = "liliworkgames@gmail.com"
        password = os.getenv("GMAIL_KEY") or ""
        receiver_email = email
        subject = "Email Confirmation from Finance Tracker!"
        body = f"Your confirmation code is: {Auth.confirmation_code}"

        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, msg.as_string())
            log.log("INFO", f"Confirmation email sent to {email}")
        except Exception as e:
            log.log("ERROR", f"Failed to send email: {e!s}")

    @staticmethod
    def register_user(username: str, email: str, password: str, user_code: str) -> None:
        if user_code == Auth.confirmation_code:
            from database.utils import Utils as Db_utils
            from security.user_key import ensure_user_encryption_key, generate_salt_bytes

            salt = generate_salt_bytes()
            Db_utils.add_user(username, email, password, salt)
            ensure_user_encryption_key(username)
        else:
            raise ConfirmCodeError("The verification code is incorrect")

    @staticmethod
    def login_user(identifier: str, password: str) -> None:
        from database.utils import Utils as Db_utils

        user_password = Db_utils.get_user_password(identifier)

        if Auth.check_password(user_password, password):
            log.log("INFO", f"User '{identifier}' logged in successfully.")
            Auth.current_user = identifier
            Auth.ENCRYPTION_KEY_USER = f"ENCRYPTION_KEY_{identifier}"
        else:
            log.log("ERROR", "Invalid credentials")
            raise InvalidCredentialsError("Invalid username/email or password")
