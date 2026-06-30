# Backend Setup Guide
## FinRelief AI — FastAPI Backend
### AI Powered Debt Relief and Financial Recovery Platform

---

## Backend Folder Structure

```
gen-ai-project/
└── backend/
    ├── main.py              ← FastAPI app, API routes (/, /register, /login, /analyze)
    ├── database.py          ← SQLite connection, creates accounts + users_data tables
    ├── ai_engine.py         ← Google Gemini API integration, get_ai_advice()
    ├── prediction.py        ← Settlement prediction logic based on financial score
    ├── requirements.txt     ← All Python dependencies with pinned versions
    ├── .env                 ← Secret API key (never commit this file)
    ├── .env.example         ← Safe template showing required environment variables
    └── finance.db           ← SQLite database file (auto-created on first run)
```

---

## Step 1 — Verify Python Installation

Open a terminal in VS Code (`Ctrl + `` `) and confirm Python is installed:

```bash
python --version
```

Expected output:
```
Python 3.10.x  or higher
```

If Python is not installed, download it from https://www.python.org/downloads/
Make sure to check **"Add Python to PATH"** during installation.

---

## Step 2 — Navigate to the Backend Folder

```bash
cd gen-ai-project/backend
```

Confirm you are in the right folder:
```bash
dir
```

You should see: `main.py`, `database.py`, `ai_engine.py`, `prediction.py`, `requirements.txt`

---

## Step 3 — Create a Python Virtual Environment

A virtual environment keeps your project dependencies isolated from other Python projects.

```bash
python -m venv .venv
```

This creates a `.venv/` folder inside your backend directory.

```
backend/
└── .venv/          ← Virtual environment folder (do not edit manually)
```

---

## Step 4 — Activate the Virtual Environment

**On Windows (Command Prompt):**
```bash
.venv\Scripts\activate
```

**On Windows (PowerShell):**
```bash
.venv\Scripts\Activate.ps1
```

**On macOS / Linux:**
```bash
source .venv/bin/activate
```

After activation, your terminal prompt will show `(.venv)`:
```
(.venv) C:\Users\USER\gen-ai-project\backend>
```

> To deactivate the virtual environment later, simply run: `deactivate`

---

## Step 5 — Install All Dependencies

Install all required packages from `requirements.txt`:

```bash
pip install -r requirements.txt
```

This installs the following packages:

| Package               | Version   | Purpose                                              |
|-----------------------|-----------|------------------------------------------------------|
| fastapi               | 0.115.0   | Web framework for building the REST API              |
| uvicorn               | 0.30.6    | ASGI server that runs the FastAPI application        |
| pydantic              | 2.8.2     | Data validation for API request and response models  |
| python-dotenv         | 1.0.1     | Loads GEMINI_API_KEY from the .env file              |
| google-generativeai   | 0.8.3     | Google Gemini AI SDK for generating financial advice |
| google-genai          | 1.16.0    | Updated Google GenAI client used in ai_engine.py     |

> sqlite3 does NOT need to be installed — it is built into Python's standard library.

Verify all packages were installed correctly:
```bash
pip list
```

---

## Step 6 — Configure the Environment File

The `.env` file stores your secret Gemini API key.
Copy the example file and add your real API key:

```bash
copy .env.example .env
```

Open `.env` and replace the placeholder:
```
GEMINI_API_KEY=your_gemini_api_key_here
```

Replace `your_gemini_api_key_here` with your actual key from https://aistudio.google.com/app/apikey

**Important:** The `.env` file is already listed in `.gitignore` and will never be committed to Git.

---

## Step 7 — Understand the API Endpoints

All three endpoints are defined in `main.py`:

### GET `/`
Health check to confirm the backend is running.
```
Request  : GET http://localhost:8000/
Response : { "message": "Backend Working" }
```

---

### POST `/register`
Registers a new user by saving username and password to the `accounts` table in SQLite.

```
Request body (JSON):
{
  "username": "john_doe",
  "password": "securepassword"
}

Response:
{ "message": "Registered successfully" }
```

Code location — [main.py](./main.py), function `register()`:
```python
@app.post("/register")
def register(user: User):
    cursor.execute(
        "INSERT INTO accounts(username,password) VALUES (?,?)",
        (user.username, user.password)
    )
    conn.commit()
    return {"message": "Registered successfully"}
```

---

### POST `/login`
Validates user credentials against the `accounts` table and returns login status.

```
Request body (JSON):
{
  "username": "john_doe",
  "password": "securepassword"
}

Response (success) : { "message": "Login success" }
Response (failure) : { "message": "Invalid credentials" }
```

Code location — [main.py](./main.py), function `login()`:
```python
@app.post("/login")
def login(user: User):
    cursor.execute(
        "SELECT * FROM accounts WHERE username=? AND password=?",
        (user.username, user.password)
    )
    account = cursor.fetchone()
    if account:
        return {"message": "Login success"}
    else:
        return {"message": "Invalid credentials"}
```

---

### POST `/analyze`
Core endpoint. Accepts income, debt, and expenses. Runs the financial calculation,
settlement prediction via `prediction.py`, and Gemini AI advice via `ai_engine.py`.

```
Request body (JSON):
{
  "income": 5000,
  "debt": 15000,
  "expenses": 2500
}

Response:
{
  "debt_ratio"      : 40,
  "financial_score" : 70,
  "health"          : "Good",
  "settlement"      : "Medium Probability",
  "suggestion"      : "Reduce discretionary spending..."
}
```

