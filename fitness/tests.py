from django.test import TestCase
from django.test.client import RequestFactory
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils import translation

from .forms import SiteSettingsForm
from .middleware import SiteSettingsMiddleware
from .models import Day, DayMedia, Plan, Program, ProgramItem, SiteSettings, WaterTarget, WorkoutItem


class SiteSettingsFormTests(TestCase):
    def test_program_settings_save_updates_default_duration_workouts_and_water_setting(self):
        settings = SiteSettings.get_solo()
        settings.default_workout_duration = 45
        settings.water_reminder_interval = 60
        settings.save()

        program = Program.objects.create(name='Weight Loss', goal_type=Program.WEIGHT_LOSS)
        plan = Plan.objects.create(program=program, name='Starter', plan_type=Plan.PLAN_DAY, count=1)
        day = Day.objects.create(plan=plan, day_number=1)
        WorkoutItem.objects.create(
            day=day,
            title='Morning HIIT Run',
            duration='45 minutes',
            goal_type=WorkoutItem.WEIGHT_LOSS,
        )
        WorkoutItem.objects.create(
            day=day,
            title='Jump Rope Circuit',
            duration='30 minutes',
            goal_type=WorkoutItem.WEIGHT_LOSS,
        )
        WaterTarget.objects.create(
            day=day,
            target_amount='2.5 Liters',
            reminder_note='Drink water before each meal.',
            goal_type=WaterTarget.WEIGHT_LOSS,
        )

        data = {
            field: getattr(settings, field)
            for field in SiteSettingsForm.Meta.fields
        }
        data['default_workout_duration'] = '90'
        data['water_reminder_interval'] = '120'

        form = SiteSettingsForm(data, instance=settings)
        self.assertTrue(form.is_valid(), form.errors)
        saved_settings = form.save()

        self.assertEqual(saved_settings.default_workout_duration, 90)
        self.assertEqual(saved_settings.water_reminder_interval, 120)
        self.assertEqual(set(WorkoutItem.objects.values_list('duration', flat=True)), {'90 mins'})
        self.assertEqual(WaterTarget.objects.get().reminder_interval_minutes, 120)

        data = {
            field: getattr(saved_settings, field)
            for field in SiteSettingsForm.Meta.fields
        }
        data['default_workout_duration'] = '60'
        data['water_reminder_interval'] = '90'

        form = SiteSettingsForm(data, instance=saved_settings)
        self.assertTrue(form.is_valid(), form.errors)
        saved_settings = form.save()

        self.assertEqual(saved_settings.default_workout_duration, 60)
        self.assertEqual(saved_settings.water_reminder_interval, 90)
        self.assertEqual(set(WorkoutItem.objects.values_list('duration', flat=True)), {'60 mins'})
        self.assertEqual(WaterTarget.objects.get().reminder_interval_minutes, 90)


