import sqlite3
import os
from pathlib import Path

# Находим БД
DATA_DIR = "/persistent" if os.path.exists("/persistent") else str(Path(__file__).resolve().parent / "data")
DB_NAME = f"{DATA_DIR}/shop_bot.db"


def add_services():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # Проверяем, есть ли уже такие услуги
    cur.execute("SELECT name FROM services")
    existing = [row[0] for row in cur.fetchall()]

    new_services = [
        ("Реферат", "Написание качественного реферата по любой теме", 1200),
        ("Редактирование работы", "Правка и доработка готовой работы", 800),
        ("Тотальная защита (PREMIER)",
         "Полное сопровождение проекта: консультация, создание работы, объяснение материала, тренаж защиты и финальные правки. Гарантия оценки!",
         3500),
    ]

    added = 0
    for name, desc, price in new_services:
        if name not in existing:
            cur.execute(
                "INSERT INTO services (name, description, price, created_at) VALUES (?, ?, ?, ?)",
                (name, desc, price, datetime.now().isoformat())
            )
            print(f"✅ Добавлена услуга: {name} ({price}₽)")
            added += 1
        else:
            print(f"⏩ Услуга уже существует: {name}")

    conn.commit()
    conn.close()

    if added == 0:
        print("ℹ️ Все услуги уже добавлены.")
    else:
        print(f"✅ Добавлено {added} новых услуг. Перезапустите бота!")


if __name__ == "__main__":
    from datetime import datetime

    add_services()