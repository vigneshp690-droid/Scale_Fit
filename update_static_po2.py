import polib
import os

ta_translations = {
    "Duration": "கால அளவு",
    "Workout Details": "பயிற்சி விவரங்கள்",
    "Weight loss friendly": "எடை குறைக்க உகந்தது",
    "Muscle gain friendly": "தசை வளர்க்க உகந்தது",
    "High protein": "அதிக புரதம்",
    "Your browser does not support video playback.": "உங்கள் உலாவி வீடியோ பிளேபேக்கை ஆதரிக்கவில்லை.",
    "Back to Day Plan": "தினசரி திட்டத்திற்குத் திரும்பு"
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
print("Tamil PO file updated successfully for workout detail strings.")
