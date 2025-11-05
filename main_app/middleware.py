from django.utils import timezone
from .models import DailyVisit

class DailyVisitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # صفحات ادمین یا استاتیک حساب نشن
        if request.path.startswith('/admin/') or request.path.startswith('/static/'):
            return response

        # فقط بازدیدهای GET حساب بشن
        if request.method == 'GET':
            today = timezone.localdate()
            ip = self.get_client_ip(request)
            path = request.path

            # بررسی تکراری نبودن بازدید امروز از همین IP
            if not DailyVisit.objects.filter(date=today, ip_address=ip, path=path).exists():
                DailyVisit.objects.create(
                    date=today,
                    ip_address=ip,
                    path=path,
                    user=request.user if request.user.is_authenticated else None
                )

        return response

    def get_client_ip(self, request):
        """بررسی هدرهای مختلف برای بدست آوردن IP واقعی"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip