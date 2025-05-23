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
    blocked_user: str | None = None

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
    def verify_email_exists(email: str) -> bool:
        from database.utils import Utils as Db_utils

        username = Db_utils.get_username_by_email(email)
        return username is not None

    @staticmethod
    def send_confirmation_email(email: str) -> None:
        Auth.confirmation_code = Auth.generate_confirmation_code()
        sender_email = "liliworkgames@gmail.com"
        password = os.getenv("GMAIL_KEY") or ""
        receiver_email = email
        subject = "Підтвердження пошти - Finance Tracker"
        body = f"Ваш код підтвердження: {Auth.confirmation_code}"

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
            raise ValueError("Помилка при відправці коду підтвердження") from e

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

    @staticmethod
    def verify_confirmation_code(email: str, code: str) -> bool:
        if Auth.confirmation_code is None:
            log.log("ERROR", "No confirmation code was generated")
            return False

        is_valid = code == Auth.confirmation_code
        if not is_valid:
            log.log("ERROR", f"Invalid confirmation code for email {email}")

        return is_valid

    @staticmethod
    def reset_password(email: str, code: str, new_password: str) -> None:
        from database.utils import Utils as Db_utils

        if not code:
            log.log("ERROR", "No confirmation code provided")
            raise ValueError("Будь ласка, введіть код підтвердження")

        username = Auth.blocked_user
        if not username:
            log.log("ERROR", f"User not found for email {email}")
            raise ValueError("Користувача з такою електронною поштою не знайдено")

        if not Auth.verify_confirmation_code(email, code):
            log.log("ERROR", f"Invalid confirmation code for email {email}")
            raise ConfirmCodeError("Невірний код підтвердження")

        try:
            Db_utils.update_user_password(username, new_password)
            log.log("INFO", f"Password reset successful for user {username}")
        except Exception as err:
            log.log("ERROR", f"Failed to reset password for user {username}: {err}")
            raise ValueError("Помилка при зміні паролю") from err
