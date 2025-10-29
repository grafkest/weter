from __future__ import annotations

from functools import wraps

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from . import db
from .models import (
    Advantage,
    Hero,
    Review,
    Service,
    SurveillancePackage,
    Tariff,
)

admin_bp = Blueprint("admin", __name__, template_folder="templates")


def login_required(view):  # type: ignore[override]
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("admin_authenticated"):
            return redirect(url_for("admin.login", next=request.path))
        return view(*args, **kwargs)

    return wrapped


@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        if (
            username == current_app.config["ADMIN_USERNAME"]
            and password == current_app.config["ADMIN_PASSWORD"]
        ):
            session["admin_authenticated"] = True
            flash("Вы вошли в панель администратора", "success")
            return redirect(request.args.get("next") or url_for("admin.dashboard"))
        flash("Неверный логин или пароль", "danger")
    return render_template("admin/login.html")


@admin_bp.route("/logout")
@login_required
def logout():
    session.clear()
    flash("Вы вышли из панели администратора", "info")
    return redirect(url_for("admin.login"))


@admin_bp.route("/")
@login_required
def dashboard():
    return render_template(
        "admin/dashboard.html",
        hero=Hero.query.first(),
        services=Service.query.all(),
        tariffs=Tariff.query.all(),
        packages=SurveillancePackage.query.all(),
        advantages=Advantage.query.all(),
        reviews=Review.query.all(),
    )


@admin_bp.route("/hero", methods=["POST"])
@login_required
def update_hero():
    hero = Hero.query.first()
    if not hero:
        hero = Hero()
        db.session.add(hero)
    hero.title = request.form.get("title", hero.title)
    hero.subtitle = request.form.get("subtitle", hero.subtitle)
    hero.primary_cta_text = request.form.get("primary_cta_text", hero.primary_cta_text)
    hero.primary_cta_link = request.form.get("primary_cta_link", hero.primary_cta_link)
    hero.secondary_cta_text = request.form.get("secondary_cta_text", hero.secondary_cta_text)
    hero.secondary_cta_link = request.form.get("secondary_cta_link", hero.secondary_cta_link)
    db.session.commit()
    flash("Герой-секция обновлена", "success")
    return redirect(url_for("admin.dashboard"))


@admin_bp.route("/services", methods=["POST"])
@login_required
def save_service():
    service_id = request.form.get("service_id")
    if service_id:
        service = Service.query.get(service_id)
        if not service:
            flash("Услуга не найдена", "danger")
            return redirect(url_for("admin.dashboard"))
    else:
        service = Service()
        db.session.add(service)

    service.category = request.form.get("category", service.category)
    service.title = request.form.get("title", service.title)
    service.description = request.form.get("description", service.description)
    service.features = request.form.get("features", service.features or "")
    db.session.commit()
    flash("Услуга сохранена", "success")
    return redirect(url_for("admin.dashboard"))


@admin_bp.route("/services/<int:service_id>/delete", methods=["POST"])
@login_required
def delete_service(service_id: int):
    service = Service.query.get_or_404(service_id)
    db.session.delete(service)
    db.session.commit()
    flash("Услуга удалена", "info")
    return redirect(url_for("admin.dashboard"))


@admin_bp.route("/tariffs", methods=["POST"])
@login_required
def save_tariff():
    tariff_id = request.form.get("tariff_id")
    if tariff_id:
        tariff = Tariff.query.get(tariff_id)
        if not tariff:
            flash("Тариф не найден", "danger")
            return redirect(url_for("admin.dashboard"))
    else:
        tariff = Tariff()
        db.session.add(tariff)

    tariff.name = request.form.get("name", tariff.name)
    tariff.speed_mbps = int(request.form.get("speed_mbps", tariff.speed_mbps or 0))
    tariff.price_per_month = float(
        request.form.get("price_per_month", tariff.price_per_month or 0.0)
    )
    tariff.description = request.form.get("description", tariff.description)
    db.session.commit()
    flash("Тариф сохранен", "success")
    return redirect(url_for("admin.dashboard"))


@admin_bp.route("/tariffs/<int:tariff_id>/delete", methods=["POST"])
@login_required
def delete_tariff(tariff_id: int):
    tariff = Tariff.query.get_or_404(tariff_id)
    db.session.delete(tariff)
    db.session.commit()
    flash("Тариф удален", "info")
    return redirect(url_for("admin.dashboard"))


@admin_bp.route("/packages", methods=["POST"])
@login_required
def save_package():
    package_id = request.form.get("package_id")
    if package_id:
        package = SurveillancePackage.query.get(package_id)
        if not package:
            flash("Комплект не найден", "danger")
            return redirect(url_for("admin.dashboard"))
    else:
        package = SurveillancePackage()
        db.session.add(package)

    package.name = request.form.get("name", package.name)
    package.description = request.form.get("description", package.description)
    package.features = request.form.get("features", package.features or "")
    package.price = float(request.form.get("price", package.price or 0.0))
    db.session.commit()
    flash("Комплект сохранен", "success")
    return redirect(url_for("admin.dashboard"))


@admin_bp.route("/packages/<int:package_id>/delete", methods=["POST"])
@login_required
def delete_package(package_id: int):
    package = SurveillancePackage.query.get_or_404(package_id)
    db.session.delete(package)
    db.session.commit()
    flash("Комплект удален", "info")
    return redirect(url_for("admin.dashboard"))


@admin_bp.route("/advantages", methods=["POST"])
@login_required
def save_advantage():
    advantage_id = request.form.get("advantage_id")
    if advantage_id:
        advantage = Advantage.query.get(advantage_id)
        if not advantage:
            flash("Преимущество не найдено", "danger")
            return redirect(url_for("admin.dashboard"))
    else:
        advantage = Advantage()
        db.session.add(advantage)

    advantage.page = request.form.get("page", advantage.page)
    advantage.title = request.form.get("title", advantage.title)
    advantage.description = request.form.get("description", advantage.description)
    db.session.commit()
    flash("Преимущество сохранено", "success")
    return redirect(url_for("admin.dashboard"))


@admin_bp.route("/advantages/<int:advantage_id>/delete", methods=["POST"])
@login_required
def delete_advantage(advantage_id: int):
    advantage = Advantage.query.get_or_404(advantage_id)
    db.session.delete(advantage)
    db.session.commit()
    flash("Преимущество удалено", "info")
    return redirect(url_for("admin.dashboard"))


@admin_bp.route("/reviews", methods=["POST"])
@login_required
def save_review():
    review_id = request.form.get("review_id")
    if review_id:
        review = Review.query.get(review_id)
        if not review:
            flash("Отзыв не найден", "danger")
            return redirect(url_for("admin.dashboard"))
    else:
        review = Review()
        db.session.add(review)

    review.author = request.form.get("author", review.author)
    review.location = request.form.get("location", review.location)
    review.rating = int(request.form.get("rating", review.rating or 5))
    review.content = request.form.get("content", review.content)
    db.session.commit()
    flash("Отзыв сохранен", "success")
    return redirect(url_for("admin.dashboard"))


@admin_bp.route("/reviews/<int:review_id>/delete", methods=["POST"])
@login_required
def delete_review(review_id: int):
    review = Review.query.get_or_404(review_id)
    db.session.delete(review)
    db.session.commit()
    flash("Отзыв удален", "info")
    return redirect(url_for("admin.dashboard"))
