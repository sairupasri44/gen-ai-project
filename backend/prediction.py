# prediction.py
# FinRelief AI — Financial Calculation and Settlement Prediction Engine
# -----------------------------------------------------------------------
# Inputs  : income, debt, expenses
# Outputs : debt_ratio, financial_score, health, settlement probability
# -----------------------------------------------------------------------


# ── FORMULA 1: Debt Ratio ────────────────────────────────────────────────────
#
#   Formula : debt_ratio = (debt / income) * 100
#
#   Purpose:
#     Measures how large the total debt is relative to monthly income.
#     A high debt ratio means the person owes much more than they earn.
#
#   Thresholds:
#     Below  40%  →  Low debt burden    (healthy)
#     40% – 79%   →  Moderate burden    (manageable)
#     80% or more →  High debt burden   (serious)
#
#   Example:
#     income = 5000,  debt = 15000
#     debt_ratio = (15000 / 5000) * 100 = 300% → capped at 100 for display
#
#     income = 5000,  debt = 2000
#     debt_ratio = (2000  / 5000) * 100 = 40%  → moderate
# ─────────────────────────────────────────────────────────────────────────────

def calculate_debt_ratio(income, debt):
    if income <= 0:
        return 100.0                               # No income = worst case

    ratio = (debt / income) * 100
    return round(min(ratio, 100.0), 2)             # Cap display at 100%


# ── FORMULA 2: Financial Score ───────────────────────────────────────────────
#
#   Formula:
#     Step 1 — monthly_debt_payment = debt / 36
#              Assumes user pays off all debt evenly over 36 months (3 years)
#
#     Step 2 — leftover = income - expenses - monthly_debt_payment
#              Money remaining after all monthly obligations
#
#     Step 3 — score = (leftover / income) * 100
#              Expresses leftover as a percentage of income
#
#   Purpose:
#     Shows how much breathing room the user has each month.
#     More leftover income = higher score = better financial position.
#
#   Score is clamped between 0 and 100.
#
#   Example:
#     income   = 5000
#     debt     = 15000 → monthly_debt_payment = 15000 / 36 = 416.67
#     expenses = 2500
#     leftover = 5000 - 2500 - 416.67 = 2083.33
#     score    = (2083.33 / 5000) * 100 = 41.67
# ─────────────────────────────────────────────────────────────────────────────

def calculate_financial_score(income, debt, expenses):
    if income <= 0:
        return 0.0                                 # No income = score of 0

    monthly_debt_payment = debt / 36
    leftover             = income - expenses - monthly_debt_payment
    score                = (leftover / income) * 100

    return round(max(0.0, min(score, 100.0)), 2)  # Clamp between 0 and 100


# ── FORMULA 3: Financial Health Status ──────────────────────────────────────
#
#   Uses the financial score to assign a health label.
#
#   Score Range   Health Label   Meaning
#   70 – 100   →  Good           Stable. User can manage debt comfortably.
#   40 – 69    →  At Risk        Needs attention. Budget carefully.
#   0  – 39    →  Critical       Serious distress. Immediate action needed.
# ─────────────────────────────────────────────────────────────────────────────

def calculate_health(score):
    if score >= 70:
        return "Good"
    elif score >= 40:
        return "At Risk"
    else:
        return "Critical"


