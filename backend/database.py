import sqlite3

DB_PATH = "finance.db"

# ── Single persistent connection for FastAPI lifetime ────────────────────────
# check_same_thread=False required — FastAPI handles requests across threads.
# conn and cursor are closed via atexit on server shutdown.
# ─────────────────────────────────────────────────────────────────────────────


# ── CREATE TABLES ─────────────────────────────────────────────────────────────

def create_tables():
    with sqlite3.connect(DB_PATH) as _conn:
        _conn.execute("PRAGMA journal_mode=WAL")   # prevents locking on Windows
        _c = _conn.cursor()

        _c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id   INTEGER PRIMARY KEY AUTOINCREMENT,
            username  TEXT    NOT NULL UNIQUE,
            password  TEXT    NOT NULL
        )
        """)

        _c.execute("""
        CREATE TABLE IF NOT EXISTS financial_data (
            finance_id      INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id         INTEGER NOT NULL,
            income          INTEGER NOT NULL,
            debt            INTEGER NOT NULL,
            expenses        INTEGER NOT NULL,
            financial_score REAL    DEFAULT 0.0,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
        """)

        _c.execute("""
        CREATE TABLE IF NOT EXISTS ai_analysis (
            analysis_id  INTEGER PRIMARY KEY AUTOINCREMENT,
            finance_id   INTEGER NOT NULL,
            health       TEXT    NOT NULL,
            settlement   TEXT    NOT NULL,
            suggestion   TEXT    NOT NULL,
            FOREIGN KEY (finance_id) REFERENCES financial_data (finance_id)
        )
        """)

        _conn.commit()


# ── INSERT / LOOKUP FUNCTIONS — each opens its own scoped connection ──────────

def insert_user(username, password):
    """
    Returns 'exists' | 'success' | 'error'.
    Called by POST /register.
    """
    try:
        with sqlite3.connect(DB_PATH) as _conn:
            _conn.execute("PRAGMA journal_mode=WAL")   # prevents locking issues
            _c = _conn.cursor()
            row = _c.execute(
                "SELECT user_id FROM users WHERE username = ?", (username,)
            ).fetchone()
            if row:
                return "exists"
            _c.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password)
            )
            _conn.commit()
        return "success"
    except Exception as e:
        print(f"INSERT USER ERROR: {type(e).__name__}: {e}")
        return "error"


def get_user(username, password):
    """
    Returns the matching user row or None.
    Called by POST /login.
    """
    try:
        with sqlite3.connect(DB_PATH) as _conn:
            _conn.row_factory = sqlite3.Row
            _c = _conn.cursor()
            return _c.execute(
                "SELECT * FROM users WHERE username = ? AND password = ?",
                (username, password)
            ).fetchone()
    except Exception as e:
        print("GET USER ERROR:", e)
        return None


def insert_financial_data(user_id, income, debt, expenses, financial_score):
    """
    Inserts a financial record and returns its auto-generated finance_id.
    Called by POST /analyze.
    """
    try:
        with sqlite3.connect(DB_PATH) as _conn:
            _c = _conn.cursor()
            _c.execute(
                """
                INSERT INTO financial_data
                    (user_id, income, debt, expenses, financial_score)
                VALUES (?, ?, ?, ?, ?)
                """,
                (user_id, income, debt, expenses, financial_score)
            )
            _conn.commit()
            return _c.lastrowid
    except Exception as e:
        print("INSERT FINANCIAL DATA ERROR:", e)
        return None


def insert_ai_analysis(finance_id, health, settlement, suggestion):
    """
    Inserts an AI analysis result linked to finance_id.
    Called by POST /analyze after insert_financial_data.
    """
    try:
        with sqlite3.connect(DB_PATH) as _conn:
            _c = _conn.cursor()
            _c.execute(
                """
                INSERT INTO ai_analysis
                    (finance_id, health, settlement, suggestion)
                VALUES (?, ?, ?, ?)
                """,
                (finance_id, health, settlement, suggestion)
            )
            _conn.commit()
            return _c.lastrowid
    except Exception as e:
        print("INSERT AI ANALYSIS ERROR:", e)
        return None


# Run on import — creates all tables if they do not exist
create_tables()
