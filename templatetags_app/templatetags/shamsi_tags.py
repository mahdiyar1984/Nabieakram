from django import template
import jdatetime
from datetime import datetime, timezone

register = template.Library()
MONTHS_FA = [
    "فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور",
    "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"
]


@register.filter
def to_shamsi(value):
    try:

        if hasattr(value, "hour"):
            shamsi_date = jdatetime.datetime.fromgregorian(datetime=value)
        else:
            shamsi_date = jdatetime.date.fromgregorian(date=value)

        return f"{shamsi_date.day} {MONTHS_FA[shamsi_date.month - 1]} {shamsi_date.year}"
    except Exception:
        return "نامشخص"


@register.filter
def timeago(value):
    try:
        if not value:
            return "نامشخص"

        # اگر naive datetime بود → به UTC تبدیلش کنیم
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)

        now = datetime.now(timezone.utc)
        diff = now - value

        seconds = diff.total_seconds()
        minutes = int(seconds // 60)
        hours = int(seconds // 3600)
        days = int(seconds // 86400)
        months = int(days // 30)
        years = int(days // 365)

        if seconds < 60:
            return "چند لحظه پیش"
        elif minutes < 60:
            return f"{minutes} دقیقه پیش"
        elif hours < 24:
            return f"{hours} ساعت پیش"
        elif days < 30:
            return f"{days} روز پیش"
        elif months < 12:
            return f"{months} ماه پیش"
        else:
            return f"{years} سال پیش"

    except Exception:
        return "نامشخص"


@register.filter
def to_persian_month(value):
    try:
        month = int(value)
        if 1 <= month <= 12:
            return MONTHS_FA[month - 1]
    except:
        pass
    return "نامشخص"
