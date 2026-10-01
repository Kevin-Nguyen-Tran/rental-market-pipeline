# First Data Engineering Project

Rental Market Data Pipeline - Setup Notes & Progress Tracker

A running reference for tools, commands, setup decisions, lessons learned, and next steps.

## 1. Project Goal

Build an end-to-end rental market data pipeline that demonstrates the core workflow of a data engineer: ingesting data, preserving raw source data, loading a database, transforming it into analytics-ready models, testing it, and eventually visualizing and scheduling the pipeline.

```text
Rental API
    ↓
Python ingestion
    ↓
Raw JSON
    ↓
PostgreSQL
    ↓
SQL / dbt transformations
    ↓
Dimensional model
    ↓
Tableau
```

## 2. Current Computer & Constraints

| Item | Current Setup |
| --- | --- |
| Computer | 2016 Intel MacBook Pro |
| Operating system | macOS Monterey 12.7.6 |
| Memory | 8 GB RAM |
| Free storage | About 202 GB |
| Approach | Keep the local stack lightweight; avoid Spark, Airflow, and Docker initially |

The laptop is sufficient for this first project. The main constraint is RAM rather than storage, so the initial architecture will favor lightweight local tools and cloud-based options later for heavier workloads.

## 3. Tools Installed & Why They Matter

### VS Code

Purpose: Development workspace

Project use: Write Python and SQL, manage project files, use the built-in terminal, and interact with Git.

### Python

Purpose: Pipeline / automation language

Project use: Call APIs, receive JSON, save raw files, validate data, connect to PostgreSQL, insert data, and automate pipeline steps.

### Git

Purpose: Version control

Project use: Track changes, create checkpoints (commits), compare versions, and manage project history.

### GitHub

Purpose: Remote repository / portfolio

Project use: Store the Git repository online, back up code, and create a portfolio artifact that can be shared with recruiters or interviewers.

### PostgreSQL 16

Purpose: Local relational database

Project use: Store structured data, practice schemas/tables/constraints, run SQL, support incremental loads, and build a dimensional model.

## 4. VS Code Terminal

The built-in terminal is where Git commands, Python commands, and other command-line tools can be run without leaving VS Code.

- Open it from Terminal > New Terminal.

