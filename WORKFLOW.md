# Project Workflow
## FinRelief AI — AI Powered Debt Relief and Financial Recovery Platform

---

## Workflow Overview

```
┌─────────────┐     ┌──────────────┐     ┌───────────────────┐     ┌──────────────────┐
│    USER     │────▶│   FRONTEND   │────▶│  FASTAPI BACKEND  │────▶│   GEMINI AI API  │
│  (Browser)  │     │  React/Vite  │     │      Python       │     │  gemini-2.5-flash│
└─────────────┘     └──────────────┘     └───────────────────┘     └──────────────────┘
                           │                       │
                           │                       ▼
                           │              ┌───────────────────┐
                           │              │  SQLite Database  │
                           │              │    finance.db     │
                           └──────────────└───────────────────┘
                              Results returned to dashboard
```

---

## Complete Step-by-Step Workflow

---

## PHASE 1 — User Registration

### Step 1 — User Opens the Application

The user navigates to `http://localhost:5173` in their browser.
Vite serves the React application. React renders the Login page from `App.jsx`
because the default `page` state is set to `"login"`.

```
Browser → http://localhost:5173
       → Vite serves index.html
       → React mounts App.jsx
       → page state = "login"
       → Login card rendered
```

---

### Step 2 — User Fills in Registration Form

The user types a username and password into the two input fields on the Login page.
React's `onChange` handlers update the `username` and `password` state values
in real time as the user types.

```jsx
// App.jsx — state updates on every keystroke
const [username, setUsername] = useState("");
const [password, setPassword] = useState("");

<input onChange={(e) => setUsername(e.target.value)} />
<input onChange={(e) => setPassword(e.target.value)} />
```

---

### Step 3 — User Clicks the Register Button

The `handleRegister()` function runs in `App.jsx`.
It first validates that both fields are filled.
Then it calls `register()` from `api.js`.

```
User clicks Register
  → handleRegister() runs
  → Validates: username and password not empty
  → Calls register(username, password) from api.js
```

---

### Step 4 — Frontend Sends POST /register to FastAPI

`api.js` sends a POST request to `http://localhost:8000/register`
with the username and password serialized as a JSON body.

```js
// api.js — register function
export async function register(username, password) {
  const response = await fetch("http://localhost:8000/register", {
    method:  "POST",
    headers: { "Content-Type": "application/json" },
    body:    JSON.stringify({ username, password }),
  });
  return response.json();
}
```

**JSON sent to backend:**
```json
{ "username": "<username>", "password": "<password>" }
```

---

### Step 5 — FastAPI Processes Registration

The `/register` endpoint in `main.py` receives the request.
Pydantic validates that both fields are strings and not empty.
`insert_user()` from `database.py` is called.
It checks whether the username already exists.
If not, it inserts the new user into the `users` table in `finance.db`.

```python
# main.py — /register endpoint
@app.post("/register")
def register(user: User):
    result = insert_user(user.username, user.password)
    if result == "exists":
        return {"message": "Username already exists. Please choose another."}
    return {"message": "Registered successfully"}
```

**SQLite insert executed in database.py:**
```sql
INSERT INTO users (username, password) VALUES (?, ?)
```

**FastAPI returns:**
```json
{ "message": "Registered successfully" }
```

---

## PHASE 2 — User Login

### Step 6 — User Fills Login Form and Clicks Login

The user enters credentials and clicks Login.
`handleLogin()` in `App.jsx` validates the fields, then calls `login()` from `api.js`.

---

### Step 7 — Frontend Sends POST /login to FastAPI

```js
// api.js — login function
export async function login(username, password) {
  const response = await fetch("http://localhost:8000/login", {
    method:  "POST",
    headers: { "Content-Type": "application/json" },
    body:    JSON.stringify({ username, password }),
  });
  return response.json();
}
```

**JSON sent to backend:**
```json
{ "username": "<username>", "password": "<password>" }
```

---

### Step 8 — FastAPI Validates Credentials

The `/login` endpoint calls `get_user()` from `database.py`.
It queries the `users` table for a matching username and password combination.

```python
# main.py — /login endpoint
@app.post("/login")
def login(user: User):
    account = get_user(user.username, user.password)
    if account:
        return {"message": "Login success"}
    else:
        return {"message": "Invalid credentials"}
```

**SQLite query executed in database.py:**
```sql
SELECT * FROM users WHERE username = ? AND password = ?
```

---

### Step 9 — Frontend Handles Login Response

Back in `App.jsx`, `handleLogin()` checks the returned message.
If `"Login success"` → `setPage("dashboard")` switches the UI to the dashboard.
If not → an error message is displayed inside the card.

```js
// App.jsx — login response handler
const data = await login(username, password);
if (data.message === "Login success") {
  setPage("dashboard");        // ← user now sees the dashboard
} else {
  setError("Invalid username or password. Please try again.");
}
```

---

## PHASE 3 — Financial Data Entry

