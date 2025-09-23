from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import ContactUs
from utils.email_service import send_activation_email


@receiver(post_save, sender=ContactUs)
def send_response_email(sender, instance, created, **kwargs):
    # فقط وقتی پاسخ جدید اضافه شده باشه و قبلا خالی بوده
    if not created and instance.response:
        old = ContactUs.objects.get(pk=instance.pk)
        if old.response != instance.response:
            # تنظیم تاریخ پاسخ
            instance.response_date = timezone.now()
            instance.save(update_fields=['response_date'])

            # ارسال ایمیل
            if instance.user and instance.user.email:
                send_activation_email(
                    subject=f"پاسخ به پیام شما: {instance.subject}",
                    user=instance.user,
                    activation_link="",  # چون نیازی به لینک نداریم، می‌تونیم خالی بذاریم
                    template="emails/contact_response.html",  # قالب ایمیل HTML
                    text_message=instance.response
                )