class FrontendLanguageSwitchingTests(TestCase):
    def test_user_site_uses_site_settings_language(self):
        settings = SiteSettings.get_solo()
        settings.default_language = 'ta'
        settings.save()

        response = self.client.get('/site/')
        self.assertContains(response, 'முகப்பு')
        self.assertContains(response, 'எடை குறைப்பு')

        settings.default_language = 'hi'
        settings.save()

        response = self.client.get('/site/')
        self.assertContains(response, 'होम')
        self.assertContains(response, 'वजन घटाना')

    def test_non_user_site_paths_stay_english(self):
        settings = SiteSettings.get_solo()
        settings.default_language = 'ta'
        settings.save()
        factory = RequestFactory()

        def get_response(request):
            return HttpResponse(request.LANGUAGE_CODE)

        response = SiteSettingsMiddleware(get_response)(factory.get('/fitness/settings/'))

        self.assertEqual(response.content.decode(), 'en')

    def test_dynamic_content_uses_selected_language_with_english_fallback(self):
        program = Program.objects.create(name='Weight Gain', goal_type=Program.WEIGHT_GAIN)
        plan = Plan.objects.create(
            program=program,
            name='10 Day Muscle Kickstart',
            name_ta='10 நாள் தசை தொடக்கம்',
            plan_type=Plan.PLAN_DAY,
            count=1,
        )
        day = Day.objects.create(plan=plan, day_number=1, title='Day 1', title_ta='நாள் 1')
        meal = ProgramItem.objects.create(
            day=day,
            title='Eggs and Steak',
            title_ta='முட்டை மற்றும் ஸ்டேக்',
            description='Three whole eggs scrambled with lean sirloin steak.',
            description_ta='மூன்று முழு முட்டை மற்றும் மெலிந்த ஸ்டேக்.',
            goal_type=ProgramItem.WEIGHT_GAIN,
            meal_category=ProgramItem.BREAKFAST,
            is_active=True,
        )
        WorkoutItem.objects.create(
            day=day,
            title='Push Ups',
            description='Complete controlled reps.',
            goal_type=WorkoutItem.WEIGHT_GAIN,
            is_active=True,
        )

        session = self.client.session
        session['django_language'] = 'ta'
        session.save()
        response = self.client.get(reverse('site_day_detail', kwargs={'day_id': day.pk}))

        self.assertContains(response, 'முட்டை மற்றும் ஸ்டேக்')
        self.assertContains(response, 'மூன்று முழு முட்டை மற்றும் மெலிந்த ஸ்டேக்.')
        self.assertContains(response, 'Push Ups')
        self.assertContains(response, 'Complete controlled reps.')

        with translation.override('hi'):
            self.assertEqual(meal.translated_title, 'Eggs and Steak')

    def test_admin_media_fields_render_on_user_day_detail_for_each_goal_type(self):
        for goal_type in [Program.WEIGHT_LOSS, Program.WEIGHT_GAIN]:
            with self.subTest(goal_type=goal_type):
                program = Program.objects.create(name=f'Media Program {goal_type}', goal_type=goal_type, is_active=True)
                plan = Plan.objects.create(program=program, name='Media Plan', plan_type=Plan.PLAN_DAY, count=1, is_active=True)
                day = Day.objects.create(plan=plan, day_number=1, title='Media Day', is_active=True)
                meal = ProgramItem.objects.create(
                    day=day,
                    title='Healthy Smoothie',
                    image='https://media.giphy.com/media/3o7qE1YN7aBOFPRw8E/giphy.gif',
                    video='https://res.cloudinary.com/demo/video/upload/dog.mp4',
                    description='Protein smoothie with greens.',
                    goal_type=goal_type,
                    meal_category=ProgramItem.BREAKFAST,
                    is_active=True,
                )
                WorkoutItem.objects.create(
                    day=day,
                    title='Push Ups',
                    image='https://media.giphy.com/media/l0HlPystfePnAI3G8/giphy.gif',
                    video='https://res.cloudinary.com/demo/video/upload/elephants.mp4',
                    description='Controlled push up reps.',
                    goal_type=goal_type,
                    is_active=True,
                )

                response = self.client.get(reverse('site_day_detail', kwargs={'day_id': day.pk}))

                self.assertContains(response, '<video', count=2)
                self.assertContains(response, 'https://res.cloudinary.com/demo/video/upload/dog')
                self.assertContains(response, 'https://res.cloudinary.com/demo/video/upload/elephants')
                self.assertContains(response, 'https://media.giphy.com/media/3o7qE1YN7aBOFPRw8E/giphy.gif')
                self.assertContains(response, 'https://media.giphy.com/media/l0HlPystfePnAI3G8/giphy.gif')
                self.assertContains(response, f'href="{reverse("site_meal_detail", kwargs={"meal_id": meal.pk})}"')

                detail_response = self.client.get(reverse('site_meal_detail', kwargs={'meal_id': meal.pk}))
                self.assertContains(detail_response, '<video', count=1)
                self.assertContains(detail_response, 'https://res.cloudinary.com/demo/video/upload/dog')

    def test_missing_meal_detail_redirects_instead_of_debug_404(self):
        response = self.client.get(reverse('site_meal_detail', kwargs={'meal_id': 999999}))

        self.assertRedirects(response, reverse('site_home'))

    def test_video_only_media_renders_without_image_poster(self):
        program = Program.objects.create(name='Video Only Program', goal_type=Program.WEIGHT_GAIN, is_active=True)
        plan = Plan.objects.create(program=program, name='Video Only Plan', plan_type=Plan.PLAN_DAY, count=1, is_active=True)
        day = Day.objects.create(plan=plan, day_number=1, title='Video Only Day', is_active=True)
        meal = ProgramItem.objects.create(
            day=day,
            title='Video Only Meal',
            video='https://res.cloudinary.com/demo/video/upload/dog.mp4',
            goal_type=ProgramItem.WEIGHT_GAIN,
            meal_category=ProgramItem.BREAKFAST,
            is_active=True,
        )
        WorkoutItem.objects.create(
            day=day,
            title='Video Only Workout',
            video='https://res.cloudinary.com/demo/video/upload/elephants.mp4',
            goal_type=WorkoutItem.WEIGHT_GAIN,
            is_active=True,
        )

        day_response = self.client.get(reverse('site_day_detail', kwargs={'day_id': day.pk}))
        self.assertContains(day_response, '<video', count=2)
        self.assertContains(day_response, 'https://res.cloudinary.com/demo/video/upload/dog')
        self.assertContains(day_response, 'https://res.cloudinary.com/demo/video/upload/elephants')
        self.assertNotContains(day_response, 'poster=""')

        detail_response = self.client.get(reverse('site_meal_detail', kwargs={'meal_id': meal.pk}))
        self.assertContains(detail_response, '<video', count=1)
        self.assertNotContains(detail_response, 'poster=""')


class PlanPeriodPaginationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='pass12345')
        self.client.force_login(self.user)

    def test_day_plan_periods_are_paginated_in_groups_of_seven_for_each_goal_type(self):
        for goal_type in [Program.WEIGHT_LOSS, Program.WEIGHT_GAIN]:
            with self.subTest(goal_type=goal_type):
                program = Program.objects.create(
                    name=f'{goal_type} program',
                    goal_type=goal_type,
                )
                plan = Plan.objects.create(
                    program=program,
                    name='14 Day Challenge',
                    plan_type=Plan.PLAN_DAY,
                    count=14,
                )
                for day_number in range(1, 15):
                    Day.objects.create(plan=plan, day_number=day_number)

                first_page = self.client.get(reverse('day_list', kwargs={'plan_id': plan.pk}))
                second_page = self.client.get(reverse('day_list', kwargs={'plan_id': plan.pk}), {'page': 2})

                self.assertEqual(first_page.status_code, 200)
                self.assertEqual(second_page.status_code, 200)
                self.assertEqual([day.day_number for day in first_page.context['items'].object_list], list(range(1, 8)))
                self.assertEqual([day.day_number for day in second_page.context['items'].object_list], list(range(8, 15)))
                self.assertContains(first_page, 'Showing 1-7 of 14 days')
                self.assertContains(second_page, 'Showing 8-14 of 14 days')


class SettingsSecurityTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='security-admin', password='InitialPass123!')
        self.client.force_login(self.user)

    def test_security_update_changes_username_and_password_together(self):
        response = self.client.post(
            reverse('settings'),
            {
                'profile_action': 'update_security',
                'new_username': 'updated-security-admin',
                'current_password': 'InitialPass123!',
                'new_password': 'UpdatedPass123!',
                'confirm_password': 'UpdatedPass123!',
            },
        )

        self.assertRedirects(response, reverse('login'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updated-security-admin')
        self.assertIsNone(authenticate(username='security-admin', password='InitialPass123!'))
        self.assertIsNone(authenticate(username='security-admin', password='InitialPass123!'))
        self.assertEqual(
            authenticate(username='updated-security-admin', password='UpdatedPass123!'),
            self.user,
        )

    def test_security_rejects_duplicate_username(self):
        User.objects.create_user(username='existing-admin', password='OtherPass123!')

        response = self.client.post(
            reverse('settings'),
            {
                'profile_action': 'update_security',
                'new_username': 'existing-admin',
                'current_password': 'InitialPass123!',
                'new_password': 'UpdatedPass123!',
                'confirm_password': 'UpdatedPass123!',
            },
        )

        self.assertRedirects(response, f'{reverse("settings")}#security')
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'security-admin')

    def test_security_requires_username_and_password_together(self):
        response = self.client.post(
            reverse('settings'),
            {
                'profile_action': 'update_security',
                'new_username': 'updated-security-admin',
            },
        )

        self.assertRedirects(response, f'{reverse("settings")}#security')
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'security-admin')
        self.assertEqual(authenticate(username='security-admin', password='InitialPass123!'), self.user)


class AdminMediaCrudTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='admin-media', password='pass12345')
        self.client.force_login(self.user)
        self.program = Program.objects.create(name='Media CRUD Program', goal_type=Program.WEIGHT_GAIN, is_active=True)
        self.plan = Plan.objects.create(program=self.program, name='Media CRUD Plan', plan_type=Plan.PLAN_DAY, count=1, is_active=True)
        self.day = Day.objects.create(plan=self.plan, day_number=1, title='Media CRUD Day', is_active=True)

    def test_custom_admin_media_read_update_delete_flow_reaches_user_site(self):
        meal = ProgramItem.objects.create(
            day=self.day,
            title='Admin GIF Meal',
            image='https://media.giphy.com/media/3o7qE1YN7aBOFPRw8E/giphy.gif',
            video='https://res.cloudinary.com/demo/video/upload/dog.mp4',
            description='Admin-created media meal.',
            goal_type=ProgramItem.WEIGHT_GAIN,
            meal_category=ProgramItem.BREAKFAST,
            is_active=True,
        )

        admin_response = self.client.get(reverse('day_content', kwargs={'day_id': self.day.pk}), {'section': 'meals'})
        self.assertContains(admin_response, 'https://media.giphy.com/media/3o7qE1YN7aBOFPRw8E/giphy.gif')
        self.assertContains(admin_response, 'https://res.cloudinary.com/demo/video/upload/dog')

        user_response = self.client.get(reverse('site_day_detail', kwargs={'day_id': self.day.pk}))
        self.assertContains(user_response, '<video', count=1)
        self.assertContains(user_response, 'Admin GIF Meal')

        edit_response = self.client.post(
            reverse('content_edit', kwargs={'day_id': self.day.pk, 'pk': meal.pk}) + '?section=meals',
            {
                'day': self.day.pk,
                'title': 'Updated Admin GIF Meal',
                'description': 'Updated media meal.',
                'meal_category': ProgramItem.BREAKFAST,
                'display_order': 0,
                'is_active': 'on',
                'image-clear': 'on',
                'video-clear': 'on',
            },
            follow=True,
        )
        self.assertEqual(edit_response.status_code, 200)

        meal.refresh_from_db()
        self.assertEqual(meal.title, 'Updated Admin GIF Meal')
        self.assertFalse(meal.image)
        self.assertFalse(meal.video)

        delete_response = self.client.post(
            reverse('content_delete', kwargs={'day_id': self.day.pk, 'pk': meal.pk}) + '?section=meals',
            follow=True,
        )
        self.assertEqual(delete_response.status_code, 200)
        self.assertFalse(ProgramItem.objects.filter(pk=meal.pk).exists())

    def test_day_media_uploads_are_day_scoped_and_render_inside_day_detail(self):
        video = DayMedia.objects.create(
            day=self.day,
            media_type=DayMedia.WORKOUT_VIDEO,
            title='Day 1 Burn Video',
            description='Follow this Day 1 workout only.',
            media_file='https://res.cloudinary.com/demo/video/upload/dog.mp4',
            is_active=True,
        )
        DayMedia.objects.create(
            day=self.day,
            media_type=DayMedia.EXERCISE_GIF,
            title='Day 1 Squat Demo',
            media_file='https://media.giphy.com/media/l0HlPystfePnAI3G8/giphy.gif',
            is_active=True,
        )
        DayMedia.objects.create(
            day=self.day,
            media_type=DayMedia.MEAL_IMAGE,
            title='Day 1 Breakfast Image',
            media_file='https://res.cloudinary.com/demo/image/upload/sample.jpg',
            is_active=True,
        )
        other_day = Day.objects.create(plan=self.plan, day_number=2, title='Day 2', is_active=True)
        DayMedia.objects.create(
            day=other_day,
            media_type=DayMedia.WORKOUT_VIDEO,
            title='Day 2 Video',
            media_file='https://res.cloudinary.com/demo/video/upload/elephants.mp4',
            is_active=True,
        )

        admin_response = self.client.get(reverse('day_content', kwargs={'day_id': self.day.pk}), {'section': 'media'})
        self.assertContains(admin_response, 'Day 1 Burn Video')
        self.assertContains(admin_response, 'Workout Video')

        user_response = self.client.get(reverse('site_day_detail', kwargs={'day_id': self.day.pk}))
        self.assertContains(user_response, 'Day 1 Burn Video')
        self.assertContains(user_response, 'Day 1 Squat Demo')
        self.assertContains(user_response, 'Day 1 Breakfast Image')
        self.assertContains(user_response, 'https://res.cloudinary.com/demo/video/upload/dog')
        self.assertNotContains(user_response, 'Day 2 Video')
        self.assertTrue(DayMedia.objects.filter(pk=video.pk, day=self.day).exists())
