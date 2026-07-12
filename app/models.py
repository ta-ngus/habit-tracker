from datetime import date, timedelta
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    habits = db.relationship("Habit", backref="owner", lazy=True, cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.Date, default=date.today)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    logs = db.relationship("HabitLog", backref="habit", lazy=True, cascade="all, delete-orphan")

    def completed_dates(self):
        return {log.date for log in self.logs}

    def is_done_today(self):
        return date.today() in self.completed_dates()

    def current_streak(self):
        done = self.completed_dates()
        if not done:
            return 0
        streak = 0
        cursor = date.today()
        if cursor not in done:
            cursor -= timedelta(days=1)
        while cursor in done:
            streak += 1
            cursor -= timedelta(days=1)
        return streak

    def longest_streak(self):
        done = sorted(self.completed_dates())
        if not done:
            return 0
        longest = current = 1
        for i in range(1, len(done)):
            if done[i] == done[i - 1] + timedelta(days=1):
                current += 1
                longest = max(longest, current)
            else:
                current = 1
        return longest

    def completion_rate(self, days=30):
        done = self.completed_dates()
        today = date.today()
        window = [today - timedelta(days=i) for i in range(days)]
        completed_in_window = sum(1 for d in window if d in done)
        return round((completed_in_window / days) * 100)


class HabitLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    habit_id = db.Column(db.Integer, db.ForeignKey("habit.id"), nullable=False)
    date = db.Column(db.Date, default=date.today, nullable=False)

    __table_args__ = (db.UniqueConstraint("habit_id", "date", name="uq_habit_date"),)