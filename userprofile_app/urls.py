from django.urls import path
from userprofile_app import views

app_name = "userprofile_app"
urlpatterns = [

    # region Dashboard
    path('', views.UserPanelDashboardPage.as_view(), name='user_panel_dashboard_page'),
    # endregion

    # region Article management
    path('articles/', views.AdminArticleListView.as_view(), name='articles_list'),
    path('articles/create/', views.AdminArticleCreateView.as_view(), name='article_create'),
    path('articles/<int:pk>/edit/', views.AdminArticleUpdateView.as_view(), name='article_edit'),
    path('articles/<int:pk>/delete/', views.AdminArticleDeleteView.as_view(), name='article_delete'),
    path("articles/<int:pk>/status/", views.AdminArticleChangeStatusView.as_view(), name="article_change_status"),
    # endregion
    # region Article Category management
    path('article-categories/', views.AdminArticleCategoryListView.as_view(), name='article_categories_list'),
    path('article-categories/create/', views.article_category_create_view, name='article_category_create'),
    path('article-categories/<int:pk>/read', views.article_category_read_view, name='article_category_read'),
    path('article-categories/<int:pk>/edit/', views.article_category_update_view, name='article_category_edit'),
    path('article-categories/<int:pk>/delete/', views.article_category_delete_view, name='article_category_delete'),
    # endregion
    # region Article Tag management
    path('article-tags/', views.AdminArticleTagListView.as_view(), name='article_tags_list'),
    path("articles/<int:pk>/", views.AdminArticleReadView.as_view(), name="article_detail"),
    path('article-tags/create/', views.AdminArticleTagCreateView.as_view(), name='article_tag_create'),
    path('article-tags/<int:pk>/edit/', views.AdminArticleTagUpdateView.as_view(), name='article_tag_edit'),
    path('article-tags/<int:pk>/delete/', views.AdminArticleTagDeleteView.as_view(), name='article_tag_delete'),
    # endregion
    # region Article Comment management
    path('article-comments/', views.AdminArticleCommentListView.as_view(), name='article_comments_list'),
    path('article-comments/create/', views.AdminArticleCommentCreateView.as_view(), name='article_comment_create'),
    path('article-comments/<int:pk>/edit/', views.AdminArticleCommentUpdateView.as_view(), name='article_comment_edit'),
    path('article-comments/<int:pk>/delete/', views.AdminArticleCommentDeleteView.as_view(),
         name='article_comment_delete'),
    # endregion

    # region Lecture management
    path('lectures/', views.AdminLectureListView.as_view(), name='lectures_list'),
    path('lecturess/create/', views.AdminLectureCreateView.as_view(), name='lecture_create'),
    path('lecturess/<int:pk>/edit/', views.AdminLectureUpdateView.as_view(), name='lecture_edit'),
    path('lecturess/<int:pk>/delete/', views.AdminLectureDeleteView.as_view(), name='lecture_delete'),
    # endregion
    # region Lecture Category management
    path('lecture-categories/', views.AdminLectureCategoryListView.as_view(), name='lecture_categories_list'),
    path('lecture-categories/create/', views.AdminLectureCategoryCreateView.as_view(), name='lecture_category_create'),
    path('lecture-categories/<int:pk>/edit/', views.AdminLectureCategoryUpdateView.as_view(),
         name='lecture_category_edit'),
    path('lecture-categories/<int:pk>/delete/', views.AdminLectureCategoryDeleteView.as_view(),
         name='lecture_category_delete'),
    # endregion
    # region Lecture Tag management
    path('lecture-tags/', views.AdminLectureTagListView.as_view(), name='lecture_tags_list'),
    path('lecture-tags/create/', views.AdminLectureTagCreateView.as_view(), name='lecture_tag_create'),
    path('lecture-tags/<int:pk>/edit/', views.AdminLectureTagUpdateView.as_view(), name='lecture_tag_edit'),
    path('lecture-tags/<int:pk>/delete/', views.AdminLectureTagDeleteView.as_view(), name='lecture_tag_delete'),
    # endregion
    # region Lecture Comment management
    path('lecture-comments/', views.AdminLectureCommentListView.as_view(), name='lecture_comments_list'),
    path('lecture-comments/create/', views.AdminLectureCommentCreateView.as_view(), name='lecture_comment_create'),
    path('lecture-comments/<int:pk>/edit/', views.AdminLectureCommentUpdateView.as_view(), name='lecture_comment_edit'),
    path('lecture-comments/<int:pk>/delete/', views.AdminLectureCommentDeleteView.as_view(),
         name='lecture_comment_delete'),
    # endregion

    # region Gallery management
    path('galleries/', views.AdminGalleryImageListView.as_view(), name='galleries_list'),
    path('galleries/create/', views.AdminGalleryImageCreateView.as_view(), name='gallery_create'),
    path('galleries/<int:pk>/edit/', views.AdminGalleryImageUpdateView.as_view(), name='gallery_edit'),
    path('galleries/<int:pk>/delete/', views.AdminGalleryImageDeleteView.as_view(), name='gallery_delete'),
    # endregion
    # region Gallery Category management
    path('gallery-categories/', views.AdminGalleryCategoryListView.as_view(), name='gallery_categories_list'),
    path('gallery-categories/create/', views.AdminGalleryCategoryCreateView.as_view(), name='gallery_category_create'),
    path('gallery-categories/<int:pk>/edit/', views.AdminGalleryCategoryUpdateView.as_view(),
         name='gallery_category_edit'),
    path('gallery-categories/<int:pk>/delete/', views.AdminGalleryCategoryDeleteView.as_view(),
         name='gallery_category_delete'),
    # endregion

    # region FooterLink management
    path('footer-links/', views.AdminFooterLinkListView.as_view(), name='footer_links_list'),
    path('footer-links/create/', views.AdminFooterLinkCreateView.as_view(), name='footer_link_create'),
    path('footer-links/<int:pk>/edit/', views.AdminFooterLinkUpdateView.as_view(), name='footer_link_edit'),
    path('footer-links/<int:pk>/delete/', views.AdminFooterLinkDeleteView.as_view(), name='footer_link_delete'),
    # endregion
    # region FooterLinkBox management
    path('footer-link-boxes/', views.AdminFooterLinkBoxListView.as_view(), name='footer_link_boxes_list'),
    path('footer-link-boxes/create/', views.AdminFooterLinkBoxCreateView.as_view(), name='footer_link_box_create'),
    path('footer-link-boxes/<int:pk>/edit/', views.AdminFooterLinkBoxUpdateView.as_view(), name='footer_link_box_edit'),
    path('footer-link-boxes/<int:pk>/delete/', views.AdminFooterLinkBoxDeleteView.as_view(),
         name='footer_link_box_delete'),
    # endregion

    # region Contact Us management
    path('contact-us/', views.AdminContactUsListView.as_view(), name='contact_us_list'),
    path('contact-us/<int:pk>/edit/', views.AdminContactUsUpdateView.as_view(), name='contact_us_edit'),
    # endregion

    # region Slider management
    path('sliders/', views.AdminSliderListView.as_view(), name='sliders_list'),
    path('sliders/<int:pk>/edit/', views.AdminSliderUpdateView.as_view(), name='slider_edit'),
    # endregion

    # region SiteSetting management
    path('Site-Settings/', views.AdminSiteSettingListView.as_view(), name='site_Settings_list'),
    path('Site-Setting/<int:pk>/edit/', views.AdminSiteSettingUpdateView.as_view(), name='Site_Setting_edit'),
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

    # region User Profile
    path('profile-user/', views.InformationUserProfile.as_view(), name='Information_user_profile_page'),
    path('edit_profile/', views.EditUserProfilePage.as_view(), name='edit_user_profile_page'),
    path('change_password/', views.ChangePasswordPage.as_view(), name='change_password_page'),
    path('update_avatar/', views.update_avatar, name='update_avatar'),
    # endregion
]
