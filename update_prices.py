import sqlite3
import os
from pathlib import Path


def find_db():
    """Ищет базу данных в разных местах"""
    possible_paths = [
        "data/shop_bot.db",  # локально
        "/persistent/shop_bot.db",  # на BotHost
        "shop_bot.db",  # в корне
        "data/shop_bot.db",  # снова
        str(Path(__file__).parent / "data" / "shop_bot.db"),  # через Path
    ]

    for path in possible_paths:
        if os.path.exists(path):
            return path
    return None


def update_prices():
    db_path = find_db()

    if not db_path:
        print("❌ База данных не найдена!")
        print("   Искал в:")
        print("   - data/shop_bot.db")
        print("   - /persistent/shop_bot.db")
        print("   - shop_bot.db")
        print("\n   Сначала запустите бота хотя бы раз, чтобы создать БД.")
        return

    print(f"✅ Найдена БД: {db_path}")

    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()

        # Проверяем, есть ли таблица services
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='services'")
        if not cur.fetchone():
            print("❌ Таблица services не существует!")
            print("   Запустите бота, чтобы создать таблицу.")
            conn.close()
            return

        print("\n📊 Текущие цены:")
        cur.execute("SELECT id, name, price FROM services")
        rows = cur.fetchall()

        if not rows:
            print("❌ Нет услуг в базе!")
            conn.close()
            return

        for row in rows:
            print(f"  {row[0]}. {row[1]} - {row[2]} ₽")

        print("\n🔄 Обновляем цены...")

        # Новые цены
        updates = [
            ("Курсовая работа", 2490),
            ("Школьный проект", 1490),
            ("Отчёт по практике", 2990),
            ("Доклад", 500),
            ("Презентация", 299),
            ("Защитное слово", 99),
        ]

        updated_count = 0
        for name, price in updates:
            cur.execute("UPDATE services SET price = ? WHERE name = ?", (price, name))
            if cur.rowcount > 0:
                print(f"  ✅ {name} → {price} ₽")
                updated_count += 1
            else:
                print(f"  ⚠️ {name} не найдена")

        conn.commit()

        print(f"\n✅ Обновлено {updated_count} услуг")

        print("\n📊 Проверка новых цен:")
        cur.execute("SELECT id, name, price FROM services")
        for row in cur.fetchall():
            print(f"  {row[0]}. {row[1]} - {row[2]} ₽")

        conn.close()
        print("\n🎉 Готово!")

    except Exception as e:
        print(f"❌ Ошибка: {e}")


if __name__ == "__main__":
    update_prices()