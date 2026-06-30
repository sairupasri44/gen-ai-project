# Testing Report
## FinRelief AI — AI Powered Debt Relief and Financial Recovery Platform
## Internship Project Submission

---

## Project Overview

| Field              | Details                                      |
|--------------------|----------------------------------------------|
| Project Name       | FinRelief AI                                 |
| Tech Stack         | React.js + Vite, FastAPI, SQLite, Gemini AI  |
| Backend Port       | http://localhost:8000                        |
| Frontend Port      | http://localhost:5173                        |
| Database File      | backend/finance.db                           |
| AI Model           | gemini-2.5-flash                             |
| Test Environment   | Windows, VS Code, Python venv, Node.js       |

---

## How to Start the Project Before Testing

**Terminal 1 — Start Backend:**
```bash
cd gen-ai-project/backend
venv\Scripts\activate
uvicorn main:app --reload
```

**Terminal 2 — Start Frontend:**
```bash
cd gen-ai-project/frontend
npm run dev
```

**Verify both are running:**
- Backend  → http://localhost:8000
- Frontend → http://localhost:5173
- API Docs → http://localhost:8000/docs

---

## Test Data Reference

Use the following values consistently across all test cases:

| Data Set      | Income | Debt   | Expenses | Expected Health | Expected Settlement   |
|---------------|--------|--------|----------|-----------------|-----------------------|
| High Score    | 6000   | 10000  | 2000     | Good            | High Probability      |
| Medium Score  | 4000   | 8000   | 2200     | At Risk         | Medium Probability    |
| Low Score     | 3000   | 25000  | 3200     | Critical        | Low Probability       |
| Edge: Zero    | 0      | 5000   | 1000     | Critical        | Low Probability       |
| Edge: Exact   | 5000   | 15000  | 2500     | At Risk         | Low Probability       |

---

## Section 1 — Frontend Loading Tests

Tests that verify the React frontend starts and renders correctly in the browser.

---

### Test 1.1 — Frontend Starts Without Errors

| Field       | Details                                     |
|-------------|---------------------------------------------|
| Test ID     | FE-01                                       |
| Component   | Vite Dev Server                             |
| Command     | `npm run dev`                               |
| Expected    | Server starts at http://localhost:5173      |

**Steps:**
1. Open terminal in `frontend/` folder
2. Run `npm run dev`
3. Open http://localhost:5173 in browser

**Pass Criteria:**
- [ ] Terminal shows `VITE ready in ... ms`
- [ ] No red error messages in terminal
- [ ] Browser loads without blank screen

---

### Test 1.2 — Login Page Renders

| Field       | Details                                     |
|-------------|---------------------------------------------|
| Test ID     | FE-02                                       |
| Component   | App.jsx — Login Page                        |
| Expected    | Login card visible with all UI elements     |

**Steps:**
1. Open http://localhost:5173
2. Inspect the page visually

