import csv
import re

with open("raw_book.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

for contact in contacts_list[1:]:
    full_name = " ".join(contact[:3])
    
    name_parts = full_name.split()
    
    name_parts = [part.title() for part in name_parts]
    
    if len(name_parts) >= 1:
        contact[0] = name_parts[0]
    if len(name_parts) >= 2:
        contact[1] = name_parts[1]
    if len(name_parts) >= 3:
        contact[2] = " ".join(name_parts[2:])
def format_phone(phone):
    if not phone or phone.strip() == '':
        return ''
    
    add_match = re.search(r'доб\.?\s*(\d+)', phone, re.IGNORECASE)
    add_number = f"доб.{add_match.group(1)}" if add_match else ""
    
    digits = re.sub(r'\D', '', phone)
    
    if len(digits) >= 10:
        main_digits = digits[-10:]
        
        formatted = f"+7({main_digits[:3]}){main_digits[3:6]}-{main_digits[6:8]}-{main_digits[8:10]}"
        
        if add_number:
            formatted += add_number
        
        return formatted
    else:
        return phone

for contact in contacts_list[1:]:
    if len(contact) > 5:
        contact[5] = format_phone(contact[5])

unique_contacts = {}
headers = contacts_list[0]

for contact in contacts_list[1:]:
    key = (contact[0].title() if contact[0] else "", 
            contact[1].title() if contact[1] else "")
    
    if key not in unique_contacts:
        unique_contacts[key] = contact.copy()
    else:
        existing = unique_contacts[key]
        for i in range(len(contact)):
            if contact[i] and not existing[i]:
                existing[i] = contact[i]

final_list = [headers] + list(unique_contacts.values())

with open("phone_book.csv", "w", encoding="utf-8", newline='') as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(final_list)

print("\n" + "=" * 60)
print("Обработка...")
print("=" * 60)
print("\nЗаголовки: ")
print(headers)
print(f"\nНайдено уникальных записей: {len(unique_contacts)}")
print("\nВывод пяти записей для проверки: ")

for i, contact in enumerate(final_list[1:6], 1):
    print(f"{i}. {contact[0]} {contact[1]} {contact[2]}: {contact[5]}")
print("\nРезультат сохранен успешно.\n > 'phone_book.csv'\n")
