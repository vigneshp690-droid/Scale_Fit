from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.utils.translation import check_for_language, get_language
from django.views.i18n import set_language as django_set_language
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from .models import UserProfile, ReferralCode, ReferralSignup, SiteTheme, SiteSettings, Program, Plan, Week, Month, Day, ProgramItem, WorkoutItem, DayMedia, WaterTarget
from .forms import (
    ALLOWED_IMAGE_TYPES,
    ProgramForm,
    PlanForm,
    WeekForm,
    MonthForm,
    DayForm,
    ProgramItemForm,
    WorkoutItemForm,
    DayMediaForm,
    WaterTargetForm,
    SiteSettingsForm,
    SiteAppearanceSettingsForm,
    validate_media_upload,
)
from .theme_options import THEME_CHOICES, THEME_SLUGS, get_theme

LANGUAGE_SESSION_KEY = 'django_language'


@require_http_methods(["POST"])
def set_language_session(request):
    response = django_set_language(request)
    language_code = request.POST.get('language')

    if language_code and check_for_language(language_code):
        request.session[LANGUAGE_SESSION_KEY] = language_code
        request.session.modified = True

    return response


@require_http_methods(["GET", "POST"])
def login_view(request):
    """
    Handle user login with username/mobile and password
    """
    if request.method == 'POST':
        username_or_mobile = request.POST.get('username_mobile', '').strip()
        password = request.POST.get('password', '').strip()
        
        # Validate inputs
        if not username_or_mobile or not password:
            messages.error(request, 'Please enter both username/mobile number and password.')
            return render(request, 'fitness/login.html')
        
        # Try to authenticate with username first
        user = authenticate(request, username=username_or_mobile, password=password)
        
        # If not found with username, try to find with mobile number
        if user is None:
            if username_or_mobile.isdigit() and len(username_or_mobile) == 10:
                try:
                    profile = UserProfile.objects.get(mobile_number=username_or_mobile)
                    user = authenticate(request, username=profile.user.username, password=password)
                except UserProfile.DoesNotExist:
                    user = None
                    messages.error(request, 'This mobile number is not registered yet. Please sign up first.')
                    return render(request, 'fitness/login.html')
            else:
                try:
                    profile = UserProfile.objects.get(mobile_number=username_or_mobile)
                    user = authenticate(request, username=profile.user.username, password=password)
                except UserProfile.DoesNotExist:
                    user = None
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            return redirect('dashboard')  # Change 'dashboard' to your desired landing page
        else:
            messages.error(request, 'Invalid credentials. Please check your username/mobile and password.')
            return render(request, 'fitness/login.html')
    
    return render(request, 'fitness/login.html')


