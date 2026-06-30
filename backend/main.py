from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from database import insert_user, get_user, insert_financial_data, insert_ai_analysis
from prediction import analyze_finances
from ai_engine import get_ai_advice

load_dotenv()

app = FastAPI()

# Allow requests from React frontend running on localhost:5173
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Request Models ─────────────────────────────────────────────────────────────

class User(BaseModel):
    username: str
    password: str

class FinancialData(BaseModel):
    income:   int
    debt:     int
    expenses: int


# ── Routes ─────────────────────────────────────────────────────────────────────

@app.get("/")
def home():
    return {"message": "FinRelief AI Backend is running"}


@app.post("/register")
def register(user: User):
    """
    Stores a new username and password in the users table.
    Returns an error message if the username already exists.
    """
    result = insert_user(user.username, user.password)

    if result == "exists":
        return {"message": "Username already exists. Please choose another."}
    elif result == "error":
        return {"message": "Registration failed. Please try again."}

    return {"message": "Registered successfully"}


@app.post("/login")
def login(user: User):
    """
    Checks if the username and password match a record in the users table.
    Returns success or invalid credentials message.
    """
    account = get_user(user.username, user.password)

    if account:
        return {"message": "Login success"}
    else:
        return {"message": "Invalid credentials"}


@app.post("/analyze")
def analyze(data: FinancialData):
    """
    Accepts income, debt, and expenses.
    Calculates debt ratio, financial score, and health label.
    Calls prediction.py for settlement probability.
    Calls ai_engine.py for Gemini AI financial advice.
    Saves the record to users_data table.
    Returns all results as JSON.
    """

    # Step 1: Run all financial calculations from prediction.py
    results    = analyze_finances(data.income, data.debt, data.expenses)

    # Step 2: Get Gemini AI advice from ai_engine.py
    suggestion = get_ai_advice(data.income, data.debt, data.expenses)

    # Step 3: Save financial data → get finance_id back
    finance_id = insert_financial_data(
        user_id         = 1,
        income          = data.income,
        debt            = data.debt,
        expenses        = data.expenses,
        financial_score = results["financial_score"]
    )

    # Step 4: Save AI analysis → linked to finance_id
    insert_ai_analysis(
        finance_id = finance_id,
        health     = results["health"],
        settlement = results["settlement"],
        suggestion = suggestion
    )

    # Step 5: Return all results to the frontend
    return {
        "debt_ratio"      : results["debt_ratio"],
        "financial_score" : results["financial_score"],
        "health"          : results["health"],
        "settlement"      : results["settlement"],
        "suggestion"      : suggestion
    }
