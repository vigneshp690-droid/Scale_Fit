import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ScaleFit.settings')
django.setup()

from fitness.models import Program, Plan, Day, ProgramItem, WorkoutItem, WaterTarget, Week, Month

# ─── CLEAR ALL ───────────────────────────────────────────────────────────────
print("Clearing existing data...")
WaterTarget.objects.all().delete()
WorkoutItem.objects.all().delete()
ProgramItem.objects.all().delete()
Day.objects.all().delete()
Week.objects.all().delete()
Month.objects.all().delete()
Plan.objects.all().delete()
Program.objects.all().delete()
print("Done clearing.")

# ─── UNSPLASH IMAGE POOLS ────────────────────────────────────────────────────
MEAL_IMAGES = {
    'breakfast': [
        'program_images/meal_b1.jpg',
        'program_images/meal_b2.jpg',
        'program_images/meal_b3.jpg',
        'program_images/meal_b4.jpg',
        'program_images/meal_b5.jpg',
        'program_images/meal_b6.jpg',
        'program_images/meal_b7.jpg',
    ],
    'lunch': [
        'program_images/meal_l1.jpg',
        'program_images/meal_l2.jpg',
        'program_images/meal_l3.jpg',
        'program_images/meal_l4.jpg',
        'program_images/meal_l5.jpg',
        'program_images/meal_l6.jpg',
        'program_images/meal_l7.jpg',
    ],
    'dinner': [
        'program_images/meal_d1.jpg',
        'program_images/meal_d2.jpg',
        'program_images/meal_d3.jpg',
        'program_images/meal_d4.jpg',
        'program_images/meal_d5.jpg',
        'program_images/meal_d6.jpg',
        'program_images/meal_d7.jpg',
    ],
    'snacks': [
        'program_images/meal_s1.jpg',
        'program_images/meal_s2.jpg',
        'program_images/meal_s3.jpg',
        'program_images/meal_s4.jpg',
        'program_images/meal_s5.jpg',
        'program_images/meal_s6.jpg',
        'program_images/meal_s7.jpg',
    ],
}

WORKOUT_IMAGES = [
    'workout_images/workout_1.jpg',
    'workout_images/workout_2.jpg',
    'workout_images/workout_3.jpg',
    'workout_images/workout_4.jpg',
    'workout_images/workout_5.jpg',
    'workout_images/workout_6.jpg',
    'workout_images/workout_7.jpg',
]

import urllib.request, os
from pathlib import Path

BASE_MEDIA = Path('/home/viki/Desktop/ScaleFit/media')
(BASE_MEDIA / 'program_images').mkdir(parents=True, exist_ok=True)
(BASE_MEDIA / 'workout_images').mkdir(parents=True, exist_ok=True)

