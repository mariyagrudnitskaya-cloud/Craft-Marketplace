import csv
import json

# путь к твоему CSV (можешь поменять при необходимости)
input_csv = "partner_A.csv"
output_json = "app/palettes/partner_A.json"

palette = []
seen_partner_codes = set()
duplicate_partner_codes = set()

with open(input_csv, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        try:
            partner_code = str(row["partner_code"]).strip()

            # проверяем на дубли
            if partner_code in seen_partner_codes:
                duplicate_partner_codes.add(partner_code)
            else:
                seen_partner_codes.add(partner_code)

            color_item = {
                "my_code": int(row["my_code"]),
                "partner_code": partner_code,
                "hex": row["Hex"].strip(),
                "rgb": [
                    int(row["R"]),
                    int(row["G"]),
                    int(row["B"])
                ],
                "shape": row["shape"].strip(),
                "stone_size_mm": float(str(row["stone_size_mm"]).replace(",", "."))
            }
            palette.append(color_item)

        except Exception as e:
            print(f"❌ Ошибка в строке {row}: {e}")

# сохраняем JSON
with open(output_json, "w", encoding="utf-8") as jsonfile:
    json.dump(palette, jsonfile, ensure_ascii=False, indent=2)

print(f"✅ Палитра сохранена в {output_json}. Всего записей: {len(palette)}")

# отчёт по дублям
if duplicate_partner_codes:
    print("⚠ Обнаружены дублирующиеся partner_code:")
    for code in sorted(duplicate_partner_codes):
        print(f"   - {code}")
else:
    print("✅ Дубликатов partner_code не найдено.")
