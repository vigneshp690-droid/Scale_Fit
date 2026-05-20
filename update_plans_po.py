import polib
import os

ta_translations = {
    "10 Day Muscle Kickstart": "10 நாள் தசை வளர்ப்பு திட்டம்",
    "A 10-day high-intensity strength program with calorie-dense meals to rapidly kickstart muscle growth and weight gain.": "விரைவான தசை வளர்ச்சி மற்றும் எடை அதிகரிப்பிற்கான அதிக கலோரி உணவுகளுடன் கூடிய 10 நாள் தீவிர வலிமை பயிற்சி திட்டம்.",
    "20 Day Mass Builder Program": "20 நாள் எடை அதிகரிப்பு திட்டம்",
    "A 20-day progressive overload strength program with a high-protein, high-calorie diet to maximize muscle mass and strength gains.": "அதிகபட்ச தசை மற்றும் வலிமையை பெற அதிக புரதம் மற்றும் அதிக கலோரி உணவுகளுடன் கூடிய 20 நாள் எடை அதிகரிப்பு திட்டம்."
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
print("Tamil PO file updated successfully for Weight Gain plans.")
