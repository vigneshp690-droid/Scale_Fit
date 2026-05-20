from datetime import time

from django.core.management.base import BaseCommand
from django.db import transaction

from fitness.models import Day, Plan, Program, ProgramItem, SiteSettings, WorkoutItem


STARTER_PROGRAM_NAME = 'Starter Fitness Program'
STARTER_PLAN_NAME = '2-Day Starter Fitness Plan'

WORKOUT_MEDIA = [
    ('Push Ups', 1, 'https://res.cloudinary.com/demo/image/upload/sample.jpg', 'https://res.cloudinary.com/demo/video/upload/dog.mp4', '12 mins'),
    ('Squats', 1, 'https://media.giphy.com/media/l0HlPystfePnAI3G8/giphy.gif', 'https://res.cloudinary.com/demo/video/upload/elephants.mp4', '15 mins'),
    ('Plank', 2, 'https://res.cloudinary.com/demo/image/upload/w_800,h_500,c_fill/sample.jpg', 'https://res.cloudinary.com/demo/video/upload/dog.mp4', '8 mins'),
    ('Jumping Jacks', 2, 'https://media.giphy.com/media/3o7TKtnuHOHHUjR38Y/giphy.gif', 'https://res.cloudinary.com/demo/video/upload/elephants.mp4', '10 mins'),
]

MEAL_MEDIA = [
    {
        'title': 'Protein Oats Bowl',
        'day_number': 1,
        'category': ProgramItem.BREAKFAST,
        'image': 'https://res.cloudinary.com/demo/image/upload/breakfast.jpg',
        'video': 'https://res.cloudinary.com/demo/video/upload/dog.mp4',
        'description': 'Oats with Greek yogurt, banana, berries, chia seeds, and protein.',
        'calories': 430,
        'protein': 32,
        'carbs': 52,
        'fat': 10,
        'fiber': 9,
        'start_time': time(7, 30),
        'end_time': time(8, 0),
        'diet_type': ProgramItem.DIET_VEGETARIAN,
    },
    {
        'title': 'Grilled Chicken Power Plate',
        'day_number': 1,
        'category': ProgramItem.LUNCH,
        'image': 'https://res.cloudinary.com/demo/image/upload/sample.jpg',
        'video': '',
        'description': 'Lean grilled chicken with brown rice, greens, avocado, and lemon dressing.',
        'calories': 560,
        'protein': 46,
        'carbs': 48,
        'fat': 18,
        'fiber': 7,
        'start_time': time(13, 0),
        'end_time': time(13, 45),
        'diet_type': ProgramItem.DIET_NON_VEGETARIAN,
    },
    {
        'title': 'Green Recovery Smoothie',
        'day_number': 2,
        'category': ProgramItem.SNACKS,
        'image': 'https://media.giphy.com/media/3o7qE1YN7aBOFPRw8E/giphy.gif',
        'video': 'https://res.cloudinary.com/demo/video/upload/dog.mp4',
        'description': 'Spinach, banana, whey protein, almond milk, and flaxseed blended smooth.',
        'calories': 310,
        'protein': 28,
        'carbs': 34,
        'fat': 8,
        'fiber': 6,
        'start_time': time(16, 30),
        'end_time': time(16, 45),
        'diet_type': ProgramItem.DIET_VEGETARIAN,
    },
]


