from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('members/', views.members_view, name='members'),
    path('referral/', views.referral_view, name='referral'),
    path('settings/', views.settings_view, name='settings'),
    path('settings/themes/', views.theme_settings, name='theme_settings'),

    # Program hierarchy
    path('programs/<slug:goal_type>/', views.program_list, name='program_list'),
    path('programs/<int:program_id>/plans/', views.plan_list, name='plan_list'),
    path('programs/<int:program_id>/plans/add/', views.plan_create, name='plan_create'),
    path('plans/<int:plan_id>/edit/', views.plan_edit, name='plan_edit'),
    path('plans/<int:plan_id>/delete/', views.plan_delete, name='plan_delete'),
    path('plans/<int:plan_id>/days/', views.day_list, name='day_list'),
    path('months/<int:month_id>/', views.month_detail, name='month_detail'),
    path('weeks/<int:week_id>/', views.week_detail, name='week_detail'),
    path('days/<int:day_id>/', views.day_content, name='day_content'),

    # Content management
    path('days/<int:day_id>/content/add/', views.content_create, name='content_create'),
    path('days/<int:day_id>/content/<int:pk>/edit/', views.content_edit, name='content_edit'),
    path('days/<int:day_id>/content/<int:pk>/delete/', views.content_delete, name='content_delete'),
]