UNSPLASH_MEALS = {
    'breakfast': [
        'https://images.unsplash.com/photo-1533089860892-a7c6f0a88666?w=600&q=80',
        'https://images.unsplash.com/photo-1484723091739-30a097e8f929?w=600&q=80',
        'https://images.unsplash.com/photo-1525351484163-7529414344d8?w=600&q=80',
        'https://images.unsplash.com/photo-1494597564530-871f2b93ac55?w=600&q=80',
        'https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=600&q=80',
        'https://images.unsplash.com/photo-1490645935967-10de6ba17061?w=600&q=80',
        'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=600&q=80',
    ],
    'lunch': [
        'https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=600&q=80',
        'https://images.unsplash.com/photo-1547592180-85f173990554?w=600&q=80',
        'https://images.unsplash.com/photo-1529059997568-3d847b1154f0?w=600&q=80',
        'https://images.unsplash.com/photo-1498837167922-ddd27525d352?w=600&q=80',
        'https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?w=600&q=80',
        'https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=600&q=80',
        'https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?w=600&q=80',
    ],
    'dinner': [
        'https://images.unsplash.com/photo-1559847844-5315695dadae?w=600&q=80',
        'https://images.unsplash.com/photo-1574484284002-952d92456975?w=600&q=80',
        'https://images.unsplash.com/photo-1432139555190-58524dae6a55?w=600&q=80',
        'https://images.unsplash.com/photo-1467003909585-2f8a72700288?w=600&q=80',
        'https://images.unsplash.com/photo-1476224203421-9ac39bcb3327?w=600&q=80',
        'https://images.unsplash.com/photo-1455619452474-d2be8b1e70cd?w=600&q=80',
        'https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=600&q=80',
    ],
    'snacks': [
        'https://images.unsplash.com/photo-1505253716362-afaea1d3d1af?w=600&q=80',
        'https://images.unsplash.com/photo-1571748982800-fa51082c2224?w=600&q=80',
        'https://images.unsplash.com/photo-1482049016688-2d3e1b311543?w=600&q=80',
        'https://images.unsplash.com/photo-1511690743698-d9d85f2fbf38?w=600&q=80',
        'https://images.unsplash.com/photo-1558961363-fa8fdf82db35?w=600&q=80',
        'https://images.unsplash.com/photo-1499195333224-3ce974eecb47?w=600&q=80',
        'https://images.unsplash.com/photo-1607532941433-304659e8198a?w=600&q=80',
    ],
}

UNSPLASH_WORKOUTS = [
    'https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=600&q=80',
    'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=600&q=80',
    'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=600&q=80',
    'https://images.unsplash.com/photo-1583454110551-21f2fa2afe61?w=600&q=80',
    'https://images.unsplash.com/photo-1526506118085-60ce8714f8c5?w=600&q=80',
    'https://images.unsplash.com/photo-1581009146145-b5ef050c2e1e?w=600&q=80',
    'https://images.unsplash.com/photo-1549060279-7e168fcee0c2?w=600&q=80',
]

def download_image(url, local_path):
    full_path = BASE_MEDIA / local_path
    if not full_path.exists():
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=15) as r, open(full_path, 'wb') as f:
                f.write(r.read())
            print(f"  Downloaded: {local_path}")
        except Exception as e:
            print(f"  FAILED {local_path}: {e}")
            return None
    return local_path

print("\nDownloading images...")
for cat, urls in UNSPLASH_MEALS.items():
    for i, url in enumerate(urls, 1):
        download_image(url, MEAL_IMAGES[cat][i-1])

for i, url in enumerate(UNSPLASH_WORKOUTS, 1):
    download_image(url, WORKOUT_IMAGES[i-1])

print("Images ready.\n")

# ─── MEAL DATA ───────────────────────────────────────────────────────────────