Internal processing order inside `analyze()`:
```
1. Validate request data using Pydantic (FinancialData model)
2. Save income, debt, expenses to SQLite via database.py
3. Compute financial_score (currently set to 70 as base)
4. Pass score to prediction.py → returns settlement label
5. Pass income, debt, expenses to ai_engine.py → calls Gemini API
6. Return all results as a JSON response to the frontend
```

---

## Step 8 — Understand Each Backend File

### main.py
The entry point of the entire backend. It:
- Creates the FastAPI `app` instance
- Registers CORS middleware to allow requests from the React frontend
- Loads environment variables via `load_dotenv()`
- Defines all three API endpoints: `/register`, `/login`, `/analyze`
- Imports and calls functions from `database.py`, `prediction.py`, and `ai_engine.py`

---

### database.py
Handles all SQLite database operations. It:
- Creates a persistent connection to `finance.db` using Python's built-in `sqlite3`
- Creates two tables on startup if they do not already exist:
  - `accounts` — stores username and password for login
  - `users_data` — stores income, debt, and expenses submissions
- Exports `conn` and `cursor` which are imported directly into `main.py`

```python
conn = sqlite3.connect("finance.db", check_same_thread=False)
cursor = conn.cursor()
```

> `check_same_thread=False` is required because FastAPI handles requests across multiple threads.

---

### ai_engine.py
Handles all communication with the Google Gemini API. It:
- Loads the `GEMINI_API_KEY` from the `.env` file
- Creates a `genai.Client` instance authenticated with the API key
- Defines `get_ai_advice(income, debt, expenses)` which:
  - Builds a structured financial prompt with the user's data
  - Sends the prompt to the `gemini-2.5-flash` model
  - Returns the AI-generated advice as a plain text string
  - Returns `"AI failed"` if any exception occurs

```python
def get_ai_advice(income, debt, expenses):
    prompt = f"""
    Give short financial advice.
    Income: {income}, Debt: {debt}, Expenses: {expenses}
    Answer in 2 lines only.
    """
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text
```

---

### prediction.py
A lightweight rule-based engine that predicts debt settlement probability. It:
- Accepts a `financial_score` integer as input
- Returns a plain text settlement label based on score thresholds:

```python
def predict(score):
    if score > 80:
        return "High Settlement Probability"
    elif score > 50:
        return "Medium Probability"
    return "Low Probability"
```

| Score Range | Settlement Result           |
|-------------|-----------------------------|
| Above 80    | High Settlement Probability |
| 51 to 80    | Medium Probability          |
| 50 or below | Low Probability             |

---

## Step 9 — Run the FastAPI Backend Server

Start the development server with auto-reload enabled:

```bash
uvicorn main:app --reload
```

Expected terminal output:
```
INFO:     Will watch for changes in these directories: ['C:\\...\\backend']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process using WatchFiles
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

The backend is now running at: **http://localhost:8000**

> `--reload` means the server automatically restarts whenever you save a file. Use this in development only.

---

## Step 10 — Test the API with Swagger UI

FastAPI automatically generates interactive API documentation.

Open your browser and go to:
```
http://localhost:8000/docs
```

You will see the Swagger UI with all three endpoints listed:

```
GET   /          ← Health check
POST  /register  ← User registration
POST  /login     ← User login
POST  /analyze   ← Financial analysis
```

Click any endpoint → Click **"Try it out"** → Enter test data → Click **"Execute"**

---

## Step 11 — Test with Sample Data

Use the `/analyze` endpoint with this test payload in Swagger UI or Postman:

```json
{
  "income": 5000,
  "debt": 15000,
  "expenses": 2500
}
```

Expected response:
```json
{
  "debt_ratio": 40,
  "financial_score": 70,
  "health": "Good",
  "settlement": "Medium Probability",
  "suggestion": "Focus on reducing high-interest debt first..."
}
```

---

## Common Errors and Fixes

| Error                                      | Cause                                  | Fix                                               |
|--------------------------------------------|----------------------------------------|---------------------------------------------------|
| `ModuleNotFoundError: No module named 'fastapi'` | Virtual environment not activated  | Run `venv\Scripts\activate` then retry            |
| `Address already in use`                   | Port 8000 is occupied                  | Run `uvicorn main:app --reload --port 8001`       |
| `GEMINI_API_KEY not found`                 | `.env` file missing or key is blank    | Create `.env` file and paste your Gemini API key  |
| `AI failed` returned in response           | Invalid or expired Gemini API key      | Regenerate key at https://aistudio.google.com     |
| `sqlite3.OperationalError: no such table`  | Database not initialized               | Ensure `database.py` runs before `main.py` starts |
| `CORS error in browser`                    | Frontend origin not allowed            | Confirm `allow_origins=["*"]` is set in `main.py` |

---

## Quick Reference — All Commands

```bash
# Step 1 — Go to backend folder
cd gen-ai-project/backend

# Step 2 — Create virtual environment
python -m venv .venv

# Step 3 — Activate virtual environment (Windows)
.venv\Scripts\activate

# Step 4 — Install all dependencies
pip install -r requirements.txt

# Step 5 — Configure environment file
copy .env.example .env
# Then open .env and paste your Gemini API key

# Step 6 — Start the backend server
uvicorn main:app --reload

# Step 7 — Open API docs in browser
# http://localhost:8000/docs
```

---

*Generated for: FinRelief AI — AI Powered Debt Relief and Financial Recovery Platform*
*Internship Project Documentation — Backend Setup Guide*
