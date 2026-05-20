import polib
import os

ta_translations = {
    # Workouts
    "Morning HIIT Run": "காலை HIIT ஓட்டம்",
    "30 minutes of high-intensity interval running. Alternate 1 min sprint with 2 min jog. Burns 350-400 calories.": "30 நிமிட தீவிர ஓட்டப்பயிற்சி. 1 நிமிடம் வேகமாக, 2 நிமிடம் மெதுவாக ஓடவும். 350-400 கலோரியை எரிக்கும்.",
    "Jump Rope Circuit": "ஜம்ப் ரோப் பயிற்சி",
    "Jump rope intervals: 3 sets of 5 minutes with 1 minute rest. Excellent cardio and coordination.": "3 செட் 5 நிமிட பயிற்சி, 1 நிமிட இடைவெளியுடன். சிறந்த கார்டியோ பயிற்சி.",
    "Cycling Session": "சைக்கிள் ஓட்டும் பயிற்சி",
    "Moderate to high intensity cycling. Maintain 75-85% max heart rate throughout. Great fat burner.": "நடுத்தர முதல் தீவிர சைக்கிள் பயிற்சி. அதிக கொழுப்பை எரிக்கும்.",
    "Bodyweight Circuit": "உடல் எடை பயிற்சி",
    "Push-ups, squats, lunges, burpees and mountain climbers. 4 rounds of 15 reps each.": "புஷ்-அப்ஸ், ஸ்குவாட்ஸ், லஞ்சஸ். தலா 15 முறை, 4 ரவுண்டுகள்.",
    "Swimming Laps": "நீச்சல் பயிற்சி",
    "Freestyle swimming laps with 30 second rest between sets. Full body low-impact cardio.": "30 வினாடி இடைவெளியுடன் ஃப்ரீஸ்டைல் நீச்சல். முழு உடல் கார்டியோ.",
    "Yoga Flow": "யோகா பயிற்சி",
    "Dynamic yoga flow focusing on core strength, flexibility and mindful breathing.": "உடல் வலிமை, நெகிழ்வுத்தன்மை மற்றும் மூச்சுப் பயிற்சிக்கு முக்கியத்துவம் அளிக்கும் யோகா.",
    "Stair Climbing": "மாடிப்படி ஏறும் பயிற்சி",
    "Stair climbing intervals for lower body strength and cardio. 10 sets of 3 floors.": "கீழ் உடல் வலிமை மற்றும் கார்டியோவுக்கான பயிற்சி. தலா 3 மாடிகள், 10 செட்.",
    "Dance Cardio": "நடன கார்டியோ பயிற்சி",
    "High energy dance workout targeting full body fat burn. Fun and effective.": "முழு உடல் கொழுப்பை எரிக்க உதவும் அதிக ஆற்றல் நடன பயிற்சி.",
    "Rowing Machine": "துடுப்பு இயந்திரப் பயிற்சி",
    "Rowing intervals: 500m hard, 250m easy. Repeat 6 times. Full body cardio.": "500 மீ வேகமாக, 250 மீ மெதுவாக. 6 முறை செய்யவும். முழு உடல் கார்டியோ.",
    "Pilates Core": "பைலேட்ஸ் கோர் பயிற்சி",
    "Pilates-based core workout focusing on deep abdominal muscles and posture.": "ஆழமான வயிற்று தசைகள் மற்றும் உடல் தோரணையை மையமாகக் கொண்ட பயிற்சி.",
    "Bench Press": "பெஞ்ச் பிரஸ்",
    "Flat bench press: 4 sets of 8-10 reps at 75% 1RM. Primary chest and tricep builder.": "மார்பு மற்றும் ட்ரைசெப் தசைக்கான பயிற்சி. தலா 8-10 முறை, 4 செட்.",
    "Squat Session": "ஸ்குவாட் பயிற்சி",
    "Back squats: 5 sets of 5 reps heavy weight. King of all muscle-building exercises.": "அதிக எடையுடன் பேக் ஸ்குவாட்ஸ். தசை வளர்க்கும் பயிற்சிகளின் அரசன்.",
    "Deadlift Day": "டெட்லிஃப்ட் பயிற்சி",
    "Conventional deadlifts: 4 sets of 6 reps. Full posterior chain activation for mass.": "தசை வளர்ச்சிக்கான டெட்லிஃப்ட் பயிற்சி. தலா 6 முறை, 4 செட்.",
    "Pull-Up and Row": "புல்-அப் மற்றும் ரோ",
    "Weighted pull-ups and barbell rows: 4 sets each. Back width and thickness builder.": "முதுகு தசையை விரிவுபடுத்தும் பயிற்சி. தலா 4 செட்.",
    "Shoulder Press": "தோள்பட்டை பயிற்சி",
    "Overhead press and lateral raises: 4 sets of 10. Boulder shoulder development.": "தோள்பட்டை தசைக்கான பயிற்சி. தலா 10 முறை, 4 செட்.",
    "Leg Press Day": "லெக் பிரஸ் பயிற்சி",
    "Leg press, leg curls and calf raises: 4 sets of 12. Complete lower body mass builder.": "கீழ் உடல் தசைக்கான பயிற்சி. தலா 12 முறை, 4 செட்.",
    "Bicep and Tricep": "பைசெப் மற்றும் ட்ரைசெப்",
    "Barbell curls and skull crushers: 4 sets of 10 each. Arm size and strength.": "கைகளின் அளவு மற்றும் வலிமைக்கான பயிற்சி. தலா 10 முறை, 4 செட்.",
    "Power Clean": "பவர் கிளீன்",
    "Olympic power cleans: 5 sets of 3 reps. Explosive full body strength and power.": "முழு உடல் வலிமை மற்றும் ஆற்றலுக்கான பயிற்சி. தலா 3 முறை, 5 செட்.",
    "Incline Press": "இன்க்லைன் பிரஸ்",
    "Incline dumbbell press and cable flyes: 4 sets of 10. Upper chest development.": "மேல் மார்பு தசைக்கான பயிற்சி. தலா 10 முறை, 4 செட்.",
    "Romanian Deadlift": "ரொமேனியன் டெட்லிஃப்ட்",
    "RDL and glute bridges: 4 sets of 10. Hamstring and glute mass builder.": "தொடை மற்றும் இடுப்பு தசைக்கான பயிற்சி. தலா 10 முறை, 4 செட்.",

    # Durations
    "30 minutes": "30 நிமிடங்கள்",
    "35 minutes": "35 நிமிடங்கள்",
    "40 minutes": "40 நிமிடங்கள்",
    "45 minutes": "45 நிமிடங்கள்",
    "50 minutes": "50 நிமிடங்கள்",
    "55 minutes": "55 நிமிடங்கள்",

    # Water targets
    "2.5 Liters": "2.5 லிட்டர்",
    "3.5 Liters": "3.5 லிட்டர்",
}

# Generate water notes dynamically for Day 1 to 30
for day_num in range(1, 31):
    wl_note_en = f'Day {day_num}: Drink water before each meal. Stay hydrated to boost metabolism and reduce hunger.'
    wl_note_ta = f'நாள் {day_num}: ஒவ்வொரு உணவிற்கும் முன் தண்ணீர் குடிக்கவும். நீர்ச்சத்துடன் இருப்பது உடல் எடையை குறைக்க உதவும்.'
    ta_translations[wl_note_en] = wl_note_ta
    
    wg_note_en = f'Day {day_num}: Hydration is key for muscle recovery. Drink extra water post-workout.'
    wg_note_ta = f'நாள் {day_num}: தசை மீட்புக்கு நீர்ச்சத்து அவசியம். பயிற்சிக்குப் பிறகு கூடுதல் தண்ணீர் குடிக்கவும்.'
    ta_translations[wg_note_en] = wg_note_ta

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
print("Tamil PO file updated successfully for workouts and water.")