# Weight Loss meals - low calorie, high fiber, lean protein
WL_MEALS = {
    'breakfast': [
        ('Oatmeal with Berries', 'Steel-cut oats topped with fresh blueberries, strawberries and a drizzle of honey. Rich in fiber to keep you full.', '07:00', '07:30'),
        ('Greek Yogurt Parfait', 'Low-fat Greek yogurt layered with granola, kiwi and mixed berries. High protein, low sugar morning fuel.', '07:00', '07:30'),
        ('Avocado Egg Toast', 'Whole grain toast topped with mashed avocado, poached eggs and chili flakes. Healthy fats and protein.', '07:00', '07:30'),
        ('Green Smoothie Bowl', 'Blended spinach, banana and almond milk topped with chia seeds, flaxseeds and sliced fruits.', '07:00', '07:30'),
        ('Veggie Omelette', 'Three-egg white omelette with bell peppers, spinach, mushrooms and low-fat cheese.', '07:00', '07:30'),
        ('Chia Pudding', 'Overnight chia seeds soaked in almond milk, topped with mango chunks and coconut flakes.', '07:00', '07:30'),
        ('Whole Grain Pancakes', 'Fluffy whole wheat pancakes with fresh strawberries and a light drizzle of maple syrup.', '07:00', '07:30'),
    ],
    'lunch': [
        ('Grilled Chicken Salad', 'Grilled chicken breast on a bed of mixed greens, cherry tomatoes, cucumber and lemon vinaigrette.', '12:30', '13:00'),
        ('Quinoa Buddha Bowl', 'Quinoa with roasted chickpeas, sweet potato, kale, avocado and tahini dressing.', '12:30', '13:00'),
        ('Turkey Lettuce Wraps', 'Lean ground turkey with water chestnuts, carrots and hoisin sauce wrapped in butter lettuce.', '12:30', '13:00'),
        ('Lentil Soup', 'Hearty red lentil soup with turmeric, cumin, spinach and a squeeze of lemon.', '12:30', '13:00'),
        ('Tuna Stuffed Peppers', 'Bell peppers stuffed with tuna, celery, onion and light mayo. Baked until tender.', '12:30', '13:00'),
        ('Zucchini Noodles', 'Spiralized zucchini with cherry tomatoes, basil pesto and grilled shrimp.', '12:30', '13:00'),
        ('Cauliflower Rice Bowl', 'Cauliflower rice with black beans, corn, salsa, lime and grilled chicken strips.', '12:30', '13:00'),
    ],
    'dinner': [
        ('Baked Salmon', 'Herb-crusted salmon fillet with steamed broccoli and lemon-garlic asparagus.', '19:00', '19:30'),
        ('Grilled Tilapia', 'Lemon-pepper tilapia with roasted Brussels sprouts and a side of brown rice.', '19:00', '19:30'),
        ('Chicken Stir Fry', 'Lean chicken breast with mixed vegetables in a light soy-ginger sauce over cauliflower rice.', '19:00', '19:30'),
        ('Turkey Meatballs', 'Lean turkey meatballs in marinara sauce with zucchini noodles and fresh basil.', '19:00', '19:30'),
        ('Shrimp Tacos', 'Grilled shrimp in corn tortillas with cabbage slaw, avocado and lime crema.', '19:00', '19:30'),
        ('Stuffed Chicken Breast', 'Chicken breast stuffed with spinach and feta, served with roasted sweet potato.', '19:00', '19:30'),
        ('Vegetable Curry', 'Light coconut milk curry with chickpeas, spinach, tomatoes and brown rice.', '19:00', '19:30'),
    ],
    'snacks': [
        ('Apple with Almond Butter', 'Sliced apple with 1 tbsp natural almond butter. Perfect balance of fiber and healthy fats.', '10:30', '10:45'),
        ('Celery and Hummus', 'Crunchy celery sticks with 2 tbsp homemade hummus. Low calorie, high fiber snack.', '10:30', '10:45'),
        ('Mixed Nuts', 'A small handful of almonds, walnuts and cashews. Healthy fats and protein.', '10:30', '10:45'),
        ('Cucumber Slices', 'Fresh cucumber slices with tzatziki dip. Hydrating and low calorie.', '10:30', '10:45'),
        ('Protein Smoothie', 'Whey protein with almond milk, banana and spinach. Post-workout recovery drink.', '10:30', '10:45'),
        ('Rice Cakes', 'Brown rice cakes with avocado and a sprinkle of sea salt. Light and satisfying.', '10:30', '10:45'),
        ('Boiled Eggs', 'Two hard-boiled eggs with a pinch of salt and pepper. High protein, portable snack.', '10:30', '10:45'),
    ],
}

