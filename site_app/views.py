from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import get_language
from fitness.models import Program, Plan, Month, Week, Day, ProgramItem, WorkoutItem, DayMedia, WaterTarget, SiteSettings


MEDIA_SAMPLE_PLAN_NAME = 'GIF & Video Sample Plan'


def home(request):
    settings = SiteSettings.get_solo()
    current_language = get_language()
    loss = Program.objects.none()
    gain = Program.objects.none()
    if settings.enable_weight_loss_programs:
        loss = Program.objects.filter(goal_type='weight_loss', is_active=True).exclude(name__iexact='Fitness Media Demo')
    if settings.enable_weight_gain_programs:
        gain = Program.objects.filter(goal_type='weight_gain', is_active=True).exclude(name__iexact='Fitness Media Demo')
    return render(request, 'site_app/home.html', {'loss': loss, 'gain': gain, 'current_language': current_language})


def goal_plans(request, goal_type):
    if goal_type not in ['weight_loss', 'weight_gain']:
        return redirect('site_home')
    settings = SiteSettings.get_solo()
    current_language = get_language()
    if not settings.is_goal_enabled(goal_type):
        return redirect('site_home')
    programs = Program.objects.filter(goal_type=goal_type, is_active=True).exclude(name__iexact='Fitness Media Demo')
    plans = (
        Plan.objects
        .filter(program__in=programs, is_active=True)
        .exclude(name__iexact=MEDIA_SAMPLE_PLAN_NAME)
        .select_related('program')
    )
    return render(request, 'site_app/goal_plans.html', {
        'plans': plans,
        'goal_type': goal_type,
        'goal_label': goal_type.replace('_', ' ').title(),
        'current_language': current_language,
    })


def plan_detail(request, plan_id):
    plan = get_object_or_404(Plan, pk=plan_id, is_active=True)
    current_language = get_language()
    if not SiteSettings.get_solo().is_goal_enabled(plan.program.goal_type):
        return redirect('site_home')
    items = []
    item_type = plan.plan_type

    if plan.plan_type == Plan.PLAN_MONTHLY:
        items = Month.objects.filter(plan=plan, is_active=True).order_by('month_number')
    elif plan.plan_type == Plan.PLAN_WEEKLY:
        items = Week.objects.filter(plan=plan, is_active=True).order_by('week_number')
    else:
        items = Day.objects.filter(plan=plan, is_active=True).order_by('day_number')

    return render(request, 'site_app/plan_detail.html', {
        'plan': plan, 'items': items, 'item_type': item_type,
        'goal_type': plan.program.goal_type,
        'goal_label': plan.program.goal_type.replace('_', ' ').title(),
        'current_language': current_language,
    })


def month_weeks(request, plan_id, month_id):
    plan = get_object_or_404(Plan, pk=plan_id, is_active=True)
    current_language = get_language()
    if not SiteSettings.get_solo().is_goal_enabled(plan.program.goal_type):
        return redirect('site_home')
    month = get_object_or_404(Month, pk=month_id, plan=plan, is_active=True)
    start = (month.month_number - 1) * 4 + 1
    end = month.month_number * 4
    weeks = Week.objects.filter(plan=plan, week_number__gte=start, week_number__lte=end, is_active=True).order_by('week_number')
    return render(request, 'site_app/week_list.html', {
        'plan': plan, 'month': month, 'items': weeks,
        'goal_type': plan.program.goal_type,
        'goal_label': plan.program.goal_type.replace('_', ' ').title(),
        'current_language': current_language,
    })


def week_days(request, plan_id, week_id):
    plan = get_object_or_404(Plan, pk=plan_id, is_active=True)
    current_language = get_language()
    if not SiteSettings.get_solo().is_goal_enabled(plan.program.goal_type):
        return redirect('site_home')
    week = get_object_or_404(Week, pk=week_id, plan=plan, is_active=True)
    days = Day.objects.filter(plan=plan, week=week, is_active=True).order_by('day_number')
    return render(request, 'site_app/day_list.html', {
        'plan': plan, 'week': week, 'items': days,
        'goal_type': plan.program.goal_type,
        'goal_label': plan.program.goal_type.replace('_', ' ').title(),
        'current_language': current_language,
    })


