import polib
import os

ta_translations = {
    # Breakfast
    "Oatmeal with Berries": "ஓட்ஸ் மற்றும் பெர்ரிகள்",
    "Steel-cut oats topped with fresh blueberries, strawberries and a drizzle of honey. Rich in fiber to keep you full.": "புதிய புளுபெர்ரிகள், ஸ்ட்ராபெர்ரிகள் மற்றும் தேன் கலந்த ஓட்ஸ். அதிக நார்ச்சத்துள்ள உணவு.",
    "Greek Yogurt Parfait": "கிரீக் தயிர் பார்பைட்",
    "Low-fat Greek yogurt layered with granola, kiwi and mixed berries. High protein, low sugar morning fuel.": "க்ரனோலா, கிவி மற்றும் பழங்களுடன் கூடிய குறைந்த கொழுப்புள்ள கிரீக் தயிர். அதிக புரதம் கொண்டது.",
    "Avocado Egg Toast": "அவகேடோ முட்டை டோஸ்ட்",
    "Whole grain toast topped with mashed avocado, poached eggs and chili flakes. Healthy fats and protein.": "அவகேடோ, வேகவைத்த முட்டை மற்றும் மிளகாய் கலந்த முழு தானிய டோஸ்ட். ஆரோக்கியமான கொழுப்புகள் மற்றும் புரதம்.",
    "Green Smoothie Bowl": "கிரீன் ஸ்மூத்தி பவுல்",
    "Blended spinach, banana and almond milk topped with chia seeds, flaxseeds and sliced fruits.": "கீரை, வாழைப்பழம் மற்றும் பாதாம் பால் கலந்த ஸ்மூத்தி, பழங்களுடன்.",
    "Veggie Omelette": "காய்கறி ஆம்லெட்",
    "Three-egg white omelette with bell peppers, spinach, mushrooms and low-fat cheese.": "குடைமிளகாய், கீரை மற்றும் காளான்களுடன் கூடிய முட்டை வெள்ளை ஆம்லெட்.",
    "Chia Pudding": "சியா புட்டு",
    "Overnight chia seeds soaked in almond milk, topped with mango chunks and coconut flakes.": "பாதாம் பாலில் ஊறவைத்த சியா விதைகள், மாம்பழ துண்டுகளுடன்.",
    "Whole Grain Pancakes": "முழு தானிய பான்கேக்",
    "Fluffy whole wheat pancakes with fresh strawberries and a light drizzle of maple syrup.": "புதிய ஸ்ட்ராபெர்ரிகளுடன் கூடிய முழு கோதுமை பான்கேக்குகள்.",
    
    # Lunch
    "Grilled Chicken Salad": "கிரில் சிக்கன் சாலட்",
    "Grilled chicken breast on a bed of mixed greens, cherry tomatoes, cucumber and lemon vinaigrette.": "பச்சை காய்கறிகள், தக்காளி மற்றும் எலுமிச்சை சாறுடன் கிரில் செய்யப்பட்ட சிக்கன்.",
    "Quinoa Buddha Bowl": "கினோவா புத்தா பவுல்",
    "Quinoa with roasted chickpeas, sweet potato, kale, avocado and tahini dressing.": "கொண்டைக்கடலை, இனிப்பு உருளைக்கிழங்கு மற்றும் அவகேடோவுடன் கினோவா.",
    "Turkey Lettuce Wraps": "டர்கி லெட்டூஸ் ரேப்ஸ்",
    "Lean ground turkey with water chestnuts, carrots and hoisin sauce wrapped in butter lettuce.": "கேரட் மற்றும் சாஸுடன் கூடிய லெட்டூஸில் சுற்றப்பட்ட டர்கி இறைச்சி.",
    "Lentil Soup": "பருப்பு சூப்",
    "Hearty red lentil soup with turmeric, cumin, spinach and a squeeze of lemon.": "மஞ்சள், சீரகம் மற்றும் கீரையுடன் கூடிய சிவப்பு பருப்பு சூப்.",
    "Tuna Stuffed Peppers": "டுனா ஸ்டஃப்டு பெப்பர்ஸ்",
    "Bell peppers stuffed with tuna, celery, onion and light mayo. Baked until tender.": "டுனா மற்றும் வெங்காயம் நிரப்பப்பட்ட குடைமிளகாய்.",
    "Zucchini Noodles": "சுரைக்காய் நூடுல்ஸ்",
    "Spiralized zucchini with cherry tomatoes, basil pesto and grilled shrimp.": "தக்காளி மற்றும் இறாலுடன் கூடிய சுரைக்காய் நூடுல்ஸ்.",
    "Cauliflower Rice Bowl": "காலிஃபிளவர் ரைஸ் பவுல்",
    "Cauliflower rice with black beans, corn, salsa, lime and grilled chicken strips.": "கருப்பு பீன்ஸ் மற்றும் சிக்கனுடன் காலிஃபிளவர் ரைஸ்.",
    
    # Dinner
    "Baked Salmon": "பேக்ட் சால்மன்",
    "Herb-crusted salmon fillet with steamed broccoli and lemon-garlic asparagus.": "ப்ரோக்கோலி மற்றும் அஸ்பாரகஸுடன் கூடிய சால்மன் மீன்.",
    "Grilled Tilapia": "கிரில் திலாபியா",
    "Lemon-pepper tilapia with roasted Brussels sprouts and a side of brown rice.": "எலுமிச்சை மிளகு திலாபியா மீன் மற்றும் பிரவுன் ரைஸ்.",
    "Chicken Stir Fry": "சிக்கன் ஸ்டிர் ஃப்ரை",
    "Lean chicken breast with mixed vegetables in a light soy-ginger sauce over cauliflower rice.": "காலிஃபிளவர் ரைஸுடன் காய்கறிகள் மற்றும் சிக்கன்.",
    "Turkey Meatballs": "டர்கி மீட்பால்ஸ்",
    "Lean turkey meatballs in marinara sauce with zucchini noodles and fresh basil.": "சுரைக்காய் நூடுல்ஸுடன் டர்கி மீட்பால்ஸ்.",
    "Shrimp Tacos": "இறால் டாக்கோஸ்",
    "Grilled shrimp in corn tortillas with cabbage slaw, avocado and lime crema.": "அவகேடோ மற்றும் முட்டைக்கோஸுடன் கூடிய இறால் டாக்கோஸ்.",
    "Stuffed Chicken Breast": "ஸ்டஃப்டு சிக்கன் பிரெஸ்ட்",
    "Chicken breast stuffed with spinach and feta, served with roasted sweet potato.": "கீரை நிரப்பப்பட்ட சிக்கன் மற்றும் இனிப்பு உருளைக்கிழங்கு.",
    "Vegetable Curry": "காய்கறி கறி",
    "Light coconut milk curry with chickpeas, spinach, tomatoes and brown rice.": "பீன்ஸ், தக்காளி மற்றும் பிரவுன் ரைஸுடன் கூடிய காய்கறி கறி.",

    # Snacks
    "Apple with Almond Butter": "ஆப்பிள் மற்றும் பாதாம் வெண்ணெய்",
    "Sliced apple with 1 tbsp natural almond butter. Perfect balance of fiber and healthy fats.": "பாதாம் வெண்ணெயுடன் கூடிய ஆப்பிள் துண்டுகள்.",
    "Celery and Hummus": "செலரி மற்றும் ஹம்முஸ்",
    "Crunchy celery sticks with 2 tbsp homemade hummus. Low calorie, high fiber snack.": "ஹம்முஸுடன் கூடிய செலரி குச்சிகள்.",
    "Mixed Nuts": "கலவையான கொட்டைகள்",
    "A small handful of almonds, walnuts and cashews. Healthy fats and protein.": "பாதாம், அக்ரூட் மற்றும் முந்திரி பருப்புகள்.",
    "Cucumber Slices": "வெள்ளரி துண்டுகள்",
    "Fresh cucumber slices with tzatziki dip. Hydrating and low calorie.": "டிப்ஸுடன் கூடிய புதிய வெள்ளரி துண்டுகள்.",
    "Protein Smoothie": "புரோட்டீன் ஸ்மூத்தி",
    "Whey protein with almond milk, banana and spinach. Post-workout recovery drink.": "வாழைப்பழம் மற்றும் பாதாம் பால் கலந்த புரோட்டீன் ஸ்மூத்தி.",
    "Rice Cakes": "ரைஸ் கேக்",
    "Brown rice cakes with avocado and a sprinkle of sea salt. Light and satisfying.": "அவகேடோவுடன் கூடிய பிரவுன் ரைஸ் கேக்.",
    "Boiled Eggs": "வேகவைத்த முட்டை",
    "Two hard-boiled eggs with a pinch of salt and pepper. High protein, portable snack.": "உப்பு மற்றும் மிளகு தூவிய இரண்டு வேகவைத்த முட்டைகள்.",
    
    # Weight Gain specific meals
    "Protein Pancake Stack": "புரோட்டீன் பான்கேக் ஸ்டாக்",
    "Thick protein pancakes with peanut butter, banana slices and maple syrup. 650 calories of muscle fuel.": "வேர்க்கடலை வெண்ணெய் மற்றும் வாழைப்பழத்துடன் கூடிய புரோட்டீன் பான்கேக்.",
    "Eggs and Steak": "முட்டை மற்றும் ஸ்டீக்",
    "Three whole eggs scrambled with a lean sirloin steak, whole grain toast and orange juice.": "ஸ்டீக் மற்றும் முழு தானிய டோஸ்டுடன் கூடிய முட்டை.",
    "Mass Gainer Smoothie": "மாஸ் கெயினர் ஸ்மூத்தி",
    "Whole milk, oats, banana, peanut butter, whey protein and honey blended together. 800+ calories.": "பழங்கள், பால் மற்றும் புரோட்டீன் கலந்த மாஸ் கெயினர் ஸ்மூத்தி.",
    "Breakfast Burrito": "பிரேக்ஃபாஸ்ட் புர்ரிட்டோ",
    "Whole wheat tortilla with scrambled eggs, black beans, cheese, avocado and salsa.": "முட்டை மற்றும் சீஸ் கொண்ட முழு கோதுமை புர்ரிட்டோ.",
    "Oatmeal Power Bowl": "ஓட்ஸ் பவர் பவுல்",
    "Large bowl of oats with whole milk, whey protein, peanut butter, banana and mixed nuts.": "பால், வாழைப்பழம் மற்றும் கொட்டைகள் கலந்த ஓட்ஸ் பவுல்.",
    "French Toast": "பிரெஞ்சு டோஸ்ட்",
    "Thick-cut whole grain French toast with eggs, topped with berries and Greek yogurt.": "முட்டை மற்றும் பழங்களுடன் கூடிய முழு தானிய பிரெஞ்சு டோஸ்ட்.",
    "Cottage Cheese Bowl": "காட்டேஜ் சீஸ் பவுல்",
    "Full-fat cottage cheese with granola, honey, walnuts and fresh pineapple chunks.": "தேன் மற்றும் அன்னாசிப்பழத்துடன் கூடிய சீஸ் பவுல்.",
    "Chicken Rice Bowl": "சிக்கன் ரைஸ் பவுல்",
    "Double portion of grilled chicken thighs over white rice with teriyaki sauce and steamed broccoli.": "ப்ரோக்கோலி மற்றும் சாஸுடன் கூடிய சிக்கன் மற்றும் ரைஸ்.",
    "Beef and Pasta": "பீஃப் மற்றும் பாஸ்தா",
    "Lean ground beef bolognese over whole wheat pasta with parmesan and garlic bread.": "முழு கோதுமை பாஸ்தாவுடன் கூடிய மாட்டிறைச்சி.",
    "Salmon Quinoa Bowl": "சால்மன் கினோவா பவுல்",
    "Grilled salmon fillet over quinoa with roasted vegetables and avocado.": "கினோவா மற்றும் காய்கறிகளுடன் கூடிய சால்மன் மீன்.",
    "Turkey Sub": "டர்கி சப்",
    "Footlong whole grain sub with turkey, cheese, avocado, veggies and olive oil.": "டர்கி மற்றும் சீஸ் கொண்ட முழு தானிய சப்.",
    "Tuna Pasta Salad": "டுனா பாஸ்தா சாலட்",
    "Whole wheat pasta with tuna, olive oil, cherry tomatoes, olives and feta cheese.": "டுனா மற்றும் தக்காளி கொண்ட முழு கோதுமை பாஸ்தா.",
    "Chicken Burrito Bowl": "சிக்கன் புர்ரிட்டோ பவுல்",
    "Large burrito bowl with chicken, brown rice, black beans, cheese, sour cream and guacamole.": "சிக்கன், பிரவுன் ரைஸ் மற்றும் சீஸ் கொண்ட புர்ரிட்டோ பவுல்.",
    "Steak and Potatoes": "ஸ்டீக் மற்றும் உருளைக்கிழங்கு",
    "Grilled sirloin steak with mashed potatoes, green beans and a side salad.": "மசித்த உருளைக்கிழங்குடன் கூடிய ஸ்டீக்.",
    "Beef Stir Fry": "பீஃப் ஸ்டிர் ஃப்ரை",
    "Lean beef strips with mixed vegetables, noodles and oyster sauce. High protein evening meal.": "நூடுல்ஸ் மற்றும் காய்கறிகளுடன் கூடிய மாட்டிறைச்சி.",
    "Baked Chicken Thighs": "பேக்ட் சிக்கன் தொடைகள்",
    "Juicy baked chicken thighs with roasted sweet potatoes and garlic green beans.": "இனிப்பு உருளைக்கிழங்குடன் கூடிய சிக்கன் தொடைகள்.",
    "Salmon and Rice": "சால்மன் மற்றும் ரைஸ்",
    "Pan-seared salmon with jasmine rice, edamame and miso soup.": "ரைஸ் மற்றும் சூப்புடன் கூடிய சால்மன் மீன்.",
    "Lamb Chops": "ஆட்டுக்கறி சாப்ஸ்",
    "Herb-marinated lamb chops with roasted potatoes and mint yogurt sauce.": "உருளைக்கிழங்குடன் கூடிய ஆட்டுக்கறி சாப்ஸ்.",
    "Chicken Pasta": "சிக்கன் பாஸ்தா",
    "Creamy chicken and mushroom pasta with whole wheat penne and parmesan.": "சிக்கன் மற்றும் காளான் கொண்ட பாஸ்தா.",
    "Pork Tenderloin": "பன்றி இறைச்சி டெண்டர்லோயின்",
    "Roasted pork tenderloin with apple sauce, roasted carrots and mashed sweet potato.": "இனிப்பு உருளைக்கிழங்குடன் கூடிய பன்றி இறைச்சி.",
    "Beef Tacos": "பீஃப் டாக்கோஸ்",
    "Seasoned ground beef tacos with cheese, sour cream, guacamole and pico de gallo.": "சீஸ் மற்றும் காய்கறிகளுடன் கூடிய மாட்டிறைச்சி டாக்கோஸ்.",
    "Peanut Butter Banana": "வேர்க்கடலை வெண்ணெய் வாழைப்பழம்",
    "Two bananas with 3 tbsp peanut butter. Quick 400-calorie muscle-building snack.": "வேர்க்கடலை வெண்ணெயுடன் கூடிய வாழைப்பழங்கள்.",
    "Protein Shake": "புரோட்டீன் ஷேக்",
    "Double scoop whey protein with whole milk and oats. 500 calories post-workout.": "பால் மற்றும் ஓட்ஸ் கலந்த புரோட்டீன் ஷேக்.",
    "Trail Mix": "ட்ரெயில் மிக்ஸ்",
    "Large handful of mixed nuts, dried fruits, dark chocolate chips and seeds.": "கொட்டைகள் மற்றும் உலர்ந்த பழங்களின் கலவை.",
    "Cheese and Crackers": "சீஸ் மற்றும் கிராக்கர்ஸ்",
    "Whole grain crackers with cheddar cheese and sliced turkey. Protein-rich snack.": "சீஸ் மற்றும் டர்கியுடன் கூடிய முழு தானிய கிராக்கர்ஸ்.",
    "Greek Yogurt": "கிரீக் தயிர்",
    "Full-fat Greek yogurt with honey, granola and mixed berries. 350 calories.": "தேன் மற்றும் பழங்களுடன் கூடிய கிரீக் தயிர்.",
    "Avocado Toast": "அவகேடோ டோஸ்ட்",
    "Two slices whole grain toast with avocado, eggs and everything bagel seasoning.": "அவகேடோ மற்றும் முட்டையுடன் கூடிய முழு தானிய டோஸ்ட்.",
    "Milk and Cookies": "பால் மற்றும் குக்கீகள்",
    "Two whole grain oat cookies with a large glass of whole milk. 400 calories.": "முழு பால் மற்றும் ஓட்ஸ் குக்கீகள்.",
    
    # Nutrition / Ingredients
    "Vitamin A, Vitamin C": "வைட்டமின் ஏ, வைட்டமின் சி",
    "Iron, Calcium": "இரும்புச்சத்து, கால்சியம்"
}

def update_po(filepath, new_translations):
    po = polib.pofile(filepath)
    for msgid, msgstr in new_translations.items():
        entry = po.find(msgid)
        if entry:
            entry.msgstr = msgstr
        else:
            entry = polib.POEntry(msgid=msgid, msgstr=msgstr)
            po.append(entry)
    po.save()

update_po("locale/ta/LC_MESSAGES/django.po", ta_translations)
print("Tamil PO file updated successfully for meal seeded data.")