class Command(BaseCommand):
    help = 'Seed duplicate-safe sample meal and workout media for the user website.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--goal-type',
            choices=[Program.WEIGHT_LOSS, Program.WEIGHT_GAIN],
            help='Seed only one goal type. By default, all enabled goal types are seeded.',
        )

    def handle(self, *args, **options):
        settings = SiteSettings.get_solo()
        goal_types = [options['goal_type']] if options.get('goal_type') else settings.enabled_goal_types()
        if not goal_types:
            goal_types = [Program.WEIGHT_LOSS, Program.WEIGHT_GAIN]

        total_meals = 0
        total_workouts = 0
        for goal_type in goal_types:
            meal_count, workout_count = self.seed_goal(goal_type)
            total_meals += meal_count
            total_workouts += workout_count

        self.stdout.write(
            self.style.SUCCESS(
                f'Seeded media demo for {", ".join(goal_types)}: '
                f'{total_meals} meals and {total_workouts} workouts touched.'
            )
        )

    def seed_goal(self, goal_type):
        with transaction.atomic():
            program = (
                Program.objects
                .filter(goal_type=goal_type, is_active=True)
                .exclude(name__iexact='Fitness Media Demo')
                .order_by('name', 'pk')
                .first()
            )

            if not program:
                program, _ = Program.objects.get_or_create(
                    name=STARTER_PROGRAM_NAME,
                    goal_type=goal_type,
                    defaults={'description': 'Starter program with day-wise workouts, meals, and nutrition.', 'is_active': True},
                )

            plan = (
                Plan.objects
                .filter(program=program, plan_type=Plan.PLAN_DAY, is_active=True)
                .exclude(name__iexact='GIF & Video Sample Plan')
                .order_by('display_order', 'name', 'pk')
                .first()
            )

            if not plan:
                plan, _ = Plan.objects.get_or_create(
                    program=program,
                    name=STARTER_PLAN_NAME,
                    defaults={
                        'plan_type': Plan.PLAN_DAY,
                        'count': 2,
                        'description': 'Two-day starter plan with integrated workout media, meals, and nutrition.',
                        'is_active': True,
                    },
                )

            program.is_active = True
            plan.is_active = True
            program.save(update_fields=['is_active', 'updated_at'])
            plan.save(update_fields=['is_active', 'updated_at'])

            days = {}
            for day_number in (1, 2):
                days[day_number], _ = Day.objects.get_or_create(
                    plan=plan,
                    day_number=day_number,
                    defaults={'title': f'Media Demo Day {day_number}', 'is_active': True},
                )

            meal_count = self.seed_meals(days, goal_type)
            workout_count = self.seed_workouts(days, goal_type)

        return meal_count, workout_count

    def seed_meals(self, days, goal_type):
        for order, item in enumerate(MEAL_MEDIA, start=1):
            meal, _ = ProgramItem.objects.get_or_create(
                day=days[item['day_number']],
                title=item['title'],
                meal_category=item['category'],
                defaults={
                    'description': item['description'],
                    'goal_type': goal_type,
                    'display_order': order,
                    'calories': item['calories'],
                    'protein': item['protein'],
                    'carbs': item['carbs'],
                    'fat': item['fat'],
                    'fiber': item['fiber'],
                    'start_time': item['start_time'],
                    'end_time': item['end_time'],
                    'diet_type': item['diet_type'],
                    'is_active': True,
                },
            )
            self.fill_blank_media(meal, item['image'], item['video'])
        return len(MEAL_MEDIA)

    def seed_workouts(self, days, goal_type):
        for order, (title, day_number, image, video, duration) in enumerate(WORKOUT_MEDIA, start=1):
            workout, _ = WorkoutItem.objects.get_or_create(
                day=days[day_number],
                title=title,
                defaults={
                    'description': f'{title} sample media workout.',
                    'duration': duration,
                    'goal_type': goal_type,
                    'display_order': order,
                    'is_active': True,
                },
            )
            self.fill_blank_media(workout, image, video)
        return len(WORKOUT_MEDIA)

    def fill_blank_media(self, instance, image, video):
        # Keep this duplicate-safe: never overwrite media an admin already set.
        update_fields = []
        if image and not instance.image:
            instance.image = image
            update_fields.append('image')
        if video and hasattr(instance, 'video') and not instance.video:
            instance.video = video
            update_fields.append('video')
        if update_fields:
            update_fields.append('updated_at')
            instance.save(update_fields=update_fields)
