import polib

translations_hi = {
    "ScaleFit logo": "स्केलफिट लोगो",
    "Select language": "भाषा चुनें",
    "Open live chat": "लाइव चैट खोलें"
}

translations_ta = {
    "ScaleFit logo": "ஸ்கேல்ஃபிட் லோகோ",
    "Select language": "மொழியைத் தேர்ந்தெடுக்கவும்",
    "Open live chat": "நேரலை அரட்டையைத் திற"
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

print("PO files updated successfully for extra strings.")
