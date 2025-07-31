# Finance Tracker

## Technologies Used

- **Python 3.12**
- **Flet** — for building the user interface
- **flet_route** — for routing in Flet
- **cryptography** — for data encryption (Fernet, PBKDF2HMAC)
- **bcrypt** — for password hashing
- **python-dotenv** — for working with .env files (key storage)
- **sqlite3** — for database management
- **logging** — for logging
- **pre-commit, ruff, mypy** — for code quality and linting
- **email, smtplib** — for sending email notifications

## Project Structure

- `ui/` — user interface (Flet)
- `auth/` — authentication, password hashing, email confirmation
- `security/` — data encryption, key generation and protection
- `database/` — database operations
- `expenses/` — expense logic
- `log/` — logging
- `start/` — environment and database initialization

## Encryption Implementation

- Data is encrypted using **Fernet** from the `cryptography` library.
- Data is encrypted with a main key (`ENCRYPTION_KEY`) stored in the `.env` file.
- Each user has a separate encryption key, also stored in `.env` in encrypted form.

### Main Encryption Functions

- `encrypt_data(data: str) -> str` — encrypts data with the main key.
- `decrypt_data(encrypted_data: str) -> str` — decrypts data with the main key.
- `encrypt_data_user(data: str) -> str` — encrypts data with the user's key.
- `decrypt_data_user(encrypted_data: str) -> str` — decrypts data with the user's key.

## Key Protection

- The main key (`ENCRYPTION_KEY`) is generated automatically if missing and stored in `.env`.
- User keys are stored in `.env` in encrypted form.
- User keys are encrypted using a key derived via PBKDF2HMAC from the user's unique user_id and salt.
- The salt and user_id are stored in the database.
- To decrypt a user key, a key is generated via PBKDF2HMAC and used to decrypt the user's key from `.env`.

---

This project ensures that sensitive data and encryption keys are securely managed and protected, following best practices for cryptography and key management.
