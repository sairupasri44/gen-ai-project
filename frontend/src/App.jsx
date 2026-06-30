import { useState } from "react";
import "./App.css";
import { register, login, analyze } from "./api";

function App() {

  // ── Page State ─────────────────────────────────────────────────────────────
  // Controls which page is shown: "login" or "dashboard"
  const [page, setPage] = useState("login");

  // ── Login / Register States ────────────────────────────────────────────────
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  // ── Dashboard States ───────────────────────────────────────────────────────
  const [income,   setIncome]   = useState("");
  const [debt,     setDebt]     = useState("");
  const [expenses, setExpenses] = useState("");

  // ── UI Feedback States ─────────────────────────────────────────────────────
  const [result,  setResult]  = useState(null);    // Stores analyze() response
  const [loading, setLoading] = useState(false);   // Shows loading spinner
  const [error,   setError]   = useState("");      // Shows error messages


  // ── HANDLER 1: handleRegister ──────────────────────────────────────────────
  //
  // Validates that username and password are not empty.
  // Calls register() from api.js → POST /register.
  // Displays the backend message as feedback to the user.
  // ──────────────────────────────────────────────────────────────────────────

  const handleRegister = async () => {
    setError("");

    if (!username || !password) {
      setError("Please enter a username and password to register.");
      return;
    }

    try {
      const data = await register(username, password);
      alert(data.message);
    } catch {
      setError("Registration failed. Make sure the backend is running.");
    }
  };


  // ── HANDLER 2: handleLogin ─────────────────────────────────────────────────
  //
  // Validates that username and password are not empty.
  // Calls login() from api.js → POST /login.
  // On "Login success" → switches page state to "dashboard".
  // On failure → shows an error message below the form.
  // ──────────────────────────────────────────────────────────────────────────

  const handleLogin = async () => {
    setError("");

    if (!username || !password) {
      setError("Please enter your username and password.");
      return;
    }

    try {
      const data = await login(username, password);

      if (data.message === "Login success") {
        setPage("dashboard");
      } else {
        setError("Invalid username or password. Please try again.");
      }
    } catch {
      setError("Login failed. Make sure the backend is running.");
    }
  };


  // ── HANDLER 3: handleAnalyze ───────────────────────────────────────────────
  //
  // Validates that income, debt, and expenses are filled and numeric.
  // Shows a loading spinner while waiting for the backend response.
  // Calls analyze() from api.js → POST /analyze.
  // Stores the full result object in state to display on the dashboard.
  // ──────────────────────────────────────────────────────────────────────────

  const handleAnalyze = async () => {
    setError("");
    setResult(null);

    if (!income || !debt || !expenses) {
      setError("Please fill in all three fields: Income, Debt, and Expenses.");
      return;
    }

    if (isNaN(income) || isNaN(debt) || isNaN(expenses)) {
      setError("Income, Debt, and Expenses must be numbers.");
      return;
    }

    try {
      setLoading(true);
      const data = await analyze(income, debt, expenses);
      setResult(data);
    } catch {
      setError("Analysis failed. Make sure the backend is running.");
    } finally {
      setLoading(false);
    }
  };


  // ── LOGIN PAGE ─────────────────────────────────────────────────────────────

  if (page === "login") {
    return (
      <div className="container">
        <div className="card">

          <h1>FinRelief AI</h1>
          <p className="subtitle">AI Powered Debt Relief Platform</p>

          {/* Username Input */}
          <input
            type="text"
            placeholder="Username"
            onChange={(e) => setUsername(e.target.value)}
          />

          {/* Password Input */}
          <input
            type="password"
            placeholder="Password"
            onChange={(e) => setPassword(e.target.value)}
          />

          {/* Error Message */}
          {error && <p className="error">{error}</p>}

          {/* Action Buttons */}
          <div className="buttons">
            <button onClick={handleLogin}>Login</button>
            <button className="btn-secondary" onClick={handleRegister}>Register</button>
          </div>

        </div>
      </div>
    );
  }


  // ── DASHBOARD PAGE ─────────────────────────────────────────────────────────

  return (
    <div className="container">
      <div className="card">

        <h1>FinRelief AI</h1>
        <p className="subtitle">Enter your financial details below</p>

        {/* Income Input */}
        <input
          type="number"
          placeholder="Monthly Income ($)"
          value={income}
          onChange={(e) => setIncome(e.target.value)}
        />

        {/* Debt Input */}
        <input
          type="number"
          placeholder="Total Debt ($)"
          value={debt}
          onChange={(e) => setDebt(e.target.value)}
        />

        {/* Expenses Input */}
        <input
          type="number"
          placeholder="Monthly Expenses ($)"
          value={expenses}
          onChange={(e) => setExpenses(e.target.value)}
        />

        {/* Error Message */}
        {error && <p className="error">{error}</p>}

        {/* Analyze Button */}
        <div className="buttons">
          <button onClick={handleAnalyze} disabled={loading}>
            {loading ? "Analyzing..." : "Analyze"}
          </button>
        </div>

        {/* Loading Spinner */}
        {loading && (
          <div className="spinner-container">
            <div className="spinner"></div>
            <p className="loading-text">Getting your financial report...</p>
          </div>
        )}

        {/* ── Financial Report ─────────────────────────────────────────────── */}
        {/* Shown only after a successful analyze() response                   */}

        {result && (
          <div className="results">

            <h2>Financial Report</h2>

            {/* Debt Ratio */}
            <div className="result-row">
              <span className="result-label">Debt Ratio</span>
              <span className="result-value">{result.debt_ratio}%</span>
            </div>

            {/* Financial Score */}
            <div className="result-row">
              <span className="result-label">Financial Score</span>
              <span className="result-value">{result.financial_score} / 100</span>
            </div>

            {/* Health Status — color coded by value */}
            <div className="result-row">
              <span className="result-label">Health Status</span>
              <span className={`result-badge ${result.health === "Good"
                  ? "badge-good"
                  : result.health === "At Risk"
                  ? "badge-risk"
                  : "badge-critical"
              }`}>
                {result.health}
              </span>
            </div>

            {/* Settlement Probability — color coded by value */}
            <div className="result-row">
              <span className="result-label">Settlement</span>
              <span className={`result-badge ${result.settlement.includes("High")
                  ? "badge-good"
                  : result.settlement.includes("Medium")
                  ? "badge-risk"
                  : "badge-critical"
              }`}>
                {result.settlement}
              </span>
            </div>

            {/* AI Advice — full text block */}
            <div className="advice-box">
              <p className="advice-label">AI Financial Advice</p>
              <p className="advice-text">{result.suggestion}</p>
            </div>

          </div>
        )}

      </div>
    </div>
  );
}

export default App;