### Step 10 — User Enters Income, Debt, and Expenses

The dashboard renders three number inputs.
The user types their monthly income, total debt, and monthly expenses.
Each input updates its corresponding React state value.

```jsx
// App.jsx — financial data inputs
<input type="number" placeholder="Monthly Income ($)"
       onChange={(e) => setIncome(e.target.value)} />

<input type="number" placeholder="Total Debt ($)"
       onChange={(e) => setDebt(e.target.value)} />

<input type="number" placeholder="Monthly Expenses ($)"
       onChange={(e) => setExpenses(e.target.value)} />
```

---

### Step 11 — User Clicks Analyze

`handleAnalyze()` runs in `App.jsx`.
It validates that all 3 fields are filled and numeric.
It sets `loading = true` to show the spinner and disable the button.
Then it calls `analyze()` from `api.js`.

```js
// App.jsx — handleAnalyze validation and call
if (!income || !debt || !expenses)       → show error
if (isNaN(income) || isNaN(expenses))   → show error
setLoading(true)
const data = await analyze(income, debt, expenses)
setResult(data)
setLoading(false)
```

---

## PHASE 4 — FastAPI Backend Processing

### Step 12 — Frontend Sends POST /analyze to FastAPI

`api.js` serializes the 3 values as numbers and sends them to the backend.

```js
// api.js — analyze function
export async function analyze(income, debt, expenses) {
  const response = await fetch("http://localhost:8000/analyze", {
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
```

**JSON sent to backend:**
```json
{ "income": 5000, "debt": 15000, "expenses": 2500 }
```

---

### Step 13 — Pydantic Validates the Request

FastAPI's `FinancialData` Pydantic model enforces that all 3 fields are integers.
If any field is missing or the wrong type, FastAPI returns a 422 validation error
automatically before the endpoint function even runs.

```python
# main.py — Pydantic model
class FinancialData(BaseModel):
    income:   int
    debt:     int
    expenses: int
```

---

## PHASE 5 — Financial Calculation Engine

### Step 14 — prediction.py Runs All Calculations

`analyze_finances()` from `prediction.py` is called with the 3 validated values.
It runs 4 calculations and returns them all in a single dictionary.

```python
# main.py — Step 1
results = analyze_finances(data.income, data.debt, data.expenses)
```

**Calculation 1 — Debt Ratio:**
```
debt_ratio = (debt / income) × 100
           = (15000 / 5000) × 100
           = 100.0%  (capped at 100)
```

**Calculation 2 — Financial Score:**
```
monthly_debt_payment = debt / 36       = 15000 / 36 = 416.67
leftover             = income - expenses - monthly_debt_payment
                     = 5000 - 2500 - 416.67 = 2083.33
score                = (leftover / income) × 100
                     = (2083.33 / 5000) × 100 = 41.67
```

**Calculation 3 — Health Status:**
```
score 41.67 → falls in range 40–69 → "At Risk"
```

**Calculation 4 — Settlement Prediction (3-condition check):**
```
Condition A: income - expenses > 0       → 5000 - 2500 = 2500 > 0    ✓
Condition B: debt / income < 3           → 15000 / 5000 = 3.0 ≥ 3    ✗
Condition C: expenses / income < 0.5    → 2500 / 5000 = 0.5 ≥ 0.5   ✗
Conditions met: 1 → "Low Probability"
```

**prediction.py returns:**
```python
{
    "debt_ratio"      : 100.0,
    "financial_score" : 41.67,
    "health"          : "At Risk",
    "settlement"      : "Low Probability"
}
```

---

## PHASE 6 — Gemini AI Advice Generation

### Step 15 — ai_engine.py Sanitizes Inputs and Builds Prompts

`get_ai_advice()` from `ai_engine.py` is called next.
Before injecting values into any prompt, `_sanitize()` clamps all inputs
to safe integers between 0 and 10,000,000, blocking XSS and prompt injection.
Two separate prompts are sent to Gemini — one for recovery advice and one
for a debt negotiation strategy.

```python
# ai_engine.py — _sanitize prevents injection
def _sanitize(value):
    sanitized = int(float(str(value)))
    return max(0, min(sanitized, 10_000_000))
```

---

### Step 16 — Prompts Are Sent to Gemini 2.5 Flash

Each prompt includes the sanitized financial values, a role instruction,
a 2-sentence output constraint, and `max_output_tokens=200` to prevent
unbounded token consumption.

```python
# Prompt 1 — Financial Recovery Advice
"You are a professional financial advisor...
 Monthly Income: $5000 / Total Debt: $15000 / Monthly Expenses: $2500
 Give recovery advice in exactly 2 sentences."

# Prompt 2 — Debt Negotiation Strategy
"You are a debt negotiation specialist...
 Monthly Income: $5000 / Total Debt: $15000 / Monthly Expenses: $2500
 Provide a negotiation strategy in exactly 2 sentences."
```

