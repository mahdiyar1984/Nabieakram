from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from config_app import settings

def send_activation_email(subject, user, activation_link, template, text_message):
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [user.email]
    context = {
        'subject': subject,
        'activation_link': activation_link,
        'user': user,
        'text_message': text_message
    }
    html_content = render_to_string(template, context)
    text_content = f"{text_message}:\n{activation_link}"
    msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    msg.attach_alternative(html_content, "text/html")
    msg.send()