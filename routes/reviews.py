from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db, Review
from datetime import datetime

reviews_bp = Blueprint("reviews", __name__)


@reviews_bp.route("/reviews")
def reviews():
    all_reviews = Review.query.order_by(Review.created_at.desc()).all()
    return render_template("reviews.html", reviews=all_reviews)


@reviews_bp.route("/reviews/add", methods=["POST"])
@login_required
def add_review():
    rating = request.form.get("rating", type=int)
    text = request.form.get("text", "").strip()

    if not rating or rating < 1 or rating > 5:
        flash("Пожалуйста, выберите оценку от 1 до 5", "danger")
        return redirect(url_for("reviews.reviews"))

    if len(text) < 10:
        flash("Отзыв должен содержать минимум 10 символов", "danger")
        return redirect(url_for("reviews.reviews"))

    existing = Review.query.filter_by(user_id=current_user.id).first()
    if existing:
        flash("Вы уже оставили отзыв! Можно оставить только один.", "warning")
        return redirect(url_for("reviews.reviews"))

    review = Review(
        user_id=current_user.id,
        rating=rating,
        text=text,
        created_at=datetime.utcnow()
    )
    db.session.add(review)
    db.session.commit()

    flash("Спасибо за отзыв! Он очень важен для нас.", "success")
    return redirect(url_for("reviews.reviews"))
