// api.js
// FinRelief AI — Fetch API Integration
// -----------------------------------------------------------------------
// All 3 functions that connect the React frontend to the FastAPI backend.
// Each function sends a POST request with JSON data and returns the
// parsed response object from the backend.
//
// Base URL points to the FastAPI server running on localhost:8000.
// Imported and called by App.jsx.
// -----------------------------------------------------------------------

const BASE_URL = "http://localhost:8000";

// ── FUNCTION 1: register ─────────────────────────────────────────────────────
//
// Sends username and password to POST /register.
// FastAPI saves the credentials to the users table in SQLite.
//
// Request body (JSON):
//   { "username": "<username>", "password": "<password>" }
//
// Response (JSON):
//   { "message": "Registered successfully" }
//   { "message": "Username already exists. Please choose another." }
//   { "message": "Registration failed. Please try again." }
//
// Returns: parsed response object  { message: string }
// ─────────────────────────────────────────────────────────────────────────────

export async function register(username, password) {
  const response = await fetch(`${BASE_URL}/register`, {
    method:  "POST",
    headers: { "Content-Type": "application/json" },
    body:    JSON.stringify({ username, password }),
  });
  return response.json();
}

// ── FUNCTION 2: login ────────────────────────────────────────────────────────
//
// Sends username and password to POST /login.
// FastAPI checks credentials against the users table in SQLite.
//
// Request body (JSON):
//   { "username": "<username>", "password": "<password>" }
//
// Response (JSON):
//   { "message": "Login success" }
//   { "message": "Invalid credentials" }
//
// Returns: parsed response object  { message: string }
// ─────────────────────────────────────────────────────────────────────────────

export async function login(username, password) {
  const response = await fetch(`${BASE_URL}/login`, {
    method:  "POST",
    headers: { "Content-Type": "application/json" },
    body:    JSON.stringify({ username, password }),
  });
  return response.json();
}

// ── FUNCTION 3: analyze ──────────────────────────────────────────────────────
//
// Sends income, debt, and expenses to POST /analyze.
// FastAPI runs all financial calculations, calls Gemini AI,
// saves the results to the database, and returns the full report.
//
// Request body (JSON):
//   { "income": 5000, "debt": 15000, "expenses": 2500 }
//
// Response (JSON):
//   {
//     "debt_ratio"      : 100.0,
//     "financial_score" : 41.67,
//     "health"          : "At Risk",
//     "settlement"      : "Medium Probability",
//     "suggestion"      : "AI-generated financial advice..."
//   }
//
// Returns: parsed response object with all 5 result fields
// ─────────────────────────────────────────────────────────────────────────────

export async function analyze(income, debt, expenses) {
  const response = await fetch(`${BASE_URL}/analyze`, {
    method:  "POST",
    headers: { "Content-Type": "application/json" },
    body:    JSON.stringify({
      income:   Number(income),
      debt:     Number(debt),
      expenses: Number(expenses),
    }),
  });
  return response.json();
}
