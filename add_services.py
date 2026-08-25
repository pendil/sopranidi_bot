import sqlite3
import os
from pathlib import Path
from datetime import datetime

print("🔍 Ищем базу данных...")

# Возможные пути
paths = [
    "data/shop_bot.db",
    "/persistent/shop_bot.db",
    str(Path(__file__).resolve().parent / "data" / "shop_bot.db"),
]

DB_NAME = None
for p in paths:
    if os.path.exists(p):
        DB_NAME = p
        print(f"✅ Найдена БД: {p}")
        break

if not DB_NAME:
    print("❌ База данных не найдена!")
    print("   Проверьте пути:")
    for p in paths:
        print(f"   - {p}")
    exit()

conn = sqlite3.connect(DB_NAME)
cur = conn.cursor()

print("\n📊 Текущие услуги в БД:")
cur.execute("SELECT id, name, price FROM services")
rows = cur.fetchall()
for row in rows:
    print(f"   {row[0]}. {row[1]} - {row[2]} ₽")

print("\n🔄 Добавляем новые услуги...")

new_services = [
    ("Реферат", "Написание качественного реферата по любой теме", 1200),
    ("Редактирование работы", "Правка и доработка готовой работы", 800),
    ("Тотальная защита (PREMIER)", "Полное сопровождение проекта: консультация, создание работы, объяснение материала, тренаж защиты и финальные правки. Гарантия оценки!", 3500),
]

added = 0
for name, desc, price in new_services:
    cur.execute("SELECT id FROM services WHERE name = ?", (name,))
    if cur.fetchone():
        print(f"   ⏩ Услуга уже существует: {name}")
    else:
        cur.execute(
            "INSERT INTO services (name, description, price, created_at) VALUES (?, ?, ?, ?)",
            (name, desc, price, datetime.now().isoformat())
        )
        print(f"   ✅ Добавлена: {name} ({price}₽)")
        added += 1

conn.commit()

print("\n📊 Проверка: услуги после добавления")
cur.execute("SELECT id, name, price FROM services")
for row in cur.fetchall():
    print(f"   {row[0]}. {row[1]} - {row[2]} ₽")

conn.close()

if added > 0:
    print(f"\n✅ Добавлено {added} новых услуг!")
    print("🔄 Перезапустите бота, чтобы изменения вступили в силу.")
else:
    print("\nℹ️ Новых услуг не добавлено (все уже есть).")
    print("   Если услуги не отображаются — проверьте код бота.")