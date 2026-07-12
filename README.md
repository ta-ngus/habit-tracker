# Habit Tracker

A full-stack habit tracking app built with Flask. Add daily habits, mark them
complete, and watch your streaks build on a GitHub-style contribution heatmap.

## Features

- User accounts (signup / login / logout) with hashed passwords
- Create and delete habits
- Mark a habit done for today with one click
- Automatic streak calculation (current streak + longest streak)
- 30-day completion rate per habit
- GitHub-style heatmap visualizing the last 30 days of activity

## Tech Stack

- **Backend:** Flask, Flask-SQLAlchemy, Flask-Login
- **Database:** SQLite (dev) — swap `DATABASE_URL` for Postgres in production
- **Frontend:** Jinja2 templates, vanilla CSS

## Getting Started

\`\`\`bash
git clone https://github.com/yourusername/habit-tracker.git
cd habit-tracker
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
python run.py
\`\`\`

Visit `http://localhost:5000`, sign up, and start tracking.

## How Streaks Are Calculated

- **Current streak:** counts consecutive completed days backwards from today.
  If today isn't marked yet, it checks from yesterday so the streak doesn't
  reset the moment a new day starts.
- **Longest streak:** scans all completion dates for the longest run ever achieved.
- **Completion rate:** percentage of the last 30 days marked done.

## License

MIT