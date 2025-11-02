import streamlit as st
import sqlite3, bcrypt, os, re, time, datetime, logging
from cryptography.fernet import Fernet


st.set_page_config(page_title="SecurePayLite 💳", layout="centered", page_icon="💳")

st.markdown("""
    <style>
        /* General background gradient */
        body {
            background: linear-gradient(120deg, #101820, #1A2A3A, #0F2027);
            color: #F3F4F6;
            font-family: 'Segoe UI', sans-serif;
        }

        /* Sidebar styling */
        section[data-testid="stSidebar"] {
            background-color: #1C2833 !important;
            color: white;
        }

        /* Buttons */
        .stButton>button {
            background: linear-gradient(90deg, #00B4DB, #0083B0);
            color: white;
            font-weight: 600;
            border-radius: 10px;
            transition: 0.3s;
        }
        .stButton>button:hover {
            background: linear-gradient(90deg, #00A0C6, #007399);
            transform: scale(1.02);
        }

        /* Headers */
        h1, h2, h3, h4 {
            color: #00B4DB !important;
        }

        /* Input fields */
        .stTextInput>div>div>input, textarea {
            border-radius: 8px;
            border: 1px solid #00B4DB;
        }

        /* Footer */
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            text-align: center;
            padding: 0.4rem;
            background: rgba(0,0,0,0.4);
            color: #AEB6BF;
            font-size: 0.8rem;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div style="text-align:center; margin-bottom:20px; padding:10px;">
        <h1>💳 SecurePayLite</h1>
        <h5>Mini Secure FinTech Application for Demonstration</h5>
    </div>
""", unsafe_allow_html=True)


DB_PATH = "securepay.db"
FERNET_KEY_FILE = "fernet.key"
LOG_FILE = "securepay.log"

logging.basicConfig(filename=LOG_FILE, level=logging.INFO)

# Encryption Key Handling
def load_or_create_fernet_key(path=FERNET_KEY_FILE):
    if os.path.exists(path):
        with open(path, "rb") as f:
            key = f.read()
    else:
        key = Fernet.generate_key()
        with open(path, "wb") as f:
            f.write(key)
    return Fernet(key)

fernet = load_or_create_fernet_key()

# Database Setup
def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    conn = get_conn()
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password_hash BLOB,
        email TEXT,
        created_at TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        amount REAL,
        note BLOB,
        created_at TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )""")
    conn.commit()
    conn.close()

init_db()

# Helper functions
def hash_pw(pw): return bcrypt.hashpw(pw.encode(), bcrypt.gensalt())
def verify_pw(pw, hashed): return bcrypt.checkpw(pw.encode(), hashed)
def strong_pw(pw): return len(pw) >= 8 and re.search(r"\d", pw) and re.search(r"[^\w\s]", pw)

def register_user(username, pw, email):
    conn = get_conn(); c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username,password_hash,email,created_at) VALUES (?,?,?,?)",
                  (username, hash_pw(pw), email, datetime.datetime.utcnow().isoformat()))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def find_user(username):
    conn = get_conn(); c = conn.cursor()
    c.execute("SELECT id,username,password_hash,email FROM users WHERE username=?", (username,))
    user = c.fetchone(); conn.close(); return user

def add_tx(user_id, amount, note):
    conn = get_conn(); c = conn.cursor()
    enc = fernet.encrypt(note.encode())
    c.execute("INSERT INTO transactions (user_id,amount,note,created_at) VALUES (?,?,?,?)",
              (user_id, amount, enc, datetime.datetime.utcnow().isoformat()))
    conn.commit(); conn.close()

def get_tx(user_id):
    conn = get_conn(); c = conn.cursor()
    c.execute("SELECT amount,note,created_at FROM transactions WHERE user_id=? ORDER BY created_at DESC", (user_id,))
    data = c.fetchall(); conn.close()
    txs = []
    for amt, enc, ts in data:
        try: note = fernet.decrypt(enc).decode()
        except: note = "[decryption error]"
        txs.append((amt, note, ts))
    return txs

# Session setup
if "user" not in st.session_state: st.session_state.user = None

page = st.sidebar.radio("Navigation", ["🏠 Home", "📝 Register", "🔐 Login", "📊 Dashboard", "👤 Profile", "🚪 Logout", "ℹ️ About"])


if page == "🏠 Home":
    st.markdown("### Welcome to SecurePayLite 💡")
    st.write("This secure FinTech demo showcases encryption, validation, and session control concepts in a simple app.")
    st.info("Use the sidebar to register or login.")

elif page == "📝 Register":
    st.subheader("Create Account ✨")
    user = st.text_input("Username")
    email = st.text_input("Email")
    pw = st.text_input("Password", type="password")
    pw2 = st.text_input("Confirm Password", type="password")
    if st.button("Register"):
        if not user or not pw:
            st.warning("Fields cannot be empty.")
        elif pw != pw2:
            st.error("Passwords do not match.")
        elif not strong_pw(pw):
            st.error("Password must be 8+ chars, include digit & symbol.")
        elif register_user(user.strip(), pw, email.strip()):
            st.success("Account created successfully! Please login.")
        else:
            st.error("Username already exists.")

elif page == "🔐 Login":
    st.subheader("Secure Login 🔑")
    if st.session_state.user:
        st.info(f"Already logged in as {st.session_state.user[1]}.")
    else:
        uname = st.text_input("Username")
        pw = st.text_input("Password", type="password")
        if st.button("Login"):
            u = find_user(uname.strip())
            if u and verify_pw(pw, u[2]):
                st.session_state.user = u
                st.success(f"Welcome back, {u[1]}!")
            else:
                st.error("Invalid credentials.")

elif page == "📊 Dashboard":
    if not st.session_state.user:
        st.warning("Login required.")
    else:
        st.subheader("📈 Your Dashboard")
        amt = st.text_input("Transaction Amount")
        note = st.text_area("Transaction Note (encrypted in DB)")
        if st.button("Add Transaction"):
            try:
                a = float(amt)
                if a <= 0:
                    st.error("Enter a valid positive number.")
                else:
                    add_tx(st.session_state.user[0], a, note)
                    st.success("Transaction added securely.")
            except:
                st.error("Amount must be numeric.")

        st.divider()
        st.markdown("#### Recent Transactions 🔒")
        txs = get_tx(st.session_state.user[0])
        if not txs:
            st.info("No transactions yet.")
        else:
            for t in txs:
                st.markdown(f"- 💰 **{t[0]}** — {t[1]} *(on {t[2]})*")

elif page == "👤 Profile":
    if not st.session_state.user:
        st.warning("Login required.")
    else:
        st.subheader("👤 Profile Information")
        u = st.session_state.user
        st.write(f"**Username:** {u[1]}")
        st.write(f"**Email:** {u[3] if u[3] else '—'}")
        st.write(f"**Created At:** {datetime.datetime.now().strftime('%Y-%m-%d')}")

elif page == "🚪 Logout":
    st.session_state.user = None
    st.success("You have logged out successfully.")

elif page == "ℹ️ About":
    st.markdown("### About SecurePayLite 🔍")
    st.write("""
    This project demonstrates secure coding principles for FinTech systems:
    - Password hashing (bcrypt)
    - Encrypted storage (Fernet)
    - Parameterized queries (SQLi protection)
    - Input validation
    - Secure session handling  
    Developed as part of **CY4053: Cybersecurity in FinTech**.
    """)

st.markdown("<div class='footer'>Developed by Muhammad Umer 22i-7464 | FAST University | CY4053</div>", unsafe_allow_html=True)
