from __future__ import annotations

from datetime import datetime

from . import db


class TimestampMixin:
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Hero(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    subtitle = db.Column(db.String(500), nullable=False)
    primary_cta_text = db.Column(db.String(120), nullable=False)
    primary_cta_link = db.Column(db.String(255), nullable=False)
    secondary_cta_text = db.Column(db.String(120))
    secondary_cta_link = db.Column(db.String(255))


class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    features = db.Column(db.Text, nullable=False)

    def feature_list(self) -> list[str]:
        return [item.strip() for item in self.features.split("\n") if item.strip()]


class Advantage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    page = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(255), nullable=False)


class Tariff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    speed_mbps = db.Column(db.Integer, nullable=False)
    price_per_month = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255))


class SurveillancePackage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    features = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)

    def feature_list(self) -> list[str]:
        return [item.strip() for item in self.features.split("\n") if item.strip()]


class Review(db.Model, TimestampMixin):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(120), nullable=False)
    location = db.Column(db.String(120))
    rating = db.Column(db.Integer, default=5)
    content = db.Column(db.Text, nullable=False)


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(255))


class AvailabilityRequest(db.Model, TimestampMixin):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120))
    phone = db.Column(db.String(50))
    address = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), default="pending")


class ContactSubmission(db.Model, TimestampMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    contact = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text)


class ConsultationRequest(db.Model, TimestampMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    comment = db.Column(db.Text)