# ── FORMULA 4: Debt Settlement Prediction ───────────────────────────────────
#
#   Purpose:
#     Predicts whether the user can successfully negotiate and settle
#     their debt based on 3 key financial conditions checked directly
#     against income, debt, and expenses.
#
#   Condition A — Surplus Check:
#     surplus = income - expenses
#     If surplus > 0, the user earns more than they spend each month.
#     This leftover money can be directed toward debt repayment.
#
#   Condition B — Debt-to-Income Ratio Check:
#     debt_to_income = debt / income  (raw multiplier, not percentage)
#     If debt_to_income < 3, the debt is less than 3× the monthly income.
#     This is a manageable level of debt.
#
#   Condition C — Expense Ratio Check:
#     expense_ratio = expenses / income
#     If expense_ratio < 0.5, the user spends less than 50% of income
#     on living expenses, leaving room for debt payments.
#
#   Prediction Rules:
#   ┌──────────────────────────────────────────────┬──────────────────────────┐
#   │  Conditions Met                              │  Result                  │
#   ├──────────────────────────────────────────────┼──────────────────────────┤
#   │  All 3 conditions are True                   │  High Probability        │
#   │  Any 2 conditions are True                   │  Medium Probability      │
#   │  Only 1 or 0 conditions are True             │  Low Probability         │
#   └──────────────────────────────────────────────┴──────────────────────────┘
#
#   Examples:
#
#   Example 1 — High Probability:
#     income = 6000, debt = 10000, expenses = 2000
#     surplus        = 6000 - 2000      = 4000  > 0      ✓  (Condition A)
#     debt_to_income = 10000 / 6000     = 1.67  < 3      ✓  (Condition B)
#     expense_ratio  = 2000  / 6000     = 0.33  < 0.5    ✓  (Condition C)
#     All 3 True → "High Probability"
#
#   Example 2 — Medium Probability:
#     income = 4000, debt = 14000, expenses = 2500
#     surplus        = 4000 - 2500      = 1500  > 0      ✓  (Condition A)
#     debt_to_income = 14000 / 4000     = 3.5   ≥ 3      ✗  (Condition B)
#     expense_ratio  = 2500  / 4000     = 0.63  ≥ 0.5    ✗  (Condition C)
#     Only 1 True → "Low Probability"
#
#   Example 3 — Low Probability:
#     income = 3000, debt = 25000, expenses = 3200
#     surplus        = 3000 - 3200      = -200  < 0      ✗  (Condition A)
#     debt_to_income = 25000 / 3000     = 8.33  ≥ 3      ✗  (Condition B)
#     expense_ratio  = 3200  / 3000     = 1.07  ≥ 0.5    ✗  (Condition C)
#     All 3 False → "Low Probability"
# ─────────────────────────────────────────────────────────────────────────────

def predict_settlement(income, debt, expenses):

    # Guard: treat zero or negative income as worst case
    if income <= 0:
        return "Low Probability"

    # Condition A: User has monthly surplus after expenses
    condition_a = (income - expenses) > 0

    # Condition B: Debt is less than 3× the monthly income
    condition_b = (debt / income) < 3

    # Condition C: Expenses are less than 50% of income
    condition_c = (expenses / income) < 0.5

    # Count how many conditions are satisfied
    conditions_met = sum([condition_a, condition_b, condition_c])

    if conditions_met == 3:
        return "High Probability"
    elif conditions_met == 2:
        return "Medium Probability"
    else:
        return "Low Probability"


# ── Legacy wrapper kept for compatibility ────────────────────────────────────
#   main.py previously called predict(score).
#   This wrapper maps the old score-based call to the new label format.

def predict(score):
    if score >= 75:
        return "High Probability"
    elif score >= 45:
        return "Medium Probability"
    else:
        return "Low Probability"


# ── MASTER FUNCTION: analyze_finances ───────────────────────────────────────
#
#   Runs all calculations in one call.
#   Called directly by the /analyze endpoint in main.py.
#
#   Input:
#     income   (int) — monthly income in dollars
#     debt     (int) — total outstanding debt in dollars
#     expenses (int) — monthly living expenses in dollars
#
#   Output  (dict):
#     debt_ratio       float   — debt as % of income (capped at 100)
#     financial_score  float   — overall score from 0 to 100
#     health           str     — Good / At Risk / Critical
#     settlement       str     — High / Medium / Low Probability
# ─────────────────────────────────────────────────────────────────────────────

def analyze_finances(income, debt, expenses):
    debt_ratio = calculate_debt_ratio(income, debt)
    score      = calculate_financial_score(income, debt, expenses)
    health     = calculate_health(score)
    settlement = predict_settlement(income, debt, expenses)

    return {
        "debt_ratio"      : debt_ratio,
        "financial_score" : score,
        "health"          : health,
        "settlement"      : settlement
    }
