from __future__ import annotations

from flask import Blueprint, flash, redirect, render_template, request, url_for

from . import db
from .models import (
    Advantage,
    AvailabilityRequest,
    ConsultationRequest,
    ContactSubmission,
    Hero,
    Review,
    Service,
    SurveillancePackage,
    Tariff,
)

main_bp = Blueprint("main", __name__, template_folder="templates")


@main_bp.app_context_processor
def inject_globals():
    return {"hero": Hero.query.first()}


@main_bp.route("/")
def index():
    services = Service.query.all()
    advantages = Advantage.query.filter_by(page="home").all()
    reviews = Review.query.order_by(Review.created_at.desc()).limit(5).all()
    return render_template(
        "index.html",
        services=services,
        advantages=advantages,
        reviews=reviews,
    )


@main_bp.route("/internet")
def internet():
    tariffs = Tariff.query.order_by(Tariff.price_per_month).all()
    advantages = Advantage.query.filter_by(page="internet").all()
    return render_template("internet.html", tariffs=tariffs, advantages=advantages)


@main_bp.route("/surveillance")
def surveillance():
    packages = SurveillancePackage.query.all()
    advantages = Advantage.query.filter_by(page="surveillance").all()
    return render_template(
        "surveillance.html",
        packages=packages,
        advantages=advantages,
    )


@main_bp.route("/about")
def about():
    team = [
        {
            "name": "Иван Смирнов",
            "role": "Руководитель компании",
            "bio": "15 лет опыта в телекоммуникациях и построении сетей.",
        },
        {
            "name": "Мария Королева",
            "role": "Руководитель службы поддержки",
            "bio": "Контролирует качество сервиса и обучение инженеров.",
        },
        {
            "name": "Алексей Морозов",
            "role": "Ведущий инженер",
            "bio": "Специализируется на системах видеонаблюдения и интеграции IoT.",
        },
    ]
    return render_template("about.html", team=team)


@main_bp.route("/contacts")
def contacts():
    return render_template("contacts.html")


@main_bp.route("/availability", methods=["POST"])
def check_availability():
    address = request.form.get("address")
    full_name = request.form.get("name")
    phone = request.form.get("phone")
    if not address:
        flash("Укажите адрес для проверки доступности", "danger")
        return redirect(url_for("main.index") + "#availability")

    request_obj = AvailabilityRequest(address=address, full_name=full_name, phone=phone)
    db.session.add(request_obj)
    db.session.commit()
    flash(
        "Заявка на проверку доступности отправлена. Мы свяжемся с вами в течение рабочего дня.",
        "success",
    )
    return redirect(url_for("main.index") + "#availability")


@main_bp.route("/consultation", methods=["POST"])
def consultation_request():
    name = request.form.get("name")
    phone = request.form.get("phone")
    address = request.form.get("address")
    comment = request.form.get("comment")
    if not all([name, phone, address]):
        flash("Заполните имя, телефон и адрес", "danger")
        return redirect(url_for("main.surveillance") + "#consultation")

    consultation = ConsultationRequest(name=name, phone=phone, address=address, comment=comment)
    db.session.add(consultation)
    db.session.commit()
    flash("Запрос на консультацию отправлен", "success")
    return redirect(url_for("main.surveillance") + "#consultation")


@main_bp.route("/contact", methods=["POST"])
def contact_submit():
    name = request.form.get("name")
    contact = request.form.get("contact")
    message = request.form.get("message")
    if not all([name, contact]):
        flash("Укажите имя и телефон или email", "danger")
        return redirect(url_for("main.contacts") + "#feedback")

    submission = ContactSubmission(name=name, contact=contact, message=message)
    db.session.add(submission)
    db.session.commit()
    flash("Сообщение отправлено. Мы ответим в ближайшее время.", "success")
    return redirect(url_for("main.contacts") + "#feedback")
