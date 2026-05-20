import polib
import os

hi_translations = {
    # Meals
    "Oatmeal with Berries": "ओटमील और बेरीज़",
    "Steel-cut oats topped with fresh blueberries, strawberries and a drizzle of honey. Rich in fiber to keep you full.": "ताजे ब्लूबेरी, स्ट्रॉबेरी और शहद के साथ स्टील-कट ओट्स। फाइबर से भरपूर जो आपको भरा रखता है।",
    "Greek Yogurt Parfait": "ग्रीक योगर्ट पारफे",
    "Low-fat Greek yogurt layered with granola, kiwi and mixed berries. High protein, low sugar morning fuel.": "ग्रेनोला, कीवी और मिक्स्ड बेरीज़ के साथ लो-फैट ग्रीक योगर्ट। उच्च प्रोटीन, कम चीनी।",
    "Avocado Egg Toast": "एवोकाडो एग टोस्ट",
    "Whole grain toast topped with mashed avocado, poached eggs and chili flakes. Healthy fats and protein.": "मैश किए हुए एवोकाडो, उबले अंडे और चिली फ्लेक्स के साथ होल ग्रेन टोस्ट। स्वस्थ वसा और प्रोटीन।",
    "Green Smoothie Bowl": "ग्रीन स्मूदी बाउल",
    "Blended spinach, banana and almond milk topped with chia seeds, flaxseeds and sliced fruits.": "पालक, केला और बादाम के दूध की स्मूदी, चिया सीड्स, फ्लैक्ससीड्स और कटे हुए फलों के साथ।",
    "Veggie Omelette": "वेज ऑमलेट",
    "Three-egg white omelette with bell peppers, spinach, mushrooms and low-fat cheese.": "शिमला मिर्च, पालक, मशरूम और लो-फैट चीज़ के साथ तीन अंडे की सफेदी का ऑमलेट।",
    "Chia Pudding": "चिया पुडिंग",
    "Overnight chia seeds soaked in almond milk, topped with mango chunks and coconut flakes.": "बादाम के दूध में रात भर भीगे हुए चिया सीड्स, आम के टुकड़ों और नारियल के साथ।",
    "Whole Grain Pancakes": "होल ग्रेन पैनकेक",
    "Fluffy whole wheat pancakes with fresh strawberries and a light drizzle of maple syrup.": "ताजी स्ट्रॉबेरी और मेपल सिरप के साथ फ्लफी होल व्हीट पैनकेक।",
    "Grilled Chicken Salad": "ग्रिल्ड चिकन सलाद",
    "Grilled chicken breast on a bed of mixed greens, cherry tomatoes, cucumber and lemon vinaigrette.": "मिक्स्ड ग्रीन्स, चेरी टमाटर, ककड़ी और नींबू के रस के साथ ग्रिल्ड चिकन ब्रेस्ट।",
    "Quinoa Buddha Bowl": "क्विनोआ बुद्धा बाउल",
    "Quinoa with roasted chickpeas, sweet potato, kale, avocado and tahini dressing.": "भुने हुए चने, शकरकंद, केल और एवोकाडो के साथ क्विनोआ।",
    "Turkey Lettuce Wraps": "टर्की लेट्यूस रैप्स",
    "Lean ground turkey with water chestnuts, carrots and hoisin sauce wrapped in butter lettuce.": "गाजर और सॉस के साथ लेट्यूस में लपेटा हुआ टर्की।",
    "Lentil Soup": "दाल का सूप",
    "Hearty red lentil soup with turmeric, cumin, spinach and a squeeze of lemon.": "हल्दी, जीरा, पालक और नींबू के साथ लाल दाल का सूप।",
    "Tuna Stuffed Peppers": "टूना स्टफ्ड पेपर्स",
    "Bell peppers stuffed with tuna, celery, onion and light mayo. Baked until tender.": "टूना, अजवाइन और प्याज से भरी हुई शिमला मिर्च।",
    "Zucchini Noodles": "ज़ुकिनी नूडल्स",
    "Spiralized zucchini with cherry tomatoes, basil pesto and grilled shrimp.": "चेरी टमाटर, पेस्टो और ग्रिल्ड झींगा के साथ ज़ुकिनी नूडल्स।",
    "Cauliflower Rice Bowl": "फूलगोभी राइस बाउल",
    "Cauliflower rice with black beans, corn, salsa, lime and grilled chicken strips.": "काले सेम, मकई और ग्रिल्ड चिकन के साथ फूलगोभी चावल।",
    "Baked Salmon": "बेक्ड सैल्मन",
    "Herb-crusted salmon fillet with steamed broccoli and lemon-garlic asparagus.": "ब्रोकोली और शतावरी के साथ सैल्मन फ़िले।",
    "Grilled Tilapia": "ग्रिल्ड तिलापिया",
    "Lemon-pepper tilapia with roasted Brussels sprouts and a side of brown rice.": "भुने हुए ब्रसेल्स स्प्राउट्स और ब्राउन राइस के साथ तिलापिया।",
    "Chicken Stir Fry": "चिकन स्टिर फ्राई",
    "Lean chicken breast with mixed vegetables in a light soy-ginger sauce over cauliflower rice.": "सब्जियों और फूलगोभी चावल के साथ चिकन ब्रेस्ट।",
    "Turkey Meatballs": "टर्की मीटबॉल",
    "Lean turkey meatballs in marinara sauce with zucchini noodles and fresh basil.": "ज़ुकिनी नूडल्स और तुलसी के साथ टर्की मीटबॉल।",
    "Shrimp Tacos": "श्रिम्प टैकोस",
    "Grilled shrimp in corn tortillas with cabbage slaw, avocado and lime crema.": "एवोकाडो और नींबू के साथ झींगा टैकोस।",
    "Stuffed Chicken Breast": "स्टफ्ड चिकन ब्रेस्ट",
    "Chicken breast stuffed with spinach and feta, served with roasted sweet potato.": "पालक और शकरकंद के साथ स्टफ्ड चिकन।",
    "Vegetable Curry": "वेजिटेबल करी",
    "Light coconut milk curry with chickpeas, spinach, tomatoes and brown rice.": "चने, पालक, टमाटर और ब्राउन राइस के साथ सब्जियों की करी।",
    "Apple with Almond Butter": "बादाम मक्खन के साथ सेब",
    "Sliced apple with 1 tbsp natural almond butter. Perfect balance of fiber and healthy fats.": "बादाम मक्खन के साथ सेब के टुकड़े। फाइबर और स्वस्थ वसा।",
    "Celery and Hummus": "अजवाइन और हमस",
    "Crunchy celery sticks with 2 tbsp homemade hummus. Low calorie, high fiber snack.": "हमस के साथ अजवाइन के टुकड़े।",
    "Mixed Nuts": "मिक्स्ड नट्स",
    "A small handful of almonds, walnuts and cashews. Healthy fats and protein.": "बादाम, अखरोट और काजू। स्वस्थ वसा और प्रोटीन।",
    "Cucumber Slices": "खीरे के टुकड़े",
    "Fresh cucumber slices with tzatziki dip. Hydrating and low calorie.": "डिप के साथ ताजे खीरे के टुकड़े।",
    "Protein Smoothie": "प्रोटीन स्मूदी",
    "Whey protein with almond milk, banana and spinach. Post-workout recovery drink.": "बादाम का दूध, केला और पालक के साथ प्रोटीन स्मूदी।",
    "Rice Cakes": "राइस केक",
    "Brown rice cakes with avocado and a sprinkle of sea salt. Light and satisfying.": "एवोकाडो और नमक के साथ ब्राउन राइस केक।",
    "Boiled Eggs": "उबले अंडे",
    "Two hard-boiled eggs with a pinch of salt and pepper. High protein, portable snack.": "नमक और काली मिर्च के साथ दो उबले अंडे।",

    "Protein Pancake Stack": "प्रोटीन पैनकेक स्टैक",
    "Thick protein pancakes with peanut butter, banana slices and maple syrup. 650 calories of muscle fuel.": "पीनट बटर, केले और मेपल सिरप के साथ प्रोटीन पैनकेक।",
    "Eggs and Steak": "अंडे और स्टेक",
    "Three whole eggs scrambled with a lean sirloin steak, whole grain toast and orange juice.": "स्टेक, टोस्ट और संतरे के रस के साथ तीन अंडे।",
    "Mass Gainer Smoothie": "मास गेनर स्मूदी",
    "Whole milk, oats, banana, peanut butter, whey protein and honey blended together. 800+ calories.": "दूध, ओट्स, केला, पीनट बटर, प्रोटीन और शहद की स्मूदी।",
    "Breakfast Burrito": "ब्रेकफास्ट बुरिटो",
    "Whole wheat tortilla with scrambled eggs, black beans, cheese, avocado and salsa.": "अंडे, बीन्स, चीज़ और एवोकाडो के साथ बुरिटो।",
    "Oatmeal Power Bowl": "ओटमील पावर बाउल",
    "Large bowl of oats with whole milk, whey protein, peanut butter, banana and mixed nuts.": "दूध, प्रोटीन, पीनट बटर और नट्स के साथ ओट्स।",
    "French Toast": "फ्रेंच टोस्ट",
    "Thick-cut whole grain French toast with eggs, topped with berries and Greek yogurt.": "अंडे, बेरीज़ और ग्रीक योगर्ट के साथ फ्रेंच टोस्ट।",
    "Cottage Cheese Bowl": "कॉटेज चीज़ बाउल",
    "Full-fat cottage cheese with granola, honey, walnuts and fresh pineapple chunks.": "ग्रेनोला, शहद, अखरोट और अनानास के साथ पनीर।",
    "Chicken Rice Bowl": "चिकन राइस बाउल",
    "Double portion of grilled chicken thighs over white rice with teriyaki sauce and steamed broccoli.": "चावल, सॉस और ब्रोकोली के साथ ग्रिल्ड चिकन।",
    "Beef and Pasta": "बीफ और पास्ता",
    "Lean ground beef bolognese over whole wheat pasta with parmesan and garlic bread.": "पास्ता और गार्लिक ब्रेड के साथ बीफ।",
    "Salmon Quinoa Bowl": "सैल्मन क्विनोआ बाउल",
    "Grilled salmon fillet over quinoa with roasted vegetables and avocado.": "क्विनोआ, सब्जियों और एवोकाडो के साथ सैल्मन।",
    "Turkey Sub": "टर्की सब",
    "Footlong whole grain sub with turkey, cheese, avocado, veggies and olive oil.": "टर्की, चीज़, एवोकाडो और सब्जियों के साथ सब।",
    "Tuna Pasta Salad": "टूना पास्ता सलाद",
    "Whole wheat pasta with tuna, olive oil, cherry tomatoes, olives and feta cheese.": "टूना, जैतून का तेल, टमाटर और चीज़ के साथ पास्ता।",
    "Chicken Burrito Bowl": "चिकन बुरिटो बाउल",
    "Large burrito bowl with chicken, brown rice, black beans, cheese, sour cream and guacamole.": "चिकन, ब्राउन राइस, बीन्स और चीज़ के साथ बुरिटो बाउल।",
    "Steak and Potatoes": "स्टेक और आलू",
    "Grilled sirloin steak with mashed potatoes, green beans and a side salad.": "मैश किए हुए आलू और बीन्स के साथ स्टेक।",
    "Beef Stir Fry": "बीफ स्टिर फ्राई",
    "Lean beef strips with mixed vegetables, noodles and oyster sauce. High protein evening meal.": "सब्जियों और नूडल्स के साथ बीफ।",
    "Baked Chicken Thighs": "बेक्ड चिकन जांघ",
    "Juicy baked chicken thighs with roasted sweet potatoes and garlic green beans.": "शकरकंद और बीन्स के साथ चिकन जांघ।",
    "Salmon and Rice": "सैल्मन और राइस",
    "Pan-seared salmon with jasmine rice, edamame and miso soup.": "चावल और सूप के साथ सैल्मन।",
    "Lamb Chops": "लैम्ब चॉप्स",
    "Herb-marinated lamb chops with roasted potatoes and mint yogurt sauce.": "भुने हुए आलू और सॉस के साथ लैम्ब चॉप्स।",
    "Chicken Pasta": "चिकन पास्ता",
    "Creamy chicken and mushroom pasta with whole wheat penne and parmesan.": "चिकन और मशरूम के साथ पास्ता।",
    "Pork Tenderloin": "पोर्क टेंडरलॉइन",
    "Roasted pork tenderloin with apple sauce, roasted carrots and mashed sweet potato.": "सेब की चटनी, गाजर और शकरकंद के साथ पोर्क।",
    "Beef Tacos": "बीफ टैकोस",
    "Seasoned ground beef tacos with cheese, sour cream, guacamole and pico de gallo.": "चीज़ और क्रीम के साथ बीफ टैकोस।",
    "Peanut Butter Banana": "पीनट बटर केला",
    "Two bananas with 3 tbsp peanut butter. Quick 400-calorie muscle-building snack.": "पीनट बटर के साथ दो केले।",
    "Protein Shake": "प्रोटीन शेक",
    "Double scoop whey protein with whole milk and oats. 500 calories post-workout.": "दूध और ओट्स के साथ प्रोटीन शेक।",
    "Trail Mix": "ट्रेल मिक्स",
    "Large handful of mixed nuts, dried fruits, dark chocolate chips and seeds.": "मिक्स्ड नट्स, सूखे मेवे और बीजों का मिश्रण।",
    "Cheese and Crackers": "चीज़ और क्रैकर्स",
    "Whole grain crackers with cheddar cheese and sliced turkey. Protein-rich snack.": "चीज़ और टर्की के साथ क्रैकर्स।",
    "Greek Yogurt": "ग्रीक योगर्ट",
    "Full-fat Greek yogurt with honey, granola and mixed berries. 350 calories.": "शहद, ग्रेनोला और बेरीज़ के साथ ग्रीक योगर्ट।",
    "Avocado Toast": "एवोकाडो टोस्ट",
    "Two slices whole grain toast with avocado, eggs and everything bagel seasoning.": "एवोकाडो और अंडे के साथ टोस्ट।",
    "Milk and Cookies": "दूध और कुकीज़",
    "Two whole grain oat cookies with a large glass of whole milk. 400 calories.": "दूध और ओट कुकीज़।",

    # Workouts
    "Morning HIIT Run": "सुबह की HIIT रन",
    "30 minutes of high-intensity interval running. Alternate 1 min sprint with 2 min jog. Burns 350-400 calories.": "30 मिनट की उच्च तीव्रता वाली दौड़। 350-400 कैलोरी जलाती है।",
    "Jump Rope Circuit": "जंप रोप सर्किट",
    "Jump rope intervals: 3 sets of 5 minutes with 1 minute rest. Excellent cardio and coordination.": "5 मिनट के 3 सेट, 1 मिनट के आराम के साथ। बेहतरीन कार्डियो।",
    "Cycling Session": "साइकिलिंग सेशन",
    "Moderate to high intensity cycling. Maintain 75-85% max heart rate throughout. Great fat burner.": "मध्यम से उच्च तीव्रता वाली साइकिलिंग। बेहतरीन फैट बर्नर।",
    "Bodyweight Circuit": "बॉडीवेट सर्किट",
    "Push-ups, squats, lunges, burpees and mountain climbers. 4 rounds of 15 reps each.": "पुश-अप्स, स्क्वैट्स, लंग्स। प्रत्येक 15 रेप्स के 4 राउंड।",
    "Swimming Laps": "स्विमिंग लैप्स",
    "Freestyle swimming laps with 30 second rest between sets. Full body low-impact cardio.": "30 सेकंड के आराम के साथ फ्रीस्टाइल तैराकी। फुल बॉडी कार्डियो।",
    "Yoga Flow": "योग प्रवाह",
    "Dynamic yoga flow focusing on core strength, flexibility and mindful breathing.": "मुख्य शक्ति, लचीलापन और श्वास पर केंद्रित योग।",
    "Stair Climbing": "सीढ़ी चढ़ना",
    "Stair climbing intervals for lower body strength and cardio. 10 sets of 3 floors.": "निचले शरीर की ताकत और कार्डियो के लिए सीढ़ी चढ़ना।",
    "Dance Cardio": "डांस कार्डियो",
    "High energy dance workout targeting full body fat burn. Fun and effective.": "फुल बॉडी फैट बर्न करने वाला हाई एनर्जी डांस वर्कआउट।",
    "Rowing Machine": "रोइंग मशीन",
    "Rowing intervals: 500m hard, 250m easy. Repeat 6 times. Full body cardio.": "500 मीटर तेज, 250 मीटर आसान। फुल बॉडी कार्डियो।",
    "Pilates Core": "पिलाटेस कोर",
    "Pilates-based core workout focusing on deep abdominal muscles and posture.": "गहरी पेट की मांसपेशियों और मुद्रा पर केंद्रित पिलाटेस वर्कआउट।",
    "Bench Press": "बेंच प्रेस",
    "Flat bench press: 4 sets of 8-10 reps at 75% 1RM. Primary chest and tricep builder.": "छाती और ट्राइसेप्स के लिए। 8-10 रेप्स के 4 सेट।",
    "Squat Session": "स्क्वैट सेशन",
    "Back squats: 5 sets of 5 reps heavy weight. King of all muscle-building exercises.": "भारी वजन के साथ बैक स्क्वैट्स। 5 रेप्स के 5 सेट।",
    "Deadlift Day": "डेडलिफ्ट डे",
    "Conventional deadlifts: 4 sets of 6 reps. Full posterior chain activation for mass.": "डेडलिफ्ट्स। 6 रेप्स के 4 सेट।",
    "Pull-Up and Row": "पुल-अप और रो",
    "Weighted pull-ups and barbell rows: 4 sets each. Back width and thickness builder.": "पुल-अप्स और बार्बेल रोज़। प्रत्येक के 4 सेट।",
    "Shoulder Press": "शोल्डर प्रेस",
    "Overhead press and lateral raises: 4 sets of 10. Boulder shoulder development.": "कंधों के लिए। 10 रेप्स के 4 सेट।",
    "Leg Press Day": "लेग प्रेस डे",
    "Leg press, leg curls and calf raises: 4 sets of 12. Complete lower body mass builder.": "लेग प्रेस और कर्ल्स। 12 रेप्स के 4 सेट।",
    "Bicep and Tricep": "बाइसेप और ट्राइसेप",
    "Barbell curls and skull crushers: 4 sets of 10 each. Arm size and strength.": "बांह की ताकत के लिए। प्रत्येक 10 रेप्स के 4 सेट।",
    "Power Clean": "पावर क्लीन",
    "Olympic power cleans: 5 sets of 3 reps. Explosive full body strength and power.": "फुल बॉडी स्ट्रेंथ के लिए पावर क्लीन्स। 3 रेप्स के 5 सेट।",
    "Incline Press": "इनक्लाइन प्रेस",
    "Incline dumbbell press and cable flyes: 4 sets of 10. Upper chest development.": "ऊपरी छाती के विकास के लिए इनक्लाइन प्रेस। 10 रेप्स के 4 सेट।",
    "Romanian Deadlift": "रोमानियाई डेडलिफ्ट",
    "RDL and glute bridges: 4 sets of 10. Hamstring and glute mass builder.": "हैमस्ट्रिंग और ग्लूट के लिए। 10 रेप्स के 4 सेट।",

    # Durations
    "30 minutes": "30 मिनट",
    "35 minutes": "35 मिनट",
    "40 minutes": "40 मिनट",
    "45 minutes": "45 मिनट",
    "50 minutes": "50 मिनट",
    "55 minutes": "55 मिनट",

    # Water targets
    "2.5 Liters": "2.5 लीटर",
    "3.5 Liters": "3.5 लीटर",

    # Vitamins and Minerals
    "Vitamin A, Vitamin C": "विटामिन ए, विटामिन सी",
    "Iron, Calcium": "आयरन, कैल्शियम",

    # Statics
    "Quick Guidance": "त्वरित मार्गदर्शन",
    "Meal Timing": "भोजन का समय",
    "Drink 500ml water": "500 मिलीलीटर पानी पिएं",
    "Weight loss friendly": "वजन घटाने के अनुकूल",
    "Muscle gain friendly": "मांसपेशियों के निर्माण के अनुकूल",
    "High protein": "उच्च प्रोटीन",
    "Duration": "अवधि",
    "Workout Details": "वर्कआउट विवरण",
    "Your browser does not support video playback.": "आपका ब्राउज़र वीडियो प्लेबैक का समर्थन नहीं करता है।",
    "Back to Day Plan": "दिन की योजना पर वापस जाएं",
    "Day": "दिन",
    "Videos, exercise demos, meals, and nutrition for today's plan.": "आज की योजना के लिए वीडियो, व्यायाम डेमो, भोजन और पोषण।",

    # Plans
    "10 Day Muscle Kickstart": "10 दिन का मसल किकस्टार्ट",
    "A 10-day high-intensity strength program with calorie-dense meals to rapidly kickstart muscle growth and weight gain.": "तेजी से मांसपेशियों की वृद्धि और वजन बढ़ाने के लिए कैलोरी-सघन भोजन के साथ 10-दिवसीय उच्च-तीव्रता वाला शक्ति कार्यक्रम।",
    "20 Day Mass Builder Program": "20 दिन का मास बिल्डर प्रोग्राम",
    "A 20-day progressive overload strength program with a high-protein, high-calorie diet to maximize muscle mass and strength gains.": "मांसपेशियों के द्रव्यमान और शक्ति लाभ को अधिकतम करने के लिए उच्च प्रोटीन, उच्च कैलोरी आहार के साथ 20 दिन का कार्यक्रम।"
}

