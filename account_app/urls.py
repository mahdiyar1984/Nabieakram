from django.urls import path
from account_app import views

app_name = "account_app"
urlpatterns = [
    path('register', views.RegisterView.as_view(), name='register_page'),
    path('activate-account/<email_active_code>', views.ActiveAccountView.as_view(), name='activate_account_page'),
    path('login', views.LoginView.as_view(), name='login_page'),
    path('logout', views.LogoutView.as_view(), name='logout_page'),
    path('forgot_password', views.ForgotPasswordView.as_view(), name='forgot_password_page'),
    path('reset-password/<email_active_code>', views.ResetPasswordView.as_view(), name='reset_password_page'),
]
