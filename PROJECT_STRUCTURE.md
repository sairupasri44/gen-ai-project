# FinRelief AI — Modular Project Folder Structure
## AI Powered Debt Relief and Financial Recovery Platform

---

## Complete Folder Structure

```
gen-ai-project/                         ← Root project folder
│
├── backend/                            ← Python FastAPI backend (server-side)
│   ├── main.py                         ← Main application entry point, all API routes
│   ├── ai_engine.py                    ← Google Gemini AI integration module
│   ├── prediction.py                   ← Settlement prediction logic engine
│   ├── database.py                     ← SQLite database connection and table creation
│   ├── finance.db                      ← SQLite database file (auto-generated)
│   ├── requirements.txt                ← Python package dependencies list
│   ├── test_ai.py                      ← Unit tests for AI engine
│   └── .env                            ← Secret environment variables (API keys)
│
├── frontend/                           ← React.js + Vite frontend (client-side)
│   ├── public/                         ← Static public assets
│   │   ├── favicon.svg                 ← Browser tab icon
│   │   └── icons.svg                   ← Reusable SVG icon set
│   │
│   ├── src/                            ← All React source code lives here
│   │   ├── assets/                     ← Images, logos, and static media
│   │   ├── App.jsx                     ← Root React component, all pages and logic
│   │   ├── App.css                     ← Styles for App.jsx (card, buttons, inputs)
│   │   ├── main.jsx                    ← React DOM entry point, mounts App.jsx
│   │   └── index.css                   ← Global base styles, CSS variables, themes
│   │
│   ├── index.html                      ← HTML shell that loads the React app
│   ├── vite.config.js                  ← Vite bundler configuration
│   ├── package.json                    ← Node.js dependencies and npm scripts
│   ├── package-lock.json               ← Locked dependency versions
│   └── .gitignore                      ← Files Git should not track (node_modules)
│
├── ERD.md                              ← Entity Relationship Diagram documentation
├── schema.sql                          ← SQL database schema with table definitions
├── PREREQUISITES.md                    ← Hardware and software requirements
├── README.md                           ← Project overview and setup instructions
├── .gitignore                          ← Root-level Git ignore rules
├── package.json                        ← Root-level scripts (if any)
└── package-lock.json                   ← Root-level lock file
```

---

## Backend File Explanations

### `main.py` — API Entry Point and Route Controller
The heart of the FastAPI backend. This is the first file that runs when the server starts.

**What it does:**
- Creates the FastAPI application instance
- Registers CORS middleware to allow the React frontend to communicate with the backend
- Defines Pydantic data models (User, FinancialData) to validate incoming request data
- Declares all three API endpoints that the frontend calls

**API Endpoints defined inside main.py:**

| Endpoint    | Method | Purpose                                          |
|-------------|--------|--------------------------------------------------|
| `/`         | GET    | Health check — confirms the server is running    |
| `/register` | POST   | Accepts username and password, saves to accounts table |
| `/login`    | POST   | Validates credentials against the database       |
| `/analyze`  | POST   | Receives income, debt, expenses — runs full analysis pipeline |

**How /analyze works internally:**
```
Request arrives → Save to database → Calculate score
→ Call predict() → Call get_ai_advice() → Return JSON result
```

**Key imports in main.py:**
```python
from database   import insert_user, get_user, insert_financial_data, insert_ai_analysis
from prediction import analyze_finances
from ai_engine  import get_ai_advice
from dotenv     import load_dotenv
```

---

### `ai_engine.py` — Google Gemini AI Integration Module
Handles all communication with the Google Gemini API with full security hardening.

**What it does:**
- Loads `GEMINI_API_KEY` from `.env` via `python-dotenv`
- `_sanitize(value)` clamps all numeric inputs to safe integers (0–10,000,000)
  blocking XSS and prompt injection before values touch any prompt string
- `_call_gemini(prompt)` is the single wrapper for all API calls — inlines
  `max_output_tokens=200` on every call to prevent LLM unbounded consumption
- `html.escape()` is applied to all Gemini responses before returning
- Two prompt functions target different advice types:

| Function | Gemini Role | Output |
|---|---|---|
| `get_recovery_advice()` | Professional financial advisor | 2-sentence recovery steps |
| `get_negotiation_strategy()` | Debt negotiation specialist | 2-sentence creditor tactics |
| `get_ai_advice()` | Master function (called by main.py) | Combined response |

**Why it is a separate module:**
Isolating AI logic means the provider (Gemini → OpenAI etc.) can be swapped
without touching any other file.

---

### `prediction.py` — Financial Calculation and Settlement Prediction Engine
A pure Python calculation module with no external dependencies.

**What it does:**
- `calculate_debt_ratio(income, debt)` — `(debt/income)×100`, capped at 100
- `calculate_financial_score(income, debt, expenses)` — leftover income ratio over 36-month debt payoff
- `calculate_health(score)` — maps score to Good / At Risk / Critical
- `predict_settlement(income, debt, expenses)` — 3-condition classifier:
  - Condition A: income − expenses > 0 (monthly surplus exists)
  - Condition B: debt / income < 3 (debt less than 3× monthly income)
  - Condition C: expenses / income < 0.5 (expenses below 50% of income)
  - 3 met → High, 2 met → Medium, 1 or 0 → Low Probability
