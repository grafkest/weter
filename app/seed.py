from __future__ import annotations

from . import db
from .models import (
    Advantage,
    Hero,
    Review,
    Service,
    SurveillancePackage,
    Tariff,
)


def seed_defaults() -> None:
    """Populate the database with initial content when tables are empty."""
    if not Hero.query.first():
        hero = Hero(
            title="Быстрый интернет и видеонаблюдение",
            subtitle="Комплексные решения для квартир, домов и бизнеса с круглосуточной поддержкой.",
            primary_cta_text="Проверить доступность",
            primary_cta_link="#availability",
            secondary_cta_text="Заказать консультацию",
            secondary_cta_link="#consultation",
        )
        db.session.add(hero)

    if Service.query.count() == 0:
        db.session.add_all(
            [
                Service(
                    category="internet",
                    title="Оптоволоконный интернет",
                    description="Стабильное подключение со скоростью до 1 Гбит/с.",
                    features="Скорость до 1 Гбит/с\nWi-Fi 6 роутер\nКруглосуточная поддержка",
                ),
                Service(
                    category="surveillance",
                    title="Интеллектуальное видеонаблюдение",
                    description="Контроль дома и бизнеса с мобильным доступом.",
                    features="Full HD камеры\nОблачное хранение\nУведомления в мобильном приложении",
                ),
            ]
        )

    if Tariff.query.count() == 0:
        db.session.add_all(
            [
                Tariff(
                    name="Комфорт",
                    speed_mbps=100,
                    price_per_month=590,
                    description="Идеально для онлайн-обучения и стриминга в HD.",
                ),
                Tariff(
                    name="Премиум",
                    speed_mbps=300,
                    price_per_month=890,
                    description="Для умного дома и видеонаблюдения без задержек.",
                ),
                Tariff(
                    name="Бизнес",
                    speed_mbps=500,
                    price_per_month=1290,
                    description="Максимальная стабильность для офисов и кафе.",
                ),
            ]
        )

    if SurveillancePackage.query.count() == 0:
        db.session.add_all(
            [
                SurveillancePackage(
                    name="Квартира",
                    description="1-2 компактные камеры с ночным режимом.",
                    features="Full HD качество\nДвусторонняя связь\nНочное видение",
                    price=1190,
                ),
                SurveillancePackage(
                    name="Частный дом",
                    description="Комплект из 4 камер для контроля периметра.",
                    features="Уличные камеры IP66\nЗапись в облако\nДоступ из приложения",
                    price=2490,
                ),
                SurveillancePackage(
                    name="Бизнес",
                    description="6 камер и видеорегистратор с резервным питанием.",
                    features="POE-питание\nОтчеты о событиях\nГарантия 3 года",
                    price=3890,
                ),
            ]
        )

    if Advantage.query.count() == 0:
        db.session.add_all(
            [
                Advantage(
                    page="home",
                    title="Собственная сеть",
                    description="Локальная инфраструктура без посредников и задержек.",
                ),
                Advantage(
                    page="home",
                    title="Поддержка 24/7",
                    description="Наши инженеры доступны круглосуточно для абонентов.",
                ),
                Advantage(
                    page="home",
                    title="Гарантия на оборудование",
                    description="Бесплатное обслуживание и замена устройств в течение 3 лет.",
                ),
            ]
        )

    if Review.query.count() == 0:
        db.session.add_all(
            [
                Review(
                    author="Анна П.",
                    location="г. Тверь",
                    rating=5,
                    content="Подключили интернет за день, стабильность отличная, техподдержка отвечает быстро.",
                ),
                Review(
                    author="ООО 'Кофейня'",
                    location="Тула",
                    rating=5,
                    content="Поставили камеры в зале и на складе, можем смотреть трансляции с телефона — очень удобно.",
                ),
            ]
        )

    db.session.commit()