# Weight Gain meals - high calorie, high protein, complex carbs
WG_MEALS = {
    'breakfast': [
        ('Protein Pancake Stack', 'Thick protein pancakes with peanut butter, banana slices and maple syrup. 650 calories of muscle fuel.', '07:00', '07:45'),
        ('Eggs and Steak', 'Three whole eggs scrambled with a lean sirloin steak, whole grain toast and orange juice.', '07:00', '07:45'),
        ('Mass Gainer Smoothie', 'Whole milk, oats, banana, peanut butter, whey protein and honey blended together. 800+ calories.', '07:00', '07:45'),
        ('Breakfast Burrito', 'Whole wheat tortilla with scrambled eggs, black beans, cheese, avocado and salsa.', '07:00', '07:45'),
        ('Oatmeal Power Bowl', 'Large bowl of oats with whole milk, whey protein, peanut butter, banana and mixed nuts.', '07:00', '07:45'),
        ('French Toast', 'Thick-cut whole grain French toast with eggs, topped with berries and Greek yogurt.', '07:00', '07:45'),
        ('Cottage Cheese Bowl', 'Full-fat cottage cheese with granola, honey, walnuts and fresh pineapple chunks.', '07:00', '07:45'),
    ],
    'lunch': [
        ('Chicken Rice Bowl', 'Double portion of grilled chicken thighs over white rice with teriyaki sauce and steamed broccoli.', '13:00', '13:45'),
        ('Beef and Pasta', 'Lean ground beef bolognese over whole wheat pasta with parmesan and garlic bread.', '13:00', '13:45'),
        ('Salmon Quinoa Bowl', 'Grilled salmon fillet over quinoa with roasted vegetables and avocado.', '13:00', '13:45'),
        ('Turkey Sub', 'Footlong whole grain sub with turkey, cheese, avocado, veggies and olive oil.', '13:00', '13:45'),
        ('Tuna Pasta Salad', 'Whole wheat pasta with tuna, olive oil, cherry tomatoes, olives and feta cheese.', '13:00', '13:45'),
        ('Chicken Burrito Bowl', 'Large burrito bowl with chicken, brown rice, black beans, cheese, sour cream and guacamole.', '13:00', '13:45'),
        ('Steak and Potatoes', 'Grilled sirloin steak with mashed potatoes, green beans and a side salad.', '13:00', '13:45'),
    ],
    'dinner': [
        ('Beef Stir Fry', 'Lean beef strips with mixed vegetables, noodles and oyster sauce. High protein evening meal.', '19:30', '20:00'),
        ('Baked Chicken Thighs', 'Juicy baked chicken thighs with roasted sweet potatoes and garlic green beans.', '19:30', '20:00'),
        ('Salmon and Rice', 'Pan-seared salmon with jasmine rice, edamame and miso soup.', '19:30', '20:00'),
        ('Lamb Chops', 'Herb-marinated lamb chops with roasted potatoes and mint yogurt sauce.', '19:30', '20:00'),
        ('Chicken Pasta', 'Creamy chicken and mushroom pasta with whole wheat penne and parmesan.', '19:30', '20:00'),
        ('Pork Tenderloin', 'Roasted pork tenderloin with apple sauce, roasted carrots and mashed sweet potato.', '19:30', '20:00'),
        ('Beef Tacos', 'Seasoned ground beef tacos with cheese, sour cream, guacamole and pico de gallo.', '19:30', '20:00'),
    ],
    'snacks': [
        ('Peanut Butter Banana', 'Two bananas with 3 tbsp peanut butter. Quick 400-calorie muscle-building snack.', '10:30', '10:45'),
        ('Protein Shake', 'Double scoop whey protein with whole milk and oats. 500 calories post-workout.', '10:30', '10:45'),
        ('Trail Mix', 'Large handful of mixed nuts, dried fruits, dark chocolate chips and seeds.', '10:30', '10:45'),
        ('Cheese and Crackers', 'Whole grain crackers with cheddar cheese and sliced turkey. Protein-rich snack.', '10:30', '10:45'),
        ('Greek Yogurt', 'Full-fat Greek yogurt with honey, granola and mixed berries. 350 calories.', '10:30', '10:45'),
        ('Avocado Toast', 'Two slices whole grain toast with avocado, eggs and everything bagel seasoning.', '10:30', '10:45'),
        ('Milk and Cookies', 'Two whole grain oat cookies with a large glass of whole milk. 400 calories.', '10:30', '10:45'),
    ],
}