- `analyze_finances(income, debt, expenses)` — master function called by `main.py`

**Why it is a separate module:**
All financial logic is isolated here. The prediction model can be upgraded to
a machine learning classifier without changing any other file.

---

### `database.py` — Database Schema and Insert Functions
Manages all SQLite database operations using a connection-per-function pattern.
Every function opens its own scoped `with sqlite3.connect()` block, guaranteeing
connection closure on every exit path — including exceptions.

**What it does:**
- Defines `DB_PATH = "finance.db"` as the single source of truth for the DB file path
- Creates all 3 tables on import via `create_tables()`
- Provides 4 clean functions used by `main.py`

**Functions exported:**

| Function | Called By | Returns |
|---|---|---|
| `insert_user(username, password)` | POST /register | `"success"` / `"exists"` / `"error"` |
| `get_user(username, password)` | POST /login | user row or `None` |
| `insert_financial_data(...)` | POST /analyze | `finance_id` int |
| `insert_ai_analysis(...)` | POST /analyze | `analysis_id` int |

**Tables created:**

```sql
users          — user_id, username (UNIQUE), password
financial_data — finance_id, user_id (FK), income, debt, expenses, financial_score
ai_analysis    — analysis_id, finance_id (FK), health, settlement, suggestion
```

---

### `requirements.txt` — Python Dependency List
Lists every Python package the backend needs to run. Used by pip to install
all dependencies with a single command.

**Current dependencies:**

| Package            | Purpose                                           |
|--------------------|---------------------------------------------------|
| fastapi            | Web framework for building the REST API           |
| uvicorn            | ASGI server that runs the FastAPI application     |
| pydantic           | Data validation for request and response models   |
| python-dotenv      | Loads environment variables from the .env file    |
| google-generativeai| Official Google Gemini AI client library          |

**Install command:**
```bash
pip install -r requirements.txt
```

---

### `.env` — Environment Variables File
Stores secret configuration values that must never be hardcoded in source code
and must never be committed to a Git repository.

**Current variable:**
```
GEMINI_API_KEY=your_gemini_api_key_here
```

**Security rules:**
- This file must be listed in `.gitignore`
- Share only a `.env.example` file with placeholder values with teammates
- Regenerate the key immediately if it is ever accidentally exposed

---

### `finance.db` — SQLite Database File
The actual database file automatically created by database.py when the backend
starts for the first time. It is a single binary file that stores all tables and data.

- No separate database server installation is needed
- Located inside the backend/ folder
- Should be added to `.gitignore` to avoid committing user data to version control

---

### `test_ai.py` — AI Engine Unit Tests
Contains test cases to verify that the Gemini AI integration is working correctly
before running the full application.

---

## Frontend File Explanations

### `App.jsx` — Root React Component (All Pages and Logic)
The most important frontend file. Contains the entire application UI and all
business logic for the three pages: Login, Register, and Dashboard.

**What it does:**
- Manages application state using React useState hooks
- Controls which page is currently displayed using a `page` state variable
- Handles all three async API calls to the FastAPI backend
- Renders the financial results returned from the /analyze endpoint

**State variables managed:**

| State Variable | Type   | Purpose                                      |
|----------------|--------|----------------------------------------------|
| page           | string | Controls which page renders: login/dashboard |
| username       | string | Stores the typed username value              |
| password       | string | Stores the typed password value              |
| income         | string | Stores the typed monthly income              |
| debt           | string | Stores the typed total debt amount           |
| expenses       | string | Stores the typed monthly expenses            |
| result         | object | Stores the JSON response from /analyze       |

**Functions defined:**

| Function  | Calls API Endpoint | Purpose                                       |
|-----------|--------------------|-----------------------------------------------|
| register()| POST /register     | Sends username + password to create account   |
| login()   | POST /login        | Validates credentials, switches page on success |
| analyze() | POST /analyze      | Sends financial data, stores result in state  |

**Page rendering logic:**
```
page === "login"     → Renders Login/Register card
page === "dashboard" → Renders Financial Input form + Results card
```

---

### `App.css` — Component Styles for App.jsx
Provides all visual styling for the FinRelief AI user interface.

**What it styles:**

