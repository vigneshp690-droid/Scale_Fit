from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='site_home'),
    path('<slug:goal_type>/', views.goal_plans, name='site_goal_plans'),
    path('plan/<int:plan_id>/', views.plan_detail, name='site_plan_detail'),
    path('plan/<int:plan_id>/week/<int:week_id>/', views.week_days, name='site_week_days'),
    path('plan/<int:plan_id>/month/<int:month_id>/', views.month_weeks, name='site_month_weeks'),
    path('day/<int:day_id>/', views.day_detail, name='site_day_detail'),
    path('meal/<int:meal_id>/', views.meal_detail, name='site_meal_detail'),
    path('workout/<int:workout_id>/', views.workout_detail, name='site_workout_detail'),
]
