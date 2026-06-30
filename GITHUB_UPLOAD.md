# GitHub Upload Guide
## FinRelief AI — AI Powered Debt Relief and Financial Recovery Platform

---

## Before You Push — Safety Checklist

Run through this checklist before running any Git commands:

- [ ] `backend/.env` is listed in `.gitignore` — never commit real API keys
- [ ] `backend/finance.db` is listed in `.gitignore` — never commit user data
- [ ] `frontend/node_modules/` is listed in `.gitignore` — never commit packages
- [ ] `backend/venv/` is listed in `.gitignore` — never commit virtual environments
- [ ] `.env.example` exists with a placeholder value — safe to commit

---

## Step 1 — Create a Repository on GitHub

1. Go to https://github.com and sign in
2. Click the **+** button (top right) → **New repository**
3. Fill in the details:

| Field               | Value                                    |
|---------------------|------------------------------------------|
| Repository name     | `finrelief-ai`                           |
| Description         | AI Powered Debt Relief and Financial Recovery Platform |
| Visibility          | Public or Private                        |
| Initialize repo     | Leave unchecked — you will push existing code |

4. Click **Create repository**
5. Copy the repository URL shown — you will need it in Step 5

---

## Step 2 — Open Terminal in VS Code

Open the terminal in VS Code (`Ctrl + `` `) and navigate to the root project folder:

```bash
cd gen-ai-project
```

Confirm you are in the right folder:
```bash
dir
```

You should see: `backend/`, `frontend/`, `README.md`, `.gitignore`

---

## Step 3 — Initialize Git Repository

```bash
git init
```

Expected output:
```
Initialized empty Git repository in C:/Users/USER/gen-ai-project/.git/
```

This creates a hidden `.git/` folder that tracks all changes in your project.

---

## Step 4 — Stage All Project Files

```bash
git add .
```

This stages every file in the project that is not listed in `.gitignore`.

To verify what was staged:
```bash
git status
```

You should see green `new file:` entries for all your project files.
You should NOT see `.env`, `finance.db`, `node_modules/`, or `venv/` listed.

---

## Step 5 — Create the First Commit

```bash
git commit -m "Initial commit — FinRelief AI full stack project"
```

Expected output:
```
[main (root-commit) a1b2c3d] Initial commit — FinRelief AI full stack project
 X files changed, X insertions(+)
```

---

## Step 6 — Set the Main Branch

```bash
git branch -M main
```

This renames the default branch to `main`, which is the standard on GitHub.

---

## Step 7 — Connect to Your GitHub Repository

Replace `<your-username>` and `<repo-name>` with your actual GitHub username and repository name:

```bash
git remote add origin https://github.com/<your-username>/finrelief-ai.git
```

Verify the remote was added:
```bash
git remote -v
```

Expected output:
```
origin  https://github.com/<your-username>/finrelief-ai.git (fetch)
origin  https://github.com/<your-username>/finrelief-ai.git (push)
```

---

## Step 8 — Push to GitHub

```bash
git push -u origin main
```

GitHub will prompt for your username and password (or personal access token).

Expected output:
```
Enumerating objects: XX, done.
Counting objects: 100% (XX/XX), done.
Writing objects: 100% (XX/XX), done.
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

Your project is now live on GitHub.

---

## Step 9 — Verify on GitHub

1. Open your browser and go to `https://github.com/<your-username>/finrelief-ai`
2. Confirm all files and folders are visible:

```
finrelief-ai/
├── backend/
│   ├── main.py
│   ├── ai_engine.py
│   ├── prediction.py
│   ├── database.py
│   ├── requirements.txt
│   └── .env.example        ← safe placeholder, committed
├── frontend/
│   ├── src/
│   └── package.json
├── ERD.md
├── schema.sql
├── README.md
└── ...
```

3. Confirm these files are NOT visible (protected by `.gitignore`):
   - `backend/.env`
   - `backend/finance.db`
   - `frontend/node_modules/`
   - `backend/venv/`

---

## Making Future Updates

After making any code changes, push them with:

```bash
git add .
git commit -m "Brief description of what changed"
git push
```

---

## All Commands Quick Reference

```bash
# Step 1 — Navigate to project root
cd gen-ai-project

# Step 2 — Initialize Git
git init

# Step 3 — Stage all files
git add .

# Step 4 — Verify staged files (optional)
git status

# Step 5 — Create first commit
git commit -m "Initial commit — FinRelief AI full stack project"

# Step 6 — Set branch to main
git branch -M main

# Step 7 — Connect to GitHub (replace with your URL)
git remote add origin https://github.com/<your-username>/finrelief-ai.git

# Step 8 — Push to GitHub
git push -u origin main

# Future updates
git add .
git commit -m "describe your changes"
git push
```

---

## Common Errors and Fixes

| Error | Cause | Fix |
|---|---|---|
| `git: command not found` | Git not installed | Download from https://git-scm.com |
| `remote origin already exists` | Remote was already added | Run `git remote remove origin` then add again |
| `Authentication failed` | Wrong credentials | Use a GitHub Personal Access Token instead of password |
| `Updates were rejected` | Remote has changes not in local | Run `git pull origin main` then push again |
| `.env visible on GitHub` | Missing .gitignore entry | Add `backend/.env` to `.gitignore`, run `git rm --cached backend/.env`, commit |

---

*Generated for: FinRelief AI — AI Powered Debt Relief and Financial Recovery Platform*
*Internship Project — GitHub Upload Guide*