**Pass Criteria:**
- [ ] "FinRelief AI" heading is visible
- [ ] "AI Powered Debt Relief Platform" subtitle is visible
- [ ] Username input field is visible
- [ ] Password input field is visible
- [ ] Login button is visible
- [ ] Register button is visible
- [ ] Background is dark (#071226)
- [ ] Card has rounded corners with dark blue background

---

### Test 1.3 — Dashboard Page Renders After Login

| Field       | Details                                     |
|-------------|---------------------------------------------|
| Test ID     | FE-03                                       |
| Component   | App.jsx — Dashboard Page                    |
| Expected    | Dashboard inputs visible after login        |

**Steps:**
1. Register a test user
2. Login with correct credentials
3. Inspect the dashboard page

**Pass Criteria:**
- [ ] Page switches from login to dashboard
- [ ] "Enter your financial details below" subtitle is visible
- [ ] Monthly Income input is visible
- [ ] Total Debt input is visible
- [ ] Monthly Expenses input is visible
- [ ] Analyze button is visible and enabled

---

## Section 2 — Backend API Endpoint Tests

Tests that verify all FastAPI endpoints respond correctly.
Use http://localhost:8000/docs (Swagger UI) to run these manually.

---

### Test 2.1 — Health Check Endpoint

| Field       | Details                                       |
|-------------|-----------------------------------------------|
| Test ID     | API-01                                        |
| Endpoint    | GET /                                         |
| File        | backend/main.py — `home()`                    |
| Expected    | `{ "message": "FinRelief AI Backend is running" }` |

**Steps:**
1. Open http://localhost:8000
2. Check the JSON response in the browser

**Pass Criteria:**
- [ ] Status code is 200
- [ ] Response body: `{ "message": "FinRelief AI Backend is running" }`

---

### Test 2.2 — Register New User

| Field       | Details                                       |
|-------------|-----------------------------------------------|
| Test ID     | API-02                                        |
| Endpoint    | POST /register                                |
| File        | backend/main.py — `register()`                |
| Input       | `{ "username": "test_user", "password": "test123" }` |
| Expected    | `{ "message": "Registered successfully" }`    |

**Steps:**
1. Go to http://localhost:8000/docs
2. Open POST /register → Try it out
3. Enter the test input above
4. Click Execute

**Pass Criteria:**
- [ ] Status code is 200
- [ ] Response: `{ "message": "Registered successfully" }`
- [ ] No 500 server error in terminal

---

### Test 2.3 — Register Duplicate Username

| Field       | Details                                          |
|-------------|--------------------------------------------------|
| Test ID     | API-03                                           |
| Endpoint    | POST /register                                   |
| File        | backend/database.py — `insert_user()`            |
| Input       | Same username as Test 2.2                        |
| Expected    | `{ "message": "Username already exists..." }`    |

**Steps:**
1. Run Test 2.2 first to create the user
2. Submit the same username again

**Pass Criteria:**
- [ ] Status code is 200
- [ ] Response: `{ "message": "Username already exists. Please choose another." }`
- [ ] No duplicate row added to database

---

### Test 2.4 — Login With Valid Credentials

| Field       | Details                                        |
|-------------|------------------------------------------------|
| Test ID     | API-04                                         |
| Endpoint    | POST /login                                    |
| File        | backend/main.py — `login()`                    |
| Input       | `{ "username": "test_user", "password": "test123" }` |
| Expected    | `{ "message": "Login success" }`               |

**Steps:**
1. Register test_user first (Test 2.2)
2. Submit login with correct credentials

**Pass Criteria:**
- [ ] Status code is 200
- [ ] Response: `{ "message": "Login success" }`

---

### Test 2.5 — Login With Wrong Password

| Field       | Details                                        |
|-------------|------------------------------------------------|
| Test ID     | API-05                                         |
| Endpoint    | POST /login                                    |
| File        | backend/database.py — `get_user()`             |
| Input       | `{ "username": "test_user", "password": "wrongpass" }` |
| Expected    | `{ "message": "Invalid credentials" }`         |

**Pass Criteria:**
- [ ] Status code is 200
- [ ] Response: `{ "message": "Invalid credentials" }`
- [ ] Dashboard does NOT open

---

### Test 2.6 — Analyze Financial Data

| Field       | Details                                                   |
|-------------|-----------------------------------------------------------|
| Test ID     | API-06                                                    |
| Endpoint    | POST /analyze                                             |
| File        | backend/main.py — `analyze()`                             |
| Input       | `{ "income": 5000, "debt": 15000, "expenses": 2500 }`     |

**Expected Response:**
```json
{
  "debt_ratio"      : 100.0,
  "financial_score" : 41.67,
  "health"          : "At Risk",
  "settlement"      : "Medium Probability",
  "suggestion"      : "AI-generated advice text..."
}
```

**Pass Criteria:**
- [ ] Status code is 200
- [ ] `debt_ratio` is a number
- [ ] `financial_score` is between 0 and 100
- [ ] `health` is one of: Good / At Risk / Critical
- [ ] `settlement` is one of: High / Medium / Low Probability
- [ ] `suggestion` is a non-empty string from Gemini

---

## Section 3 — Database Tests

Tests that verify SQLite stores data correctly after each API call.
Use a SQLite viewer (VS Code SQLite extension or DB Browser for SQLite).

---

### Test 3.1 — Tables Are Created on Startup

| Field       | Details                                         |
|-------------|-------------------------------------------------|
| Test ID     | DB-01                                           |
| File        | backend/database.py — `create_tables()`         |
| Expected    | 3 tables exist in finance.db                    |

**Steps:**
1. Start the backend with `uvicorn main:app --reload`
2. Open `finance.db` in a SQLite viewer

**Pass Criteria:**
- [ ] Table `users` exists with columns: user_id, username, password
- [ ] Table `financial_data` exists with columns: finance_id, user_id, income, debt, expenses, financial_score
- [ ] Table `ai_analysis` exists with columns: analysis_id, finance_id, health, settlement, suggestion

---

### Test 3.2 — User Registration Saves to Database

| Field       | Details                                         |
|-------------|-------------------------------------------------|
| Test ID     | DB-02                                           |
| File        | backend/database.py — `insert_user()`           |
| Trigger     | POST /register                                  |

**Steps:**
1. Register a new user via the frontend or Swagger
2. Open finance.db → users table

**Pass Criteria:**
- [ ] New row appears in `users` table
- [ ] `username` matches what was submitted
- [ ] `user_id` is auto-incremented correctly

---

### Test 3.3 — Financial Data Saves to Database

| Field       | Details                                           |
|-------------|---------------------------------------------------|
| Test ID     | DB-03                                             |
| File        | backend/database.py — `insert_financial_data()`   |
| Trigger     | POST /analyze                                     |

**Steps:**
1. Submit income/debt/expenses via the dashboard
2. Open finance.db → financial_data table

**Pass Criteria:**
- [ ] New row appears in `financial_data` table
- [ ] `income`, `debt`, `expenses` match submitted values
- [ ] `financial_score` is stored as a decimal (e.g. 41.67)
- [ ] `finance_id` is auto-incremented

---

### Test 3.4 — AI Analysis Saves to Database

| Field       | Details                                          |
|-------------|--------------------------------------------------|
| Test ID     | DB-04                                            |
| File        | backend/database.py — `insert_ai_analysis()`     |
| Trigger     | POST /analyze                                    |

**Steps:**
1. Submit analyze request
2. Open finance.db → ai_analysis table

**Pass Criteria:**
- [ ] New row appears in `ai_analysis` table
- [ ] `finance_id` matches the ID from `financial_data`
- [ ] `health` is Good / At Risk / Critical
- [ ] `settlement` is High / Medium / Low Probability
- [ ] `suggestion` contains the Gemini advice text
- [ ] Foreign key link between ai_analysis and financial_data is intact

---

## Section 4 — Login Authentication Tests

Tests that verify the login flow works correctly end-to-end from the frontend.

---

### Test 4.1 — Successful Login Redirects to Dashboard

| Field       | Details                               |
|-------------|---------------------------------------|
| Test ID     | AUTH-01                               |
| File        | frontend/src/App.jsx — `handleLogin()`|

**Steps:**
1. Open http://localhost:5173
2. Register a new user
3. Enter correct username and password
4. Click Login

**Pass Criteria:**
- [ ] Page switches to dashboard (page state changes to "dashboard")
- [ ] Dashboard inputs are visible
- [ ] No error message is shown

---

### Test 4.2 — Wrong Password Shows Error

| Field       | Details                               |
|-------------|---------------------------------------|
| Test ID     | AUTH-02                               |
| File        | frontend/src/App.jsx — `handleLogin()`|

**Steps:**
1. Enter correct username but wrong password
2. Click Login

**Pass Criteria:**
- [ ] Page stays on login screen
- [ ] Red error message appears: "Invalid username or password. Please try again."
- [ ] Dashboard is NOT shown

---

### Test 4.3 — Empty Fields Show Validation Error

| Field       | Details                               |
|-------------|---------------------------------------|
| Test ID     | AUTH-03                               |
| File        | frontend/src/App.jsx — `handleLogin()`|

**Steps:**
1. Leave username and password blank
2. Click Login

**Pass Criteria:**
- [ ] No API call is made to the backend
- [ ] Error message appears: "Please enter your username and password."

---

## Section 5 — Gemini AI Response Tests

Tests that verify the Gemini API integration returns valid responses.

---

### Test 5.1 — AI Returns Non-Empty Advice

| Field       | Details                                            |
|-------------|----------------------------------------------------|
| Test ID     | AI-01                                              |
| File        | backend/ai_engine.py — `get_ai_advice()`           |
| Input       | income=5000, debt=15000, expenses=2500             |

**Pass Criteria:**
- [ ] `suggestion` field in /analyze response is not empty
- [ ] `suggestion` contains two paragraphs (recovery advice + negotiation strategy)
- [ ] Text is in English and reads as professional financial advice
- [ ] No "AI failed" or error text in the response

---

### Test 5.2 — AI Advice Changes With Different Inputs

| Field       | Details                                       |
|-------------|-----------------------------------------------|
| Test ID     | AI-02                                         |
| File        | backend/ai_engine.py — `get_ai_advice()`      |

**Steps:**
1. Run /analyze with income=6000, debt=5000, expenses=1500
2. Run /analyze with income=2000, debt=30000, expenses=2500
3. Compare the two suggestion fields

**Pass Criteria:**
- [ ] Both responses contain advice text
- [ ] The advice content is meaningfully different between the two inputs
- [ ] Critical scenario returns more urgent language than the healthy scenario

---

### Test 5.3 — Fallback Works When API Fails

| Field       | Details                                             |
|-------------|-----------------------------------------------------|
| Test ID     | AI-03                                               |
| File        | backend/ai_engine.py — `get_recovery_advice()`      |

**Steps:**
1. Temporarily set `GEMINI_API_KEY=invalid_key` in .env
2. Restart backend
3. Submit an analyze request

**Pass Criteria:**
- [ ] Backend does NOT crash
- [ ] Response still returns a `suggestion` field
- [ ] Fallback message is returned instead of empty string
- [ ] Restore the real API key after this test

---

## Section 6 — Error Handling Tests

Tests that verify the application handles unexpected inputs and failures gracefully.

---

### Test 6.1 — Empty Analyze Fields Show Validation Error

| Field       | Details                                          |
|-------------|--------------------------------------------------|
| Test ID     | ERR-01                                           |
| File        | frontend/src/App.jsx — `handleAnalyze()`         |

**Steps:**
1. Login to dashboard
2. Leave all 3 inputs empty
3. Click Analyze

**Pass Criteria:**
- [ ] No API call is made
- [ ] Error message: "Please fill in all three fields: Income, Debt, and Expenses."

---

### Test 6.2 — Non-Numeric Input Shows Validation Error

| Field       | Details                                        |
|-------------|------------------------------------------------|
| Test ID     | ERR-02                                         |
| File        | frontend/src/App.jsx — `handleAnalyze()`       |

**Steps:**
1. Enter "abc" in the Income field
2. Click Analyze

**Pass Criteria:**
- [ ] No API call is made
- [ ] Error message: "Income, Debt, and Expenses must be numbers."

---

### Test 6.3 — Backend Offline Shows Error Message

| Field       | Details                                           |
|-------------|---------------------------------------------------|
| Test ID     | ERR-03                                            |
| File        | frontend/src/api.js — `analyze()`                 |

**Steps:**
1. Stop the backend server (Ctrl+C)
2. Try to login or submit analyze from frontend

**Pass Criteria:**
- [ ] Application does NOT crash or show blank screen
- [ ] Error message appears: "... Make sure the backend is running."
- [ ] User can still interact with the form

---

### Test 6.4 — Zero Income Handled in Backend

| Field       | Details                                          |
|-------------|--------------------------------------------------|
| Test ID     | ERR-04                                           |
| File        | backend/prediction.py — `calculate_debt_ratio()` |
| Input       | `{ "income": 0, "debt": 5000, "expenses": 1000 }` |

**Pass Criteria:**
- [ ] Backend does NOT crash with division by zero error
- [ ] `debt_ratio` returns 100.0 (capped)
- [ ] `financial_score` returns 0.0
- [ ] `health` returns "Critical"
- [ ] `settlement` returns "Low Probability"

---

## Section 7 — Financial Calculation Accuracy Tests

Tests that verify `prediction.py` calculations are mathematically correct.

---

### Test 7.1 — Debt Ratio Calculation

| Field       | Details                                           |
|-------------|---------------------------------------------------|
| Test ID     | CALC-01                                           |
| File        | backend/prediction.py — `calculate_debt_ratio()`  |
| Formula     | debt_ratio = (debt / income) × 100, capped at 100 |

| Input                        | Expected Output |
|------------------------------|-----------------|
| income=5000, debt=2000        | 40.0            |
| income=5000, debt=15000       | 100.0 (capped)  |
| income=6000, debt=10000       | 100.0 (capped)  |
| income=0,    debt=5000        | 100.0 (guard)   |

**Pass Criteria:**
- [ ] All 4 rows return the expected value
- [ ] No value exceeds 100.0
- [ ] Zero income returns 100.0 without error

---

### Test 7.2 — Financial Score Calculation

| Field       | Details                                                |
|-------------|--------------------------------------------------------|
| Test ID     | CALC-02                                                |
| File        | backend/prediction.py — `calculate_financial_score()`  |
| Formula     | score = ((income − expenses − debt/36) / income) × 100 |

| Input                               | Expected Score |
|-------------------------------------|----------------|
| income=5000, debt=15000, expenses=2500 | 41.67       |
| income=6000, debt=10000, expenses=2000 | 71.3        |
| income=3000, debt=25000, expenses=3200 | 0.0 (clamped) |

**Pass Criteria:**
- [ ] Score for 5000/15000/2500 is approximately 41.67
- [ ] Score for 6000/10000/2000 is approximately 71.3
- [ ] Score never goes below 0 or above 100

---

### Test 7.3 — Health Status Label

| Field       | Details                                       |
|-------------|-----------------------------------------------|
| Test ID     | CALC-03                                       |
| File        | backend/prediction.py — `calculate_health()`  |

| Score Input | Expected Health |
|-------------|-----------------|
| 85          | Good            |
| 70          | Good            |
| 69          | At Risk         |
| 40          | At Risk         |
| 39          | Critical        |
| 0           | Critical        |

**Pass Criteria:**
- [ ] All 6 score inputs return the correct health label
- [ ] Boundary values (70 and 40) return correct labels

---

### Test 7.4 — Settlement Prediction (3-Condition Logic)

| Field       | Details                                            |
|-------------|----------------------------------------------------|
| Test ID     | CALC-04                                            |
| File        | backend/prediction.py — `predict_settlement()`     |
| Logic       | 3 conditions: surplus > 0, debt/income < 3, expenses/income < 0.5 |

| Income | Debt  | Expenses | Conditions Met | Expected Result      |
|--------|-------|----------|----------------|----------------------|
| 6000   | 10000 | 2000     | 3 of 3         | High Probability     |
| 4000   | 8000  | 2200     | 2 of 3         | Medium Probability   |
| 3000   | 25000 | 3200     | 0 of 3         | Low Probability      |
| 0      | 5000  | 1000     | —              | Low Probability      |

**Pass Criteria:**
- [ ] All 4 rows return the expected settlement label
- [ ] Zero income guard returns "Low Probability" without error

---

## Section 8 — End-to-End Full Flow Test

The final test that validates the complete user journey from registration to viewing AI results.

---

### Test 8.1 — Complete User Journey

| Field       | Details                                     |
|-------------|---------------------------------------------|
| Test ID     | E2E-01                                      |
| Covers      | All modules: frontend, backend, DB, Gemini  |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Open http://localhost:5173 | Login page loads |
| 2 | Enter username + password → Register | "Registered successfully" alert |
| 3 | Enter same credentials → Login | Dashboard opens |
| 4 | Enter income=5000, debt=15000, expenses=2500 | Fields accepted |
| 5 | Click Analyze | Button shows "Analyzing...", spinner appears |
| 6 | Wait for response (5–15 seconds) | Financial Report section appears |
| 7 | Check Debt Ratio | Shows a percentage value |
| 8 | Check Financial Score | Shows a value between 0 and 100 |
| 9 | Check Health Status | Shows colored badge: Good/At Risk/Critical |
| 10 | Check Settlement | Shows colored badge: High/Medium/Low Probability |
| 11 | Check AI Advice | Two paragraphs of financial advice visible |
| 12 | Open finance.db | Row exists in financial_data and ai_analysis tables |

**Pass Criteria:**
- [ ] All 12 steps complete without errors
- [ ] Data is saved to database
- [ ] AI advice is displayed on dashboard

---

## Test Results Summary

Fill in after completing all tests:

| Section                           | Total Tests | Passed | Failed | Pass Rate |
|-----------------------------------|-------------|--------|--------|-----------|
| Section 1 — Frontend Loading      | 3           |        |        |           |
| Section 2 — Backend API Endpoints | 6           |        |        |           |
| Section 3 — Database              | 4           |        |        |           |
| Section 4 — Login Authentication  | 3           |        |        |           |
| Section 5 — Gemini AI Response    | 3           |        |        |           |
| Section 6 — Error Handling        | 4           |        |        |           |
| Section 7 — Financial Calculations| 4           |        |        |           |
| Section 8 — End-to-End            | 1           |        |        |           |
| **TOTAL**                         | **28**      |        |        |           |

---

## Known Limitations

| # | Limitation                                          | Impact  |
|---|-----------------------------------------------------|---------|
| 1 | user_id is hardcoded as 1 in /analyze endpoint      | Medium  |
| 2 | Passwords are stored as plain text (not hashed)     | High    |
| 3 | No session/token management after login             | Medium  |
| 4 | Gemini API response time may vary (5–20 seconds)    | Low     |
| 5 | SQLite not suitable for concurrent multi-user load  | Low     |

---

## Tester Sign-Off

| Field              | Details            |
|--------------------|--------------------|
| Project            | FinRelief AI       |
| Tested By          |                    |
| Testing Date       |                    |
| Overall Status     | Pass / Fail        |
| Supervisor         |                    |

---

*Generated for: FinRelief AI — AI Powered Debt Relief and Financial Recovery Platform*
*Internship Project Testing Report*
