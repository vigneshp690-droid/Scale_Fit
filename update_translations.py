import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ScaleFit.settings')
django.setup()

from fitness.models import Program, Plan, Day, ProgramItem, WorkoutItem, DayMedia

def translate_db():
    print("Translating Plans...")
    plans = Plan.objects.all()
    for plan in plans:
        if plan.name == "7 Day Fat Burn Challenge":
            plan.name_ta = "7 நாள் கொழுப்பு குறைப்பு சவால்"
            plan.name_hi = "7 दिन फैट बर्न चैलेंज"
            plan.description_ta = "உங்கள் எடை குறைப்பு பயணத்தைத் தொடங்க HIIT உடற்பயிற்சிகள் மற்றும் சுத்தமான குறைந்த கலோரி உணவுகளுடன் கூடிய 7 நாள் தீவிர கொழுப்பு எரியும் திட்டம்."
            plan.description_hi = "आपकी वजन घटाने की यात्रा को शुरू करने के लिए HIIT वर्कआउट और स्वच्छ कम कैलोरी भोजन के साथ एक 7-दिवसीय गहन वसा जलने वाला कार्यक्रम।"
        elif plan.name == "30 Day Lean Body Transformation":
            plan.name_ta = "30 நாள் உடல் மாற்றம்"
            plan.name_hi = "30 दिन लीन बॉडी ट्रांसफॉर्मेशन"
            plan.description_ta = "ஒரு மெலிந்த, உறுதியான உடலை அடைய முற்போக்கான கார்டியோ உடற்பயிற்சிகள் மற்றும் கட்டமைக்கப்பட்ட உணவுத் திட்டத்துடன் கூடிய முழுமையான 30 நாள் மாற்றுத் திட்டம்."
            plan.description_hi = "एक दुबला, टोंड शरीर प्राप्त करने के लिए प्रगतिशील कार्डियो वर्कआउट और एक संरचित भोजन योजना के साथ एक पूर्ण 30-दिवसीय परिवर्तन योजना।"
        plan.save()
        print(f"Updated Plan: {plan.name}")

    print("Translating Programs...")
    for program in Program.objects.all():
        if "Weight Loss" in program.name:
            program.name_ta = "எடை குறைப்பு திட்டம்"
            program.name_hi = "वजन घटाने का कार्यक्रम"
            program.description_ta = "கொழுப்பை குறைக்க உதவும் சிறந்த பயிற்சி திட்டம்."
            program.description_hi = "वसा कम करने में मदद करने के लिए बेहतरीन कसरत योजना।"
        elif "Weight Gain" in program.name:
            program.name_ta = "எடை அதிகரிப்பு திட்டம்"
            program.name_hi = "वजन बढ़ाने का कार्यक्रम"
            program.description_ta = "உடல் எடையை அதிகரிக்க உதவும் திட்டம்."
            program.description_hi = "वजन बढ़ाने में मदद करने वाली योजना।"
        program.save()
        print(f"Updated Program: {program.name}")

    print("Translating Meals (ProgramItem)...")
    for meal in ProgramItem.objects.all():
        if "Greek Yogurt Parfait" in meal.title:
            meal.title_ta = "கிரீக் யோகர்ட் பர்ஃபைட்"
            meal.title_hi = "ग्रीक योगर्ट पारफेट"
            meal.description_ta = "குறைந்த கொழுப்புள்ள கிரீக் யோகர்ட் மற்றும் பழங்கள் கலந்த சுவையான உணவு."
            meal.description_hi = "कम वसा वाले ग्रीक योगर्ट और फलों के साथ स्वादिष्ट भोजन।"
        meal.save()

    print("Translating Workouts (WorkoutItem)...")
    for workout in WorkoutItem.objects.all():
        if "Morning HIIT" in workout.title:
            workout.title_ta = "காலை HIIT"
            workout.title_hi = "सुबह का HIIT"
            workout.description_ta = "காலை கொழுப்பு குறைக்கும் பயிற்சி."
            workout.description_hi = "सुबह वसा जलने का वर्कआउट।"
        workout.save()
        
    print("Translating Days...")
    for day in Day.objects.all():
        if "Day 1" in day.title:
            day.title_ta = "நாள் 1"
            day.title_hi = "दिन 1"
            day.description_ta = "உங்கள் பயணத்தின் முதல் நாள்."
            day.description_hi = "आपकी यात्रा का पहला दिन।"
        day.save()

    print("Done!")

if __name__ == '__main__':
    translate_db()
