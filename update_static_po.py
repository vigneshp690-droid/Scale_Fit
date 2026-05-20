import polib
import os

ta_translations = {
    "Quick Guidance": "விரைவான வழிகாட்டல்",
    "Meal Timing": "உணவு நேரம்",
    "Drink 500ml water": "500 மில்லி தண்ணீர் குடிக்கவும்"
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
print("Tamil PO file updated successfully for meal_detail.html static templates.")