| Class / Selector | Purpose                                              |
|------------------|------------------------------------------------------|
| body             | Sets dark navy background color (#071226) for whole page |
| .container       | Flexbox centering — keeps the card in the middle of the screen |
| .card            | Dark card panel (#121d35) with rounded corners and shadow |
| h1, h2, h3, p    | Sets all text to white for dark theme readability    |
| input            | Styles all form input fields with padding and border radius |
| button           | Indigo (#4f46e5) styled action buttons               |
| button:hover     | Darker indigo (#3730a3) on mouse hover for feedback  |
| .results         | Left-aligned results section inside the dashboard card |
| .buttons         | Flex row layout for Login and Register button pair   |

**Color palette used:**

| Variable  | Hex Code  | Used For                  |
|-----------|-----------|---------------------------|
| Background| #071226   | Full page background       |
| Card      | #121d35   | Main content card          |
| Primary   | #4f46e5   | Buttons                    |
| Hover     | #3730a3   | Button hover state         |
| Text      | #ffffff   | All text inside cards      |

---

### `main.jsx` — React DOM Entry Point
The file that bootstraps the entire React application. It is the bridge between
the HTML file and the React component tree.

**What it does:**
- Imports React StrictMode for development warnings
- Selects the `<div id="root">` element from index.html
- Mounts the App component into that div using createRoot
- Imports index.css to apply global base styles

**Code:**
```jsx
createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>
)
```

This file is rarely modified. It simply connects index.html to App.jsx.

---

### `index.css` — Global Base Styles and CSS Variables
Defines the foundational CSS for the entire application including CSS custom
properties (variables), typography settings, and light/dark theme support.

**What it defines:**

| Section              | Purpose                                              |
|----------------------|------------------------------------------------------|
| :root variables      | CSS color variables: --text, --bg, --accent, --border|
| Dark mode media query| Automatically switches colors for dark theme users   |
| body                 | Removes default browser margin                       |
| #root                | Centers the app with max-width and border layout     |
| h1, h2 typography    | Font size, weight, and letter spacing for headings   |
| code, .counter       | Monospace font styling for code display elements     |

App.css overrides many of these base styles for the FinRelief dark navy theme.

---

### `index.html` — HTML Application Shell
The single HTML page that the browser loads. Contains no visible content by
itself — it just provides the mount point for the React application.

**Key elements:**
```html
<div id="root"></div>              ← React mounts the entire app here
<script src="/src/main.jsx">       ← Loads the React entry point
```

Vite injects the compiled JavaScript bundles into this file automatically
during both development and production builds.

---

### `vite.config.js` — Vite Bundler Configuration
Configures the Vite build tool that powers the frontend development server
and production build process.

**Current configuration:**
```js
import { defineConfig } from 'vite'
import react  from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()]   // Enables JSX transform and React Fast Refresh
})
```

**What Vite provides:**
- Instant hot module replacement (HMR) during development
- Optimized production bundle when running `npm run build`
- Built-in development server at http://localhost:5173

---

### `package.json` — Node.js Project Manifest
Defines the project metadata, all npm dependencies, and available scripts
for the frontend.

**Available scripts:**

| Script          | Command         | Purpose                                    |
|-----------------|-----------------|--------------------------------------------|
| npm run dev     | vite            | Starts the development server on port 5173 |
| npm run build   | vite build      | Creates an optimized production bundle     |
| npm run preview | vite preview    | Previews the production build locally      |
| npm run lint    | oxlint          | Runs the linter to check code quality      |

**Frontend dependencies:**

| Package        | Version  | Purpose                              |
|----------------|----------|--------------------------------------|
| react          | ^19.2.7  | Core React library                   |
| react-dom      | ^19.2.7  | React DOM renderer for browsers      |
| vite           | ^8.1.0   | Frontend build tool and dev server   |
| @vitejs/plugin-react | ^6.0.2 | Vite plugin that enables React JSX |

---

## How All Files Connect Together

```
index.html
    └── loads → main.jsx
                    └── mounts → App.jsx
                                    ├── imports → App.css      (component styles)
                                    ├── imports → index.css    (global base styles)
                                    └── fetches →
                                          ├── POST /register  → main.py → database.py
                                          ├── POST /login     → main.py → database.py
                                          └── POST /analyze   → main.py
                                                                    ├── database.py    (save data)
                                                                    ├── prediction.py  (score → settlement)
                                                                    └── ai_engine.py   (Gemini AI advice)
```

---

## Module Responsibility Summary

| File            | Layer     | Single Responsibility                          |
|-----------------|-----------|------------------------------------------------|
| main.py         | Backend   | Route definitions and request/response handling|
| ai_engine.py    | Backend   | Google Gemini API communication                |
| prediction.py   | Backend   | Financial score to settlement classification   |
| database.py     | Backend   | SQLite connection and table initialization     |
| App.jsx         | Frontend  | All UI pages, state management, API calls      |
| App.css         | Frontend  | FinRelief dark theme visual styling            |
| main.jsx        | Frontend  | React app bootstrap and DOM mounting           |
| index.css       | Frontend  | Global typography and CSS variable definitions |
| vite.config.js  | Config    | Vite bundler and dev server setup              |
| requirements.txt| Config    | Python backend package dependencies            |
| .env            | Config    | Secret API keys and environment variables      |
| finance.db      | Database  | SQLite persistent data storage file            |

---

*Generated for: FinRelief AI — AI Powered Debt Relief and Financial Recovery Platform*
*Tech Stack: React 19 + Vite 8 | FastAPI | SQLite | Google Gemini 2.5 Flash*
