# Frontend Setup Guide
## FinRelief AI — React + Vite Frontend
### AI Powered Debt Relief and Financial Recovery Platform

---

## Frontend Folder Structure

```
gen-ai-project/
└── frontend/
    ├── public/
    │   ├── favicon.svg          ← Browser tab icon for FinRelief AI
    │   └── icons.svg            ← Shared SVG icon assets
    ├── src/
    │   ├── assets/              ← Static assets folder (images, logos)
    │   ├── App.jsx              ← Main component: Login page + Dashboard page
    │   ├── App.css              ← Styles for card, inputs, buttons, results panel
    │   ├── main.jsx             ← React entry point, mounts App into index.html
    │   └── index.css            ← Global CSS variables, typography, root layout
    ├── index.html               ← HTML shell with <div id="root"> for React to mount
    ├── vite.config.js           ← Vite configuration, registers React plugin
    ├── package.json             ← Project metadata, npm scripts, dependencies
    └── package-lock.json        ← Locked dependency versions for reproducibility
```

---

## Step 1 — Verify Node.js and npm Are Installed

Open a terminal in VS Code (`Ctrl + `` `) and run:

```bash
node --version
npm --version
```

Expected output:
```
v18.0.0   (or higher)
9.0.0     (or higher)
```

If Node.js is not installed, download it from https://nodejs.org
Choose the **LTS version** for stability.

---

## Step 2 — Navigate to the Frontend Folder

```bash
cd gen-ai-project/frontend
```

Confirm you are in the right folder:
```bash
dir
```

You should see: `package.json`, `index.html`, `vite.config.js`, `src/`

---

## Step 3 — Install Frontend Dependencies

Install all packages listed in `package.json`:

```bash
npm install
```

This installs the following packages into a `node_modules/` folder:

**Production Dependencies:**

| Package      | Version   | Purpose                                             |
|--------------|-----------|-----------------------------------------------------|
| react        | ^19.2.7   | Core React library for building UI components       |
| react-dom    | ^19.2.7   | Renders React components into the browser DOM       |

**Development Dependencies:**

| Package               | Version   | Purpose                                             |
|-----------------------|-----------|-----------------------------------------------------|
| vite                  | ^8.1.0    | Lightning-fast build tool and dev server            |
| @vitejs/plugin-react  | ^6.0.2    | Enables JSX and React Fast Refresh in Vite          |
| @types/react          | ^19.2.17  | TypeScript type definitions for React               |
| @types/react-dom      | ^19.2.3   | TypeScript type definitions for React DOM           |
| oxlint                | ^1.69.0   | Fast JavaScript and JSX linter                      |

After installation, a `node_modules/` folder will appear in your frontend directory.

> Never commit `node_modules/` to Git — it is already in `.gitignore`.

---

## Step 4 — Understand Each Frontend File

### index.html
The HTML shell that loads the entire React application.
Vite injects the compiled JavaScript into this file at build time.

```html
<body>
  <div id="root"></div>                          <!-- React mounts here -->
  <script type="module" src="/src/main.jsx"></script>
</body>
```

- `<div id="root">` is the single container React renders everything into
- The page title is set here: change `<title>frontend</title>` to `<title>FinRelief AI</title>`

---

### main.jsx
The React entry point. It connects React to the `index.html` root div and wraps
the entire app in `StrictMode` for development warnings.

```jsx
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
```

- `createRoot` finds the `<div id="root">` in `index.html` and hands it to React
- `<App />` is the top-level component that controls the entire application
- `index.css` is imported here so global styles apply to the entire app

---

### App.jsx
The core component of the entire frontend. It contains two pages managed by a
`page` state variable — no router library is needed for this project.

**State variables declared at the top:**

```jsx
const [page, setPage]         = useState("login");   // controls which page shows
const [username, setUsername] = useState("");         // login form
const [password, setPassword] = useState("");         // login form
const [income, setIncome]     = useState("");         // dashboard form
const [debt, setDebt]         = useState("");         // dashboard form
const [expenses, setExpenses] = useState("");         // dashboard form
const [result, setResult]     = useState(null);       // stores API response
```