# Generate water notes dynamically for Day 1 to 30
for day_num in range(1, 31):
    wl_note_en = f'Day {day_num}: Drink water before each meal. Stay hydrated to boost metabolism and reduce hunger.'
    wl_note_hi = f'दिन {day_num}: प्रत्येक भोजन से पहले पानी पिएं। चयापचय को बढ़ावा देने और भूख कम करने के लिए हाइड्रेटेड रहें।'
    hi_translations[wl_note_en] = wl_note_hi
    
    wg_note_en = f'Day {day_num}: Hydration is key for muscle recovery. Drink extra water post-workout.'
    wg_note_hi = f'दिन {day_num}: मांसपेशियों की रिकवरी के लिए हाइड्रेशन महत्वपूर्ण है। वर्कआउट के बाद अतिरिक्त पानी पिएं।'
    hi_translations[wg_note_en] = wg_note_hi

def update_po(filepath, new_translations):
    if not os.path.exists(filepath):
        print(f"Error: {filepath} not found.")
        return
    po = polib.pofile(filepath)
    for msgid, msgstr in new_translations.items():
        entry = po.find(msgid)
        if entry:
            entry.msgstr = msgstr
        else:
            entry = polib.POEntry(msgid=msgid, msgstr=msgstr)
            po.append(entry)
    po.save()

update_po("locale/hi/LC_MESSAGES/django.po", hi_translations)
print("Hindi PO file updated successfully for all strings.")
