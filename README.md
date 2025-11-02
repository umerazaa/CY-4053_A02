# SecurePayLite - Demo Secure FinTech App

## Setup
1. Install dependencies:
   pip install -r requirements.txt

2. Run the app:
   streamlit run app.py

3. Files created:
   - securepay.db (SQLite DB)
   - securepay.log (activity log)
   - fernet.key (symmetric key for encryption)

## Notes on security (for report)
- Passwords hashed with bcrypt (with salt).
- All SQL uses parameterized queries to prevent SQL injection.
- Transaction notes are encrypted with Fernet (symmetric encryption).
- Session timeout (5 minutes) and account lockout (after 5 failed attempts) implemented.
- Input validation (amount numeric, note length limits, password strength).
- File uploads validated by extension and size.