# Weight Loss workouts - cardio, HIIT, fat burn
WL_WORKOUTS = [
    ('Morning HIIT Run', '30 minutes of high-intensity interval running. Alternate 1 min sprint with 2 min jog. Burns 350-400 calories.', '45 minutes'),
    ('Jump Rope Circuit', 'Jump rope intervals: 3 sets of 5 minutes with 1 minute rest. Excellent cardio and coordination.', '30 minutes'),
    ('Cycling Session', 'Moderate to high intensity cycling. Maintain 75-85% max heart rate throughout. Great fat burner.', '45 minutes'),
    ('Bodyweight Circuit', 'Push-ups, squats, lunges, burpees and mountain climbers. 4 rounds of 15 reps each.', '40 minutes'),
    ('Swimming Laps', 'Freestyle swimming laps with 30 second rest between sets. Full body low-impact cardio.', '45 minutes'),
    ('Yoga Flow', 'Dynamic yoga flow focusing on core strength, flexibility and mindful breathing.', '50 minutes'),
    ('Stair Climbing', 'Stair climbing intervals for lower body strength and cardio. 10 sets of 3 floors.', '35 minutes'),
    ('Dance Cardio', 'High energy dance workout targeting full body fat burn. Fun and effective.', '40 minutes'),
    ('Rowing Machine', 'Rowing intervals: 500m hard, 250m easy. Repeat 6 times. Full body cardio.', '35 minutes'),
    ('Pilates Core', 'Pilates-based core workout focusing on deep abdominal muscles and posture.', '45 minutes'),
]

# Weight Gain workouts - strength, compound lifts, muscle building
WG_WORKOUTS = [
    ('Bench Press', 'Flat bench press: 4 sets of 8-10 reps at 75% 1RM. Primary chest and tricep builder.', '50 minutes'),
    ('Squat Session', 'Back squats: 5 sets of 5 reps heavy weight. King of all muscle-building exercises.', '55 minutes'),
    ('Deadlift Day', 'Conventional deadlifts: 4 sets of 6 reps. Full posterior chain activation for mass.', '50 minutes'),
    ('Pull-Up and Row', 'Weighted pull-ups and barbell rows: 4 sets each. Back width and thickness builder.', '50 minutes'),
    ('Shoulder Press', 'Overhead press and lateral raises: 4 sets of 10. Boulder shoulder development.', '45 minutes'),
    ('Leg Press Day', 'Leg press, leg curls and calf raises: 4 sets of 12. Complete lower body mass builder.', '55 minutes'),
    ('Bicep and Tricep', 'Barbell curls and skull crushers: 4 sets of 10 each. Arm size and strength.', '45 minutes'),
    ('Power Clean', 'Olympic power cleans: 5 sets of 3 reps. Explosive full body strength and power.', '50 minutes'),
    ('Incline Press', 'Incline dumbbell press and cable flyes: 4 sets of 10. Upper chest development.', '50 minutes'),
    ('Romanian Deadlift', 'RDL and glute bridges: 4 sets of 10. Hamstring and glute mass builder.', '45 minutes'),
]

# ─── HELPER ──────────────────────────────────────────────────────────────────
def get_meal_img(cat, day_num):
    return MEAL_IMAGES[cat][(day_num - 1) % 7]

def get_workout_img(day_num, offset=0):
    return WORKOUT_IMAGES[(day_num - 1 + offset) % 7]

def get_meal_data(meals_dict, cat, day_num):
    return meals_dict[cat][(day_num - 1) % 7]

def get_workout_data(workouts_list, day_num, offset=0):
    return workouts_list[(day_num - 1 + offset) % len(workouts_list)]

