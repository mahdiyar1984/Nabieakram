from .models import SiteSetting

def site_settings(request):
    try:
        site_setting = SiteSetting.objects.first()  # اولین رکورد سایت
    except SiteSetting.DoesNotExist:
        site_setting = None
    return {'site_setting': site_setting}
