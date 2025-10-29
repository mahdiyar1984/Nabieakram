from django import template

register = template.Library()

@register.filter
def dict_get(d, key):
    """مقدار دیکشنری را با کلید برمی‌گرداند"""
    return d.get(key, 0)  # اگر کلید نبود 0 برگرداند
