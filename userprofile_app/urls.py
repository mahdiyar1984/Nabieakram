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

    # region User management
    path('users/', views.UserListView.as_view(), name='user_list'),
    path('users/create/', views.UserCreateView.as_view(), name='user_create'),
    path('users/<int:pk>/edit/', views.UserUpdateView.as_view(), name='user_edit'),
    path('users/<int:pk>/delete/', views.UserDeleteView.as_view(), name='user_delete'),
    # endregion

    # region Group management
    path('groups/', views.GroupPermissionMatrixView.as_view(), name='group_list'),
    path('groups/create/', views.GroupCreateView.as_view(), name='group_create'),
    path('groups/<int:pk>/edit/', views.GroupUpdateView.as_view(), name='group_edit'),
    path('groups/<int:pk>/delete/', views.GroupDeleteView.as_view(), name='group_delete'),
    # endregion

    # region articles management
    path('articles/', views.AuthorArticleListView.as_view(), name='articles_list'),
    path('articles/create/', views.AuthorArticleCreateView.as_view(), name='article_create'),
    path('articles/<int:pk>/edit/', views.AuthorArticleUpdateView.as_view(), name='article_edit'),
    path('articles/<int:pk>/delete/', views.AuthorArticleDeleteView.as_view(), name='article_delete'),
    path("articles/<int:pk>/status/", views.ArticleChangeStatusView.as_view(), name="article_change_status"),
    # endregion
]