def day_detail(request, day_id):
    day = get_object_or_404(Day, pk=day_id, is_active=True)
    settings = SiteSettings.get_solo()
    current_language = get_language()
    if not settings.is_goal_enabled(day.plan.program.goal_type):
        return redirect('site_home')
    meals = ProgramItem.objects.filter(day=day, is_active=True, meal_category__in=settings.meal_sections).order_by('display_order')
    breakfasts = meals.filter(meal_category=ProgramItem.BREAKFAST)
    lunches = meals.filter(meal_category=ProgramItem.LUNCH)
    dinners = meals.filter(meal_category=ProgramItem.DINNER)
    snacks = meals.filter(meal_category=ProgramItem.SNACKS)
    workouts = WorkoutItem.objects.filter(day=day, is_active=True).order_by('display_order')
    workout_videos = workouts.filter(video__isnull=False).exclude(video='')
    exercise_demos = workouts.filter(image__isnull=False).exclude(image='')
    day_media = DayMedia.objects.filter(day=day, is_active=True).exclude(media_file='').order_by('display_order', 'title')
    day_media_videos = day_media.filter(media_type=DayMedia.WORKOUT_VIDEO)
    day_media_demos = day_media.filter(media_type__in=[DayMedia.EXERCISE_GIF, DayMedia.EXERCISE_IMAGE])
    day_media_meals = day_media.filter(media_type=DayMedia.MEAL_IMAGE)
    water = WaterTarget.objects.filter(day=day, is_active=True).order_by('display_order')
    return render(request, 'site_app/day_detail.html', {
        'day': day, 'plan': day.plan,
        'meals': meals,
        'breakfast': breakfasts,
        'breakfasts': breakfasts,
        'lunch': lunches,
        'lunches': lunches,
        'dinner': dinners,
        'dinners': dinners,
        'snacks': snacks,
        'workouts': workouts, 'workout_videos': workout_videos,
        'exercise_demos': exercise_demos, 'day_media_videos': day_media_videos,
        'day_media_demos': day_media_demos, 'day_media_meals': day_media_meals,
        'water': water,
        'goal_type': day.plan.program.goal_type,
        'goal_label': day.plan.program.goal_type.replace('_', ' ').title(),
        'current_language': current_language,
    })


def meal_detail(request, meal_id):
    settings = SiteSettings.get_solo()
    current_language = get_language()
    meal = ProgramItem.objects.select_related('day__plan__program').filter(pk=meal_id, is_active=True).first()
    if not meal or not meal.day_id:
        messages.warning(request, 'That meal is no longer available.')
        return redirect('site_home')

    day = meal.day
    plan = day.plan
    program = plan.program
    if not settings.is_goal_enabled(program.goal_type):
        return redirect('site_home')

    return render(request, 'site_app/meal_detail.html', {
        'meal': meal,
        'day': day,
        'plan': plan,
        'program': program,
        'goal_type': program.goal_type,
        'goal_label': program.goal_type.replace('_', ' ').title(),
        'current_language': current_language,
    })


def workout_detail(request, workout_id):
    settings = SiteSettings.get_solo()
    current_language = get_language()
    workout = WorkoutItem.objects.select_related('day__plan__program').filter(pk=workout_id, is_active=True).first()
    if not workout or not workout.day_id:
        messages.warning(request, 'That workout is no longer available.')
        return redirect('site_home')

    day = workout.day
    plan = day.plan
    program = plan.program
    if not settings.is_goal_enabled(program.goal_type):
        return redirect('site_home')

    return render(request, 'site_app/workout_detail.html', {
        'workout': workout,
        'day': day,
        'plan': plan,
        'program': program,
        'goal_type': program.goal_type,
        'goal_label': program.goal_type.replace('_', ' ').title(),
        'current_language': current_language,
    })
