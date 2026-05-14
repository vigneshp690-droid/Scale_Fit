from django.shortcuts import render, get_object_or_404, redirect
from fitness.models import Program, Plan, Month, Week, Day, ProgramItem, WorkoutItem, WaterTarget, SiteSettings


def home(request):
    settings = SiteSettings.get_solo()
    loss = Program.objects.none()
    gain = Program.objects.none()
    if settings.enable_weight_loss_programs:
        loss = Program.objects.filter(goal_type='weight_loss', is_active=True)
    if settings.enable_weight_gain_programs:
        gain = Program.objects.filter(goal_type='weight_gain', is_active=True)
    return render(request, 'site_app/home.html', {'loss': loss, 'gain': gain})


def goal_plans(request, goal_type):
    if goal_type not in ['weight_loss', 'weight_gain']:
        return redirect('site_home')
    settings = SiteSettings.get_solo()
    if not settings.is_goal_enabled(goal_type):
        return redirect('site_home')
    programs = Program.objects.filter(goal_type=goal_type, is_active=True)
    plans = Plan.objects.filter(program__in=programs, is_active=True).select_related('program')
    return render(request, 'site_app/goal_plans.html', {
        'plans': plans,
        'goal_type': goal_type,
        'goal_label': goal_type.replace('_', ' ').title(),
    })


def plan_detail(request, plan_id):
    plan = get_object_or_404(Plan, pk=plan_id, is_active=True)
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
    })


def month_weeks(request, plan_id, month_id):
    plan = get_object_or_404(Plan, pk=plan_id, is_active=True)
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
    })


def week_days(request, plan_id, week_id):
    plan = get_object_or_404(Plan, pk=plan_id, is_active=True)
    if not SiteSettings.get_solo().is_goal_enabled(plan.program.goal_type):
        return redirect('site_home')
    week = get_object_or_404(Week, pk=week_id, plan=plan, is_active=True)
    days = Day.objects.filter(plan=plan, week=week, is_active=True).order_by('day_number')
    return render(request, 'site_app/day_list.html', {
        'plan': plan, 'week': week, 'items': days,
        'goal_type': plan.program.goal_type,
        'goal_label': plan.program.goal_type.replace('_', ' ').title(),
    })


def day_detail(request, day_id):
    day = get_object_or_404(Day, pk=day_id, is_active=True)
    settings = SiteSettings.get_solo()
    if not settings.is_goal_enabled(day.plan.program.goal_type):
        return redirect('site_home')
    meals = ProgramItem.objects.filter(day=day, is_active=True, meal_category__in=settings.meal_sections).order_by('display_order')
    workouts = WorkoutItem.objects.filter(day=day, is_active=True).order_by('display_order')
    water = WaterTarget.objects.filter(day=day, is_active=True).order_by('display_order')
    return render(request, 'site_app/day_detail.html', {
        'day': day, 'plan': day.plan,
        'meals': meals, 'workouts': workouts, 'water': water,
        'goal_type': day.plan.program.goal_type,
        'goal_label': day.plan.program.goal_type.replace('_', ' ').title(),
    })