**Three async functions handle all API communication:**

| Function    | API Endpoint              | HTTP Method | What It Does                              |
|-------------|---------------------------|-------------|-------------------------------------------|
| `register()`| `POST /register`          | POST        | Saves username and password to SQLite     |
| `login()`   | `POST /login`             | POST        | Validates credentials, switches to dashboard |
| `analyze()` | `POST /analyze`           | POST        | Sends financial data, receives AI results |

**Page rendering logic:**

```jsx
if (page === "login") {
  return ( /* Login Page JSX */ );
}
return ( /* Dashboard Page JSX */ );
```

The app starts on the login page. After a successful login, `setPage("dashboard")`
switches the view to the dashboard — no page reload occurs.

---

### App.css
Styles every visible element in the application. The dark navy colour scheme
(`#071226` background, `#121d35` card) is defined here.

| Class / Selector | What It Styles                                               |
|------------------|--------------------------------------------------------------|
| `body`           | Deep navy background (`#071226`), global font (Arial)        |
| `.container`     | Full viewport flex layout, centres the card vertically       |
| `.card`          | White-on-dark rounded card, 500px wide, indigo shadow        |
| `input`          | Full-width rounded inputs, 12px padding, no border           |
| `button`         | Indigo (`#4f46e5`) rounded buttons with hover darkening      |
| `button:hover`   | Darkens to `#3730a3` on mouse hover                          |
| `.results`       | Left-aligned results block with top margin                   |
| `.buttons`       | Flex row for centering multiple buttons side by side         |

---

### index.css
Global CSS variables and typography system for the entire application.
Defines CSS custom properties used across the project:

```css
:root {
  --accent: #aa3bff;       /* Purple accent colour */
  --bg: #fff;              /* Light mode background */
  --text: #6b6375;         /* Body text colour */
}
```

Also includes a `prefers-color-scheme: dark` media query for automatic
dark mode support on devices that have it enabled.

---

### vite.config.js
Vite build tool configuration. Registers the React plugin which enables:
- JSX syntax transformation
- React Fast Refresh (hot module replacement during development)

```js
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
})
```

No additional configuration is needed for this project.

---

### package.json
Defines project metadata and available npm scripts:

```json
{
  "scripts": {
    "dev"    : "vite",          // starts development server on localhost:5173
    "build"  : "vite build",    // compiles production-ready files into dist/
    "lint"   : "oxlint",        // runs the linter to check for code issues
    "preview": "vite preview"   // serves the production build locally for testing
  }
}
```

---

## Step 5 — Understand the Login Page

The login page renders when `page === "login"`. It contains:
- A username text input
- A password input with `type="password"` for masking
- A Login button that calls `login()`
- A Register button that calls `register()`

**How Register works:**
```
User fills username + password
        ↓
register() sends POST to http://localhost:8000/register
        ↓
FastAPI saves username + password to SQLite accounts table
        ↓
alert("Registered Successfully") shown to user
```

**How Login works:**
```
User fills username + password
        ↓
login() sends POST to http://localhost:8000/login
        ↓
FastAPI queries accounts table for matching credentials
        ↓
If match found → setPage("dashboard") → dashboard renders
If no match   → alert("Wrong username or password")
```

---

## Step 6 — Understand the Dashboard Page

The dashboard renders when `page === "dashboard"`. It contains:
- An Income number input
- A Debt number input
- An Expenses number input
- An Analyze button that calls `analyze()`
- A Financial Report section that appears after results load

**How Analyze works:**
```
User enters income, debt, expenses
        ↓
analyze() converts values to Number and sends POST to http://localhost:8000/analyze
        ↓
FastAPI runs financial calculation → prediction.py → ai_engine.py (Gemini)
        ↓
JSON response received:
{
  debt_ratio      : 40,
  financial_score : 70,
  health          : "Good",
  settlement      : "Medium Probability",
  suggestion      : "AI-generated advice text..."
}
        ↓
setResult(data) triggers re-render
        ↓
Financial Report section appears with all five values displayed
```

---

