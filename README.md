# CY-4053_A02
Assignment 2 for the course of Cyber Security for Fintech

💳 SecurePayLite – Secure FinTech Demo Application
CY4053 – Cybersecurity in FinTech

Developer: Muhammad Umer
Institution: FAST National University, Islamabad
Semester: Fall 2025

📘 Overview

SecurePayLite is a minimal FinTech-style web application developed as part of the Cybersecurity in FinTech (CY4053) course assignment.
The app demonstrates secure coding principles and manual testing methods in a controlled environment using Python and Streamlit.

The application simulates a secure financial transaction system where users can register, log in, and record encrypted transaction notes — all while adhering to cybersecurity best practices.

🚀 Key Features
Category	Security Mechanism
Authentication	Password hashing using bcrypt
Encryption	Sensitive notes encrypted using Fernet (AES symmetric key)
Database Security	Parameterized queries (SQLite) to prevent SQL Injection
Session Management	Session timeout and login lockout mechanisms
Input Validation	Enforced constraints on passwords, emails, and amounts
Error Handling	Generic user messages (no sensitive debug info)
File Validation	File uploads restricted by type (images only) and size (≤2MB)
Audit Logging	User activities recorded in securepay.log and audit_logs table
UI Design	Secure, minimalist dark-themed interface with clean visuals for demonstration
🧩 Technologies Used

Python 3.11+

Streamlit (for UI)

MongoDB (local database)

bcrypt (password hashing)

Logging (secure activity logs)

🧪 Manual Testing Summary

20 manual security test cases were performed on SecurePayLite covering:

Input validation tests (SQLi, XSS, length checks)

Session management tests (timeout, logout, unauthorized access)

Authentication tests (password hashing, lockout, registration)

Error handling and encryption validation

File upload and format validation

Result: ✅ All 20 test cases passed successfully.


