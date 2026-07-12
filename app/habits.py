from datetime import date, timedelta
from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from flask_login import login_required, current_user
from app import db
from app.models import Habit, HabitLog

habits_bp = Blueprint("habits", __name__)


def get_owned_habit_or_404(habit_id):
    habit = Habit.query.get_or_404(habit_id)
    if habit.user_id != current_user.id:
        abort(403)
    return habit


@habits_bp.route("/")
@login_required
def dashboard():
    habits = Habit.query.filter_by(user_id=current_user.id).order_by(Habit.created_at.desc()).all()
    today = date.today()
    last_30_days = [today - timedelta(days=i) for i in range(29, -1, -1)]
    habit_data = []
    for h in habits:
        done_dates = h.completed_dates()
        heatmap = [{"date": d.isoformat(), "done": d in done_dates} for d in last_30_days]
        habit_data.append({
            "habit": h,
            "heatmap": heatmap,
            "current_streak": h.current_streak(),
            "longest_streak": h.longest_streak(),
            "completion_rate": h.completion_rate(),
            "done_today": h.is_done_today(),
        })
    return render_template("dashboard.html", habit_data=habit_data)


@habits_bp.route("/habits/new", methods=["POST"])
@login_required
def create_habit():
    name = request.form.get("name", "").strip()
    if not name:
        flash("Habit name can't be empty.", "error")
        return redirect(url_for("habits.dashboard"))
    habit = Habit(name=name, user_id=current_user.id)
    db.session.add(habit)
    db.session.commit()
    return redirect(url_for("habits.dashboard"))


@habits_bp.route("/habits/<int:habit_id>/toggle", methods=["POST"])
@login_required
def toggle_today(habit_id):
    habit = get_owned_habit_or_404(habit_id)
    today = date.today()
    log = HabitLog.query.filter_by(habit_id=habit.id, date=today).first()
    if log:
        db.session.delete(log)
    else:
        db.session.add(HabitLog(habit_id=habit.id, date=today))
    db.session.commit()
    return redirect(url_for("habits.dashboard"))


@habits_bp.route("/habits/<int:habit_id>/delete", methods=["POST"])
@login_required
def delete_habit(habit_id):
    habit = get_owned_habit_or_404(habit_id)
    db.session.delete(habit)
    db.session.commit()
    return redirect(url_for("habits.dashboard"))