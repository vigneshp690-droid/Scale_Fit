from django.test import TestCase
from django.test.client import RequestFactory
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.models import User

from .forms import SiteSettingsForm
from .middleware import SiteSettingsMiddleware
from .models import Day, Plan, Program, SiteSettings, WaterTarget, WorkoutItem


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
