from django.urls import path
from account_app import views

app_name = "account_app"
urlpatterns = [

    # region authentication
    path('register', views.RegisterView.as_view(), name='register_page'),
    path('activate-account/<email_active_code>', views.ActiveAccountView.as_view(), name='activate_account_page'),
    path('login', views.LoginView.as_view(), name='login_page'),
    path('logout', views.LogoutView.as_view(), name='logout_page'),
    path('forgot_password', views.ForgotPasswordView.as_view(), name='forgot_password_page'),
    path('reset-password/<email_active_code>', views.ResetPasswordView.as_view(), name='reset_password_page'),
    # endregion

    # region profile
    path('profile/', views.UserPanelDashboardPage.as_view(), name='user_panel_dashboard_page'),
    path('profile/edit_profile/', views.EditUserProfilePage.as_view(), name='edit_user_profile_page'),
    path('profile/change_password/', views.ChangePasswordPage.as_view(), name='change_password_page'),
    path('profile/update_avatar/', views.update_avatar, name='update_avatar'),
    # endregion
]