@require_http_methods(["GET", "POST"])
def signup_view(request):
    """
    Handle user signup with username, mobile number and password
    """
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        mobile_number = request.POST.get('mobile_number', '').strip()
        password = request.POST.get('password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()

        if not username or not mobile_number or not password or not confirm_password:
            messages.error(request, 'Please complete all fields.')
            return render(request, 'fitness/signup.html')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'fitness/signup.html')

        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
            return render(request, 'fitness/signup.html')

        if not mobile_number.isdigit() or len(mobile_number) != 10:
            messages.error(request, 'Mobile number must be exactly 10 digits.')
            return render(request, 'fitness/signup.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'This username is already taken.')
            return render(request, 'fitness/signup.html')

        if UserProfile.objects.filter(mobile_number=mobile_number).exists():
            messages.error(request, 'This mobile number is already registered.')
            return render(request, 'fitness/signup.html')

        user = User.objects.create_user(username=username, password=password)
        UserProfile.objects.create(user=user, mobile_number=mobile_number)
        login(request, user)
        messages.success(request, 'Your account has been created and you are now logged in.')
        return redirect('dashboard')

    return render(request, 'fitness/signup.html')


CONTENT_SECTIONS = [
    ('meals', 'Meals'),
    ('workout', 'Workout'),
    ('media', 'Day Media'),
    ('water', 'Water'),
]
DEFAULT_SECTION = 'meals'
ITEMS_PER_PAGE = 7


def get_content_config(section):
    if section == 'media':
        return DayMedia, DayMediaForm, 'Day Media'
    if section == 'workout':
        return WorkoutItem, WorkoutItemForm, 'Workout'
    if section == 'water':
        return WaterTarget, WaterTargetForm, 'Water'
    return ProgramItem, ProgramItemForm, 'Meals'


def paginate_queryset(request, queryset, per_page=ITEMS_PER_PAGE):
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get('page', 1)

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return paginator, page_obj


@require_http_methods(["GET"])
@login_required(login_url='login')
def program_list(request, goal_type):
    """
    List programs for a goal type
    """
    goal_type = goal_type.lower()
    if goal_type not in [Program.WEIGHT_LOSS, Program.WEIGHT_GAIN]:
        return redirect('dashboard')

    programs_queryset = (
        Program.objects
        .filter(goal_type=goal_type, is_active=True)
        .exclude(name__iexact='Fitness Media Demo')
        .order_by('name', 'pk')
    )
    paginator, programs = paginate_queryset(request, programs_queryset)

    return render(request, 'fitness/program_list.html', {
        'programs': programs,
        'page_obj': programs,
        'paginator': paginator,
        'goal_type': goal_type,
        'formatted_goal_type': goal_type.replace('_', ' ').title(),
        'view_type': 'programs',
    })


@require_http_methods(["GET"])
@login_required(login_url='login')
def plan_list(request, program_id):
    """
    List plans for a program
    """
    program = get_object_or_404(Program, pk=program_id, is_active=True)
    plans = Plan.objects.filter(program=program, is_active=True)

    return render(request, 'fitness/plan_list.html', {
        'program': program,
        'plans': plans,
        'goal_type': program.goal_type,
        'formatted_goal_type': program.goal_type.replace('_', ' ').title(),
        'view_type': 'plans',
    })


@require_http_methods(["GET", "POST"])
@login_required(login_url='login')
def plan_create(request, program_id):
    """
    Create a new plan for a program
    """
    program = get_object_or_404(Program, pk=program_id, is_active=True)

    if request.method == 'POST':
        form = PlanForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Plan created successfully.')
            return redirect(reverse('plan_list', kwargs={'program_id': program_id}))
    else:
        form = PlanForm(initial={'program': program})

    return render(request, 'fitness/plan_form.html', {
        'form': form,
        'program': program,
        'goal_type': program.goal_type,
        'formatted_goal_type': program.goal_type.replace('_', ' ').title(),
        'action': 'Create',
    })


@require_http_methods(["GET", "POST"])
@login_required(login_url='login')
def plan_edit(request, plan_id):
    """
    Edit an existing plan
    """
    plan = get_object_or_404(Plan, pk=plan_id)
    program = plan.program

    if request.method == 'POST':
        form = PlanForm(request.POST, instance=plan)
        if form.is_valid():
            form.save()
            messages.success(request, 'Plan updated successfully.')
            return redirect(reverse('plan_list', kwargs={'program_id': program.pk}))
    else:
        form = PlanForm(instance=plan)

    return render(request, 'fitness/plan_form.html', {
        'form': form,
        'program': program,
        'goal_type': program.goal_type,
        'formatted_goal_type': program.goal_type.replace('_', ' ').title(),
        'action': 'Update',
        'plan': plan,
    })


@require_http_methods(["GET", "POST"])
@login_required(login_url='login')
def plan_delete(request, plan_id):
    """
    Delete a plan
    """
    plan = get_object_or_404(Plan, pk=plan_id)
    program = plan.program

    if request.method == 'POST':
        plan.delete()
        messages.success(request, 'Plan deleted successfully.')
        return redirect(reverse('plan_list', kwargs={'program_id': program.pk}))

    return render(request, 'fitness/plan_confirm_delete.html', {
        'plan': plan,
        'program': program,
        'goal_type': program.goal_type,
        'formatted_goal_type': program.goal_type.replace('_', ' ').title(),
    })


@require_http_methods(["GET"])
@login_required(login_url='login')
def day_list(request, plan_id):
    """
    List days/weeks/months for a plan based on plan_type
    """
    plan = get_object_or_404(Plan, pk=plan_id, is_active=True)

    if plan.plan_type == Plan.PLAN_MONTHLY:
        months = Month.objects.filter(plan=plan, is_active=True).order_by('month_number')
        if not months.exists():
            for i in range(1, plan.count + 1):
                Month.objects.create(plan=plan, month_number=i)
            months = Month.objects.filter(plan=plan, is_active=True).order_by('month_number')
        paginator, page_obj = paginate_queryset(request, months)
        return render(request, 'fitness/day_list.html', {
            'plan': plan, 'items': page_obj, 'item_type': 'month',
            'page_obj': page_obj, 'paginator': paginator,
            'program': plan.program, 'goal_type': plan.program.goal_type,
            'formatted_goal_type': plan.program.goal_type.replace('_', ' ').title(),
        })

    elif plan.plan_type == Plan.PLAN_WEEKLY:
        weeks = Week.objects.filter(plan=plan, is_active=True).order_by('week_number')
        if not weeks.exists():
            for i in range(1, plan.count + 1):
                Week.objects.create(plan=plan, week_number=i)
            weeks = Week.objects.filter(plan=plan, is_active=True).order_by('week_number')
        paginator, page_obj = paginate_queryset(request, weeks)
        return render(request, 'fitness/day_list.html', {
            'plan': plan, 'items': page_obj, 'item_type': 'week',
            'page_obj': page_obj, 'paginator': paginator,
            'program': plan.program, 'goal_type': plan.program.goal_type,
            'formatted_goal_type': plan.program.goal_type.replace('_', ' ').title(),
        })

    else:  # PLAN_DAY
        days = Day.objects.filter(plan=plan, is_active=True).order_by('day_number')
        if not days.exists():
            for i in range(1, plan.count + 1):
                Day.objects.create(plan=plan, day_number=i)
            days = Day.objects.filter(plan=plan, is_active=True).order_by('day_number')
        paginator, page_obj = paginate_queryset(request, days)
        return render(request, 'fitness/day_list.html', {
            'plan': plan, 'items': page_obj, 'item_type': 'day',
            'page_obj': page_obj, 'paginator': paginator,
            'program': plan.program, 'goal_type': plan.program.goal_type,
            'formatted_goal_type': plan.program.goal_type.replace('_', ' ').title(),
        })


@require_http_methods(["GET"])
@login_required(login_url='login')
def month_detail(request, month_id):
    """
    Show weeks inside a month (4 weeks per month)
    """
    month = get_object_or_404(Month, pk=month_id, is_active=True)
    plan = month.plan
    start_week = (month.month_number - 1) * 4 + 1
    end_week = month.month_number * 4
    weeks = Week.objects.filter(plan=plan, week_number__gte=start_week, week_number__lte=end_week, is_active=True).order_by('week_number')
    if not weeks.exists():
        for i in range(start_week, end_week + 1):
            Week.objects.get_or_create(plan=plan, week_number=i,
                defaults={'title': f"Month {month.month_number} - Week {i - start_week + 1}"})
        weeks = Week.objects.filter(plan=plan, week_number__gte=start_week, week_number__lte=end_week, is_active=True).order_by('week_number')
    return render(request, 'fitness/week_list.html', {
        'plan': plan, 'month': month, 'items': weeks, 'item_type': 'week',
        'program': plan.program, 'goal_type': plan.program.goal_type,
        'formatted_goal_type': plan.program.goal_type.replace('_', ' ').title(),
    })


@require_http_methods(["GET"])
@login_required(login_url='login')
def week_detail(request, week_id):
    """
    Show days inside a week
    """
    week = get_object_or_404(Week, pk=week_id, is_active=True)
    plan = week.plan
    days = Day.objects.filter(plan=plan, week=week, is_active=True).order_by('day_number')
    if not days.exists():
        # Determine day numbers for this week
        week_index = week.week_number - 1
        for i in range(1, 8):  # 7 days per week
            day_num = week_index * 7 + i
            Day.objects.create(plan=plan, week=week, day_number=day_num)
        days = Day.objects.filter(plan=plan, week=week, is_active=True).order_by('day_number')
    return render(request, 'fitness/week_list.html', {
        'plan': plan, 'week': week, 'items': days, 'item_type': 'day',
        'program': plan.program, 'goal_type': plan.program.goal_type,
        'formatted_goal_type': plan.program.goal_type.replace('_', ' ').title(),
    })


@require_http_methods(["GET"])
@login_required(login_url='login')
def day_content(request, day_id):
    """
    Show content for a specific day with tabs for Meals/Workout/Water
    """
    day = get_object_or_404(Day, pk=day_id, is_active=True)
    current_language = get_language()
    section = request.GET.get('section', DEFAULT_SECTION).lower()
    if section not in dict(CONTENT_SECTIONS):
        section = DEFAULT_SECTION

    model, _, section_label = get_content_config(section)
    site_settings = SiteSettings.get_solo()
    items = model.objects.filter(day=day)
    meal_category = ''

    if section == 'meals':
        meal_category = request.GET.get('meal_category', '').lower()
        allowed_categories = dict(
            (value, label)
            for value, label in ProgramItem.CATEGORY_CHOICES
            if value in site_settings.meal_sections
        )
        if meal_category and meal_category in allowed_categories:
            items = items.filter(meal_category=meal_category)
        items = items.filter(meal_category__in=allowed_categories.keys())

    if section == 'water':
        items = items.order_by('display_order')
    else:
        items = items.order_by('display_order', 'title')

    return render(request, 'fitness/day_content.html', {
        'day': day,
        'plan': day.plan,
        'program': day.plan.program,
        'items': items,
        'goal_type': day.plan.program.goal_type,
        'section': section,
        'section_label': section_label,
        'section_choices': CONTENT_SECTIONS,
        'meal_category': meal_category,
        'formatted_goal_type': day.plan.program.goal_type.replace('_', ' ').title(),
        'category_choices': allowed_categories.items() if section == 'meals' else ProgramItem.CATEGORY_CHOICES,
        'view_type': 'content',
        'current_language': current_language,
    })


@require_http_methods(["GET", "POST"])
@login_required(login_url='login')
def content_create(request, day_id):
    """
    Create content item for a day
    """
    day = get_object_or_404(Day, pk=day_id, is_active=True)
    section = request.GET.get('section', DEFAULT_SECTION).lower()
    if section not in dict(CONTENT_SECTIONS):
        section = DEFAULT_SECTION

    _, form_class, section_label = get_content_config(section)

    if request.method == 'POST':
        form = form_class(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.day = day
            if hasattr(item, 'goal_type'):
                item.goal_type = day.plan.program.goal_type
            item.save()
            messages.success(request, f'{section_label} item created successfully.')
            return redirect(reverse('day_content', kwargs={'day_id': day_id}) + f'?section={section}')
    else:
        form = form_class(initial={'day': day})

    return render(request, 'fitness/content_form.html', {
        'form': form,
        'day': day,
        'plan': day.plan,
        'program': day.plan.program,
        'goal_type': day.plan.program.goal_type,
        'section': section,
        'section_label': section_label,
        'action': 'Create',
        'formatted_goal_type': day.plan.program.goal_type.replace('_', ' ').title(),
    })


@require_http_methods(["GET", "POST"])
@login_required(login_url='login')
def content_edit(request, day_id, pk):
    """
    Edit content item for a day
    """
    day = get_object_or_404(Day, pk=day_id, is_active=True)
    section = request.GET.get('section', DEFAULT_SECTION).lower()
    if section not in dict(CONTENT_SECTIONS):
        section = DEFAULT_SECTION

    model, form_class, section_label = get_content_config(section)
    item = get_object_or_404(model, pk=pk, day=day)

    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, f'{section_label} item updated successfully.')
            return redirect(reverse('day_content', kwargs={'day_id': day_id}) + f'?section={section}')
    else:
        form = form_class(instance=item)

    return render(request, 'fitness/content_form.html', {
        'form': form,
        'day': day,
        'plan': day.plan,
        'program': day.plan.program,
        'goal_type': day.plan.program.goal_type,
        'section': section,
        'section_label': section_label,
        'action': 'Update',
        'item': item,
        'formatted_goal_type': day.plan.program.goal_type.replace('_', ' ').title(),
    })


@require_http_methods(["GET", "POST"])
@login_required(login_url='login')
def content_delete(request, day_id, pk):
    """
    Delete content item for a day
    """
    day = get_object_or_404(Day, pk=day_id, is_active=True)
    section = request.GET.get('section', DEFAULT_SECTION).lower()
    if section not in dict(CONTENT_SECTIONS):
        section = DEFAULT_SECTION

    model, _, section_label = get_content_config(section)
    item = get_object_or_404(model, pk=pk, day=day)

    if request.method == 'POST':
        item.delete()
        messages.success(request, f'{section_label} item deleted successfully.')
        return redirect(reverse('day_content', kwargs={'day_id': day_id}) + f'?section={section}')

    return render(request, 'fitness/program_confirm_delete.html', {
        'item': item,
        'day': day,
        'plan': day.plan,
        'program': day.plan.program,
        'goal_type': day.plan.program.goal_type,
        'section': section,
        'section_label': section_label,
        'formatted_goal_type': day.plan.program.goal_type.replace('_', ' ').title(),
    })


@require_http_methods(["GET"])
@login_required(login_url='login')
def members_view(request):
    """
    Admin members page placeholder
    """
    return render(request, 'fitness/members.html')


@require_http_methods(["GET"])
@login_required(login_url='login')
def referral_view(request):
    referral, _ = ReferralCode.objects.get_or_create(user=request.user)
    signups = ReferralSignup.objects.filter(referral_code=referral).select_related('referred_user').order_by('-joined_at')
    total_referrals = signups.count()
    this_month = signups.filter(joined_at__month=__import__('datetime').date.today().month).count()
    referral_link = request.build_absolute_uri(f'/fitness/signup/?ref={referral.code}')
    return render(request, 'fitness/referral.html', {
        'referral': referral,
        'signups': signups,
        'total_referrals': total_referrals,
        'this_month': this_month,
        'referral_link': referral_link,
    })


@require_http_methods(["GET", "POST"])
@login_required(login_url='login')
def settings_view(request):
    site_settings = SiteSettings.get_solo()
    profile, _ = UserProfile.objects.get_or_create(
        user=request.user,
        defaults={'mobile_number': f'{request.user.pk:010d}'[-10:]}
    )
    settings_form = SiteSettingsForm(instance=site_settings)
    appearance_form = SiteAppearanceSettingsForm(instance=site_settings)

    if request.method == 'POST':
        settings_action = request.POST.get('settings_action')

        if settings_action == 'save_site_settings':
            settings_form = SiteSettingsForm(request.POST, instance=site_settings)
            if settings_form.is_valid():
                settings_form.save()
                messages.success(request, 'Settings updated successfully')
                return_anchor = request.POST.get('settings_return_anchor') or 'programs'
                return redirect(f'{reverse("settings")}#{return_anchor}')
            messages.error(request, 'Please correct the highlighted settings fields.')

        elif settings_action == 'save_appearance_settings':
            appearance_form = SiteAppearanceSettingsForm(request.POST, request.FILES, instance=site_settings)
            if appearance_form.is_valid():
                appearance_form.save()
                messages.success(request, 'Settings updated successfully')
                return redirect(f'{reverse("settings")}#theme')
            messages.error(request, 'Please correct the highlighted appearance fields.')

        if settings_action in {'save_site_settings', 'save_appearance_settings'}:
            active_theme_slug = SiteTheme.get_active_slug()
            return render(request, 'fitness/settings.html', {
                'themes': THEME_CHOICES,
                'active_theme_slug': active_theme_slug,
                'active_theme': get_theme(active_theme_slug),
                'profile': profile,
                'site_settings': site_settings,
                'settings_form': settings_form,
                'appearance_form': appearance_form,
            })

        if 'profile_image' in request.FILES:
            try:
                validate_media_upload(request.FILES['profile_image'], ALLOWED_IMAGE_TYPES, 'profile image')
            except ValidationError as exc:
                messages.error(request, ' '.join(exc.messages))
                return redirect('settings')
            if profile.profile_image:
                profile.profile_image.delete(save=False)
            profile.profile_image = request.FILES['profile_image']
            profile.save(update_fields=['profile_image', 'updated_at'])
            messages.success(request, 'Profile image uploaded successfully.')
            return redirect('settings')

        if request.POST.get('profile_action') == 'remove_image':
            if profile.profile_image:
                profile.profile_image.delete(save=False)
                profile.profile_image = None
                profile.save(update_fields=['profile_image', 'updated_at'])
                messages.success(request, 'Profile image removed.')
            else:
                messages.info(request, 'No profile image to remove.')
            return redirect('settings')

        if request.POST.get('profile_action') == 'save_profile':
            full_name = request.POST.get('full_name', '').strip()
            username = request.POST.get('username', '').strip()
            email = request.POST.get('email', '').strip()
            phone = request.POST.get('phone', '').strip()

            if username and username != request.user.username and User.objects.filter(username=username).exclude(pk=request.user.pk).exists():
                messages.error(request, 'That username is already taken.')
                return redirect('settings')

            if phone and phone != profile.mobile_number and UserProfile.objects.filter(mobile_number=phone).exclude(pk=profile.pk).exists():
                messages.error(request, 'That phone number is already in use.')
                return redirect('settings')

            if username:
                request.user.username = username
            request.user.email = email
            name_parts = full_name.split(' ', 1)
            request.user.first_name = name_parts[0] if name_parts else ''
            request.user.last_name = name_parts[1] if len(name_parts) > 1 else ''
            request.user.save(update_fields=['username', 'email', 'first_name', 'last_name'])

            if phone:
                profile.mobile_number = phone
                profile.save(update_fields=['mobile_number', 'updated_at'])

            messages.success(request, 'Profile settings saved.')
            return redirect('settings')

        selected_theme = request.POST.get('theme', '').strip()
        if selected_theme in THEME_SLUGS:
            SiteTheme.set_active_slug(selected_theme)
            messages.success(request, f'{get_theme(selected_theme)["name"]} theme applied to user pages.')
        else:
            messages.error(request, 'Please choose a valid theme.')
        return redirect('settings')

    active_theme_slug = SiteTheme.get_active_slug()
    return render(request, 'fitness/settings.html', {
        'themes': THEME_CHOICES,
        'active_theme_slug': active_theme_slug,
        'active_theme': get_theme(active_theme_slug),
        'profile': profile,
        'site_settings': site_settings,
        'settings_form': settings_form,
        'appearance_form': appearance_form,
    })


@require_http_methods(["GET", "POST"])
@login_required(login_url='login')
def theme_settings(request):
    if request.method == 'POST':
        selected_theme = request.POST.get('theme', '').strip()
        if selected_theme in THEME_SLUGS:
            SiteTheme.set_active_slug(selected_theme)
            messages.success(request, f'{get_theme(selected_theme)["name"]} theme applied to user pages.')
        else:
            messages.error(request, 'Please choose a valid theme.')
        return redirect('theme_settings')

    active_theme_slug = SiteTheme.get_active_slug()
    return render(request, 'fitness/theme_settings.html', {
        'themes': THEME_CHOICES,
        'active_theme_slug': active_theme_slug,
        'active_theme': get_theme(active_theme_slug),
    })


@require_http_methods(["GET"])
@login_required(login_url='login')
def logout_view(request):
    """
    Handle user logout
    """
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')


@login_required(login_url='login')
def dashboard(request):
    """
    Dashboard view (landing page after login)
    """
    site_settings = SiteSettings.get_solo()
    loss_programs = Program.objects.filter(goal_type=Program.WEIGHT_LOSS, is_active=True).count() if site_settings.enable_weight_loss_programs else 0
    gain_programs = Program.objects.filter(goal_type=Program.WEIGHT_GAIN, is_active=True).count() if site_settings.enable_weight_gain_programs else 0
    total_plans = Plan.objects.filter(is_active=True).count()
    total_days = Day.objects.filter(is_active=True).count()

    return render(request, 'fitness/dashboard.html', {
        'loss_programs': loss_programs,
        'gain_programs': gain_programs,
        'total_plans': total_plans,
        'total_days': total_days,
    })
