import csv
import re

with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

headers = contacts_list[0]

for contact in contacts_list[1:]:
    full_name = " ".join(contact[:3]).strip()
    parts = full_name.split()

    contact[0] = parts[0].title() if len(parts) > 0 else ""
    contact[1] = parts[1].title() if len(parts) > 1 else ""
    contact[2] = parts[2].title() if len(parts) > 2 else ""

def format_phone(phone):
    if not phone:
        return ""

    phone = phone.strip()

    add = ""
    add_match = re.search(r'доб\.?\s*(\d+)', phone)
    if add_match:
        add = f"доб.{add_match.group(1)}"

    phone = re.sub(r'доб\.?\s*\d+', '', phone)
    digits = re.sub(r'\D', '', phone)

    if len(digits) >= 10:
        digits = digits[-10:]
        phone = f"+7({digits[:3]}){digits[3:6]}-{digits[6:8]}-{digits[8:10]}"
        return phone + add

    return phone

for contact in contacts_list[1:]:
    contact[5] = format_phone(contact[5])

unique_contacts = {}

for contact in contacts_list[1:]:
    key = (contact[0].lower(), contact[1].lower())

    if key not in unique_contacts:
        unique_contacts[key] = contact.copy()
    else:
        existing = unique_contacts[key]
        for i in range(len(contact)):
            if not existing[i] and contact[i]:
                existing[i] = contact[i]

final_list = [headers] + list(unique_contacts.values())

with open("phonebook.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(final_list)

print(f"Итоговых контактов: {len(unique_contacts)}")