## Step 7 — How the Fetch API Connects Frontend to Backend

All three API calls in `App.jsx` follow the exact same pattern:

```jsx
const response = await fetch("http://localhost:8000/analyze", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",   // tells backend to expect JSON
  },
  body: JSON.stringify({                  // converts JS object to JSON string
    income: Number(income),
    debt:   Number(debt),
    expenses: Number(expenses),
  }),
});

const data = await response.json();       // parses JSON response back to JS object
setResult(data);                          // stores result in React state
```

**Why `Number(income)` is used:**
Input values from HTML inputs are always strings. The FastAPI backend expects
`income`, `debt`, and `expenses` as integers. `Number()` converts them before sending.

**Why CORS is needed:**
The frontend runs on `http://localhost:5173` and the backend runs on
`http://localhost:8000`. Browsers block cross-origin requests by default.
The `CORSMiddleware` in `main.py` with `allow_origins=["*"]` removes this restriction.

---

## Step 8 — Run the Frontend Development Server

Make sure your terminal is inside the frontend folder:

```bash
cd gen-ai-project/frontend
npm run dev
```

Expected terminal output:
```
  VITE v8.1.0  ready in 312 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

Open your browser and go to: **http://localhost:5173**

You will see the FinRelief AI login page.

> Vite supports Hot Module Replacement (HMR). Any changes you save in
> `App.jsx` or `App.css` will instantly reflect in the browser without a full reload.

---

## Step 9 — Run Both Servers Together

The frontend and backend must both be running at the same time.
Open **two separate terminals** in VS Code:

**Terminal 1 — Backend:**
```bash
cd gen-ai-project/backend
venv\Scripts\activate
uvicorn main:app --reload
```
Backend runs at: `http://localhost:8000`

**Terminal 2 — Frontend:**
```bash
cd gen-ai-project/frontend
npm run dev
```
Frontend runs at: `http://localhost:5173`

---

## Step 10 — End-to-End Test Walkthrough

Follow these steps to test the complete application flow:

```
1. Open http://localhost:5173 in your browser
        ↓
2. Enter a username and password → click Register
   → "Registered Successfully" alert appears
        ↓
3. Enter the same username and password → click Login
   → Dashboard page loads
        ↓
4. Enter test values:
   Income   : 5000
   Debt     : 15000
   Expenses : 2500
        ↓
5. Click Analyze
   → Loading begins, fetch sends data to http://localhost:8000/analyze
        ↓
6. Financial Report appears:
   Debt Ratio      : 40
   Financial Score : 70
   Health          : Good
   Settlement      : Medium Probability
   AI Advice       : [Gemini-generated financial advice]
```

---

## Common Errors and Fixes

| Error                                        | Cause                                    | Fix                                                        |
|----------------------------------------------|------------------------------------------|------------------------------------------------------------|
| `npm : command not found`                    | Node.js not installed                    | Download and install Node.js from https://nodejs.org       |
| `Failed to fetch` in browser console        | Backend not running                      | Start backend with `uvicorn main:app --reload`             |
| `CORS error` in browser console             | Backend CORS not configured              | Confirm `allow_origins=["*"]` is set in `main.py`         |
| Blank page at `localhost:5173`              | JavaScript error in App.jsx              | Open browser DevTools (`F12`) → Console tab for details    |
| `node_modules not found`                    | npm install not run                      | Run `npm install` inside the frontend folder               |
| AI Advice shows `"AI failed"`               | Gemini API key missing or expired        | Check `.env` file in backend folder has a valid key        |
| Login always shows wrong password alert     | User not registered yet                  | Click Register first before attempting to Login            |
| `NaN` sent to backend for income/debt       | Input left empty before clicking Analyze | Always fill all three fields before clicking Analyze       |

---

## Quick Reference — All Commands

```bash
# Navigate to frontend folder
cd gen-ai-project/frontend

# Install all dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build locally
npm run preview

# Run linter
npm run lint
```

---

*Generated for: FinRelief AI — AI Powered Debt Relief and Financial Recovery Platform*
*Internship Project Documentation — Frontend Setup Guide*
