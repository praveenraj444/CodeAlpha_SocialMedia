from django.urls import path
from . import views

urlpatterns = [
    # ─────────────────────────────────────────
    # AUTH
    # ─────────────────────────────────────────
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # ─────────────────────────────────────────
    # HOME / FEED
    # ─────────────────────────────────────────
    path('', views.home_view, name='home'),

    # ─────────────────────────────────────────
    # PROFILE
    # ─────────────────────────────────────────
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
    path('profile/<str:username>/', views.user_profile_view, name='user_profile'),

    # ─────────────────────────────────────────
    # POST
    # ─────────────────────────────────────────
    path('post/new/', views.create_post_view, name='create_post'),
    path('post/<int:post_id>/delete/', views.delete_post_view, name='delete_post'),

    # ─────────────────────────────────────────
    # LIKE / COMMENT
    # ─────────────────────────────────────────
    path('post/<int:post_id>/like/', views.like_post_view, name='like_post'),
    path('post/<int:post_id>/comment/', views.add_comment_view, name='add_comment'),

    # ─────────────────────────────────────────
    # FOLLOW
    # ─────────────────────────────────────────
    path('follow/<str:username>/', views.follow_toggle_view, name='follow_toggle'),
    path('profile/<str:username>/followers/', views.followers_list_view, name='followers_list'),
    path('profile/<str:username>/following/', views.following_list_view, name='following_list'),
    path('suggested/', views.suggested_users_view, name='suggested_users'),

    # ─────────────────────────────────────────
    # YOUTUBE SEARCH (AJAX)
    # ─────────────────────────────────────────
    path('youtube-search/', views.youtube_search_view, name='youtube_search'),

    # ─────────────────────────────────────────
    # NOTIFICATIONS
    # ─────────────────────────────────────────
    path('notifications/', views.notifications_view, name='notifications'),
    path('notifications/unread-count/', views.unread_count_view, name='unread_count'),
]