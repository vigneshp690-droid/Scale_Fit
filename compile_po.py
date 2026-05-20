import polib
import os

for lang in ['hi', 'ta', 'en']:
    po_path = f"locale/{lang}/LC_MESSAGES/django.po"
    mo_path = f"locale/{lang}/LC_MESSAGES/django.mo"
    if os.path.exists(po_path):
        po = polib.pofile(po_path)
        po.save_as_mofile(mo_path)
        print(f"Compiled {mo_path}")