---

### Step 17 — Gemini Returns AI-Generated Text

Gemini processes each prompt and returns a 2-sentence response.
`html.escape()` sanitizes the output before it is stored or returned,
preventing any XSS if Gemini's response contains special characters.
Both responses are joined with a blank line and returned as one string.

```python
# ai_engine.py — combined output
return f"{recovery}\n\n{negotiation}"
```

**Example AI response:**
```
Prioritize paying down your highest-interest debt first while cutting
discretionary spending to free up at least $500 more per month.

Contact your creditors and propose a structured repayment plan, highlighting
your commitment to repayment while requesting a temporary interest reduction.
```

---

## PHASE 7 — Database Storage

### Step 18 — Results Are Saved to SQLite

After calculations and AI advice are ready, `main.py` saves both to the database
in the correct order — financial data first to get its `finance_id`, then the AI
analysis using that ID as a foreign key.

```python
# main.py — Step 3: Save financial data
finance_id = insert_financial_data(
    user_id=1, income=5000, debt=15000,
    expenses=2500, financial_score=41.67
)

# main.py — Step 4: Save AI analysis linked to finance_id
insert_ai_analysis(
    finance_id=finance_id,
    health="At Risk",
    settlement="Low Probability",
    suggestion="Prioritize paying down..."
)
```

**Tables written to in finance.db:**
```
financial_data  ← income, debt, expenses, financial_score
ai_analysis     ← health, settlement, suggestion (linked via finance_id)
```

---

## PHASE 8 — Results Returned to Frontend Dashboard

### Step 19 — FastAPI Returns the Full JSON Response

After saving to the database, `/analyze` returns all 5 result fields to the frontend.

```python
# main.py — Step 5: Return results
return {
    "debt_ratio"      : 100.0,
    "financial_score" : 41.67,
    "health"          : "At Risk",
    "settlement"      : "Low Probability",
    "suggestion"      : "Prioritize paying down..."
}
```

---

### Step 20 — React Renders the Financial Report on the Dashboard

Back in `App.jsx`, `setResult(data)` stores the response.
`setLoading(false)` hides the spinner.
The result section renders with color-coded badges and the full AI advice block.

```jsx
// App.jsx — result display
{result && (
  <div className="results">
    <div className="result-row">
      <span>Debt Ratio</span>
      <span>{result.debt_ratio}%</span>          {/* 100.0% */}
    </div>
    <div className="result-row">
      <span>Financial Score</span>
      <span>{result.financial_score} / 100</span> {/* 41.67 / 100 */}
    </div>
    <span className="badge-risk">{result.health}</span>       {/* At Risk — yellow */}
    <span className="badge-critical">{result.settlement}</span> {/* Low — red */}
    <p className="advice-text">{result.suggestion}</p>        {/* AI text */}
  </div>
)}
```

**Badge colors applied automatically:**
```
health = "Good"      → badge-good     (green)
health = "At Risk"   → badge-risk     (yellow)
health = "Critical"  → badge-critical (red)
```

---

## Complete Workflow Summary

| Step | Phase | Action | File |
|------|-------|--------|------|
| 1    | Launch   | Browser opens app at localhost:5173              | index.html       |
| 2    | Register | User fills username and password                 | App.jsx          |
| 3    | Register | handleRegister() validates inputs                | App.jsx          |
| 4    | Register | POST /register sent with JSON body               | api.js           |
| 5    | Register | FastAPI inserts user into users table            | main.py / database.py |
| 6    | Login    | User fills credentials and clicks Login          | App.jsx          |
| 7    | Login    | POST /login sent with JSON body                  | api.js           |
| 8    | Login    | FastAPI queries users table for match            | main.py / database.py |
| 9    | Login    | "Login success" → setPage("dashboard")           | App.jsx          |
| 10   | Input    | User enters income, debt, expenses               | App.jsx          |
| 11   | Input    | handleAnalyze() validates and calls analyze()    | App.jsx          |
| 12   | Analyze  | POST /analyze sent with numeric JSON body        | api.js           |
| 13   | Analyze  | Pydantic validates all 3 fields as integers      | main.py          |
| 14   | Calc     | analyze_finances() computes all 4 metrics        | prediction.py    |
| 15   | AI       | _sanitize() clamps inputs, builds prompts        | ai_engine.py     |
| 16   | AI       | Two prompts sent to Gemini 2.5 Flash             | ai_engine.py     |
| 17   | AI       | Gemini returns advice, html.escape() applied     | ai_engine.py     |
| 18   | Database | Financial data and AI results saved to SQLite    | database.py      |
| 19   | Response | FastAPI returns 5-field JSON to frontend         | main.py          |
| 20   | Display  | React renders color-coded report on dashboard    | App.jsx          |

---

*Generated for: FinRelief AI — AI Powered Debt Relief and Financial Recovery Platform*
*Document Type: Project Workflow — Internship Project Submission*