def seed_day(day, goal_type, day_num):
    meals_data = WL_MEALS if goal_type == 'weight_loss' else WG_MEALS
    workouts_data = WL_WORKOUTS if goal_type == 'weight_loss' else WG_WORKOUTS

    # 4 meals
    for order, cat in enumerate(['breakfast', 'lunch', 'snacks', 'dinner'], 1):
        title, desc, start, end = get_meal_data(meals_data, cat, day_num + order)
        ProgramItem.objects.create(
            day=day, title=title, description=desc,
            goal_type=goal_type, meal_category=cat,
            image=get_meal_img(cat, day_num + order),
            start_time=start, end_time=end,
            display_order=order, is_active=True,
            calories=450 if goal_type == 'weight_loss' else 750,
            protein=30.0, carbs=45.0, fat=15.0, fiber=8.0,
            vitamins='Vitamin A, Vitamin C', minerals='Iron, Calcium'
        )

    # 2 workouts
    for offset in range(2):
        w_title, w_desc, w_dur = get_workout_data(workouts_data, day_num, offset)
        WorkoutItem.objects.create(
            day=day, title=w_title, description=w_desc,
            goal_type=goal_type, duration=w_dur,
            image=get_workout_img(day_num, offset),
            display_order=offset + 1, is_active=True
        )

    # 1 water target
    if goal_type == 'weight_loss':
        amount = '2.5 Liters'
        note = f'Day {day_num}: Drink water before each meal. Stay hydrated to boost metabolism and reduce hunger.'
    else:
        amount = '3.5 Liters'
        note = f'Day {day_num}: Hydration is key for muscle recovery. Drink extra water post-workout.'

    WaterTarget.objects.create(
        day=day, target_amount=amount,
        reminder_note=note, goal_type=goal_type,
        display_order=1, is_active=True
    )

# ─── CREATE PROGRAMS ─────────────────────────────────────────────────────────
print("Creating programs...")
wl_program = Program.objects.create(
    name='Weight Loss Program',
    goal_type='weight_loss',
    description='Science-backed weight loss program combining clean eating and cardio workouts to burn fat effectively.',
    is_active=True
)
wg_program = Program.objects.create(
    name='Weight Gain Program',
    goal_type='weight_gain',
    description='High-calorie nutrition and strength training program designed to build lean muscle mass and increase body weight.',
    is_active=True
)

# ─── CREATE PLANS ────────────────────────────────────────────────────────────
print("Creating plans...")
plans = [
    (wl_program, '7 Day Fat Burn Challenge',        'day', 7,  1, 'weight_loss',
     'A 7-day intensive fat-burning program with HIIT workouts and clean low-calorie meals to kickstart your weight loss journey.'),
    (wl_program, '30 Day Lean Body Transformation', 'day', 30, 2, 'weight_loss',
     'A complete 30-day transformation plan with progressive cardio workouts and a structured meal plan to achieve a lean, toned body.'),
    (wg_program, '10 Day Muscle Kickstart',         'day', 10, 1, 'weight_gain',
     'A 10-day high-intensity strength program with calorie-dense meals to rapidly kickstart muscle growth and weight gain.'),
    (wg_program, '20 Day Mass Builder Program',     'day', 20, 2, 'weight_gain',
     'A 20-day progressive overload strength program with a high-protein, high-calorie diet to maximize muscle mass and strength gains.'),
]

for program, name, plan_type, count, order, goal_type, desc in plans:
    print(f"  Seeding: {name} ({count} days)...")
    plan = Plan.objects.create(
        program=program, name=name, plan_type=plan_type,
        count=count, display_order=order,
        description=desc, is_active=True
    )
    for day_num in range(1, count + 1):
        day = Day.objects.create(
            plan=plan, day_number=day_num,
            title=f'Day {day_num}', is_active=True
        )
        seed_day(day, goal_type, day_num)
        if day_num % 5 == 0:
            print(f"    ...day {day_num} done")

print("\n✅ Seeding complete!")
print(f"Programs: {Program.objects.count()}")
print(f"Plans: {Plan.objects.count()}")
print(f"Days: {Day.objects.count()}")
print(f"Meals: {ProgramItem.objects.count()}")
print(f"Workouts: {WorkoutItem.objects.count()}")
print(f"Water: {WaterTarget.objects.count()}")
