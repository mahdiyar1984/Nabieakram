from django.urls import path
from userprofile_app import views

app_name = "userprofile_app"
urlpatterns = [

    # region setting
    path('', views.UserPanelDashboardPage.as_view(), name='user_panel_dashboard_page'),
    path('profile-user/', views.InformationUserProfile.as_view(), name='Information_user_profile_page'),
    path('edit_profile/', views.EditUserProfilePage.as_view(), name='edit_user_profile_page'),
    path('change_password/', views.ChangePasswordPage.as_view(), name='change_password_page'),
    path('update_avatar/', views.update_avatar, name='update_avatar'),

    # endregion

    # region User & Group management

    path('users/', views.UserListView.as_view(), name='user_list'),
    path('users/create/', views.UserCreateView.as_view(), name='user_create'),
    path('users/<int:pk>/edit/', views.UserUpdateView.as_view(), name='user_edit'),
    path('users/<int:pk>/delete/', views.UserDeleteView.as_view(), name='user_delete'),

    # endregion

    # region articles management
    path('articles/', views.AuthorArticleListView.as_view(), name='author_articles'),
    path('articles/create/', views.AuthorArticleCreateView.as_view(), name='author_article_create'),
    path('articles/<int:pk>/edit/', views.AuthorArticleUpdateView.as_view(), name='author_article_edit'),
    path('articles/<int:pk>/delete/', views.AuthorArticleDeleteView.as_view(), name='author_article_delete'),

    # endregion
]
