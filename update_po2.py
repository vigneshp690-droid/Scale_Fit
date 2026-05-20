import polib

translations_hi = {
    "Workouts": "वर्कआउट्स",
    "Hydration": "हाइड्रेशन",
    "Vegetarian": "शाकाहारी",
    "Non-vegetarian": "मांसाहारी",
    "Vegan": "वीगन",
    "Workout Video": "वर्कआउट वीडियो",
    "Exercise GIF": "व्यायाम GIF",
    "Exercise Image": "व्यायाम छवि",
    "Meal Image": "भोजन छवि",
    "View": "देखें",
}

translations_ta = {
    "Workouts": "பயிற்சிகள்",
    "Hydration": "நீரேற்றம்",
    "Vegetarian": "சைவம்",
    "Non-vegetarian": "அசைவம்",
    "Vegan": "வீகன்",
    "Workout Video": "பயிற்சி வீடியோ",
    "Exercise GIF": "உடற்பயிற்சி GIF",
    "Exercise Image": "உடற்பயிற்சி படம்",
    "Meal Image": "உணவு படம்",
    "View": "பார்க்க",
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

update_po("locale/hi/LC_MESSAGES/django.po", translations_hi)
update_po("locale/ta/LC_MESSAGES/django.po", translations_ta)

print("PO files updated successfully for second batch.")