- Mac shortcut: Control + ` (backtick).

- Before running project commands, confirm the terminal is inside the rental-market-pipeline folder.

```text
pwd
ls
```

## 5. Git & GitHub Workflow

Git automatically notices file changes inside a Git repository, but it does not automatically commit or upload them. The normal workflow is:

```text
git status
git add .
git commit -m "Describe what changed"
git push
```

| Command | Meaning |
| --- | --- |
| git status | Shows changed, staged, and untracked files. |
| git add . | Stages all changes in the current folder and subfolders, except ignored files. |
| git commit -m "..." | Creates a local checkpoint with a description. |
| git push | Sends local commits to GitHub. |
| git remote -v | Shows which remote GitHub repository the project is connected to. |
| git ls-files | Shows the files currently tracked by Git. |

The period in git add . means “the current directory,” so the command stages changes in the current project folder and its subfolders.

## 6. Git Issues Encountered & Lessons Learned

No upstream branch: The local main branch was not yet linked to origin/main. The first push can use: git push --set-upstream origin main.

Remote contains work / fetch first: GitHub already had a commit that was not in the local repository. Because this was a brand-new project, the remote was ultimately replaced with the clean local branch.

Too many tracked files: The .venv folder was accidentally committed before Git was cleaned up. This caused more than 1,200 files to be tracked and created push problems.

Clean restart: The local Git history was reset, the correct .gitignore was in place, and a fresh clean project commit was pushed successfully.

Force push: A force operation was used only to repair the brand-new repository. Normal future work should use standard git push without --force.

## 7. Current Project Structure

```text
rental-market-pipeline/
├── ingestion/
├── data/
│   └── raw/
├── sql/
├── README.md
├── .gitignore
└── requirements.txt
```

| Path | Purpose |
| --- | --- |
| ingestion/ | Python scripts that retrieve data from source APIs. |
| data/raw/ | Untouched raw API responses used as the source-of-truth layer. |
| sql/ | SQL scripts for database creation, loading, and transformations. |
| README.md | Explains the project, architecture, setup, and decisions. |
| .gitignore | Prevents local-only, sensitive, temporary, or large files from being tracked. |
| requirements.txt | Records the Python packages needed to recreate the environment. |

## 8. .gitignore

The current .gitignore should contain:

```text
.venv/
.env
__pycache__/
data/raw/
```

.venv/ - Do not upload the local Python virtual environment.

.env - Do not upload secrets such as API keys, passwords, or connection strings.

__pycache__/ - Ignore temporary Python cache files.

data/raw/ - Avoid tracking potentially large downloaded source data.

Important: .gitignore prevents untracked files from being added. If a file was already committed, adding it to .gitignore alone does not remove it from Git history.

## 9. Python Virtual Environment & Dependencies

A virtual environment keeps this project’s Python packages isolated from the operating system and other projects.

```text
python3 -m venv .venv
source .venv/bin/activate
```

When active, the terminal prompt should begin with (.venv).

The first package for the project is requests, which allows Python to communicate with web APIs:

```text
pip install requests
```

To record the exact installed package versions:

```text
pip freeze > requirements.txt
```

pip freeze lists installed packages and their versions. The > redirects that output into requirements.txt. Later, the same environment can be recreated with:

```text
pip install -r requirements.txt
```

## 10. PostgreSQL Setup Notes

- Installed PostgreSQL 16 for Intel / x86-64 macOS.

- Stack Builder was not needed for the first project.

- PostgreSQL will be the local database used for raw/staging/analytics tables and SQL practice.

- A GUI such as DBeaver Community can be added for easier database browsing and querying.

## 11. Progress Checklist

| Status | Milestone | Notes |
| --- | --- | --- |
| DONE | Confirm laptop is sufficient | 2016 Intel MacBook Pro, 8 GB RAM, ~202 GB free. |
| DONE | Install VS Code | Primary development workspace. |
| DONE | Install Python | Used for API ingestion and pipeline logic. |
| DONE | Install Git | Local version control. |
| DONE | Create GitHub account/repository | Repository: rental-market-pipeline. |
| DONE | Connect local project to GitHub | Connection is working after clean repository reset. |
| DONE | Install PostgreSQL 16 | Local database engine. |
| DONE | Create project folders/files | ingestion, data/raw, sql, README, .gitignore, requirements.txt. |
| DONE | Create .gitignore | Excludes .venv, .env, __pycache__, and data/raw. |
| NEXT | Create/verify Python virtual environment | Activate .venv and confirm project-specific Python environment. |
| NEXT | Install requests | First API-related Python dependency. |
| NEXT | Make first API call | Retrieve a real JSON response. |
| LATER | Save raw JSON | Create the first raw / bronze data layer. |
| LATER | Load PostgreSQL | Move structured data from JSON into tables. |
| LATER | Add dbt / SQL modeling | Create staging and analytics layers. |
| LATER | Build dimensional model | Dimensions + fact rental snapshot. |
| LATER | Add testing and incremental loads | Improve reliability and history tracking. |
| LATER | Build Tableau dashboard | Demonstrate business use of the pipeline. |
| LATER | Schedule pipeline | Use GitHub Actions first; heavier orchestration later. |

## 12. Immediate Next Step

The environment setup is essentially complete. The next milestone is to stop installing tools and begin the first real data engineering workflow:

```text
Rental API
    ↓
Python request
    ↓
JSON response
    ↓
Inspect JSON
    ↓
Save raw JSON
```

Once that works, the next stage will be loading the raw data into PostgreSQL and beginning the database portion of the project.

## 13. Running Notes / Future Additions

Use this section to add key commands, issues encountered, architecture decisions, and lessons learned as the project grows.

________________________________________________________________________________

________________________________________________________________________________

________________________________________________________________________________

________________________________________________________________________________

________________________________________________________________________________
