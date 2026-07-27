import sqlite3
import os

# Находим базу данных
DB_NAME = "data/shop_bot.db"

# Если папка data не существует, пробуем persistent
if not os.path.exists("data"):
    DB_NAME = "/persistent/shop_bot.db"


def update_prices():
    try:
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()

        print("📊 Текущие цены:")
        cur.execute("SELECT id, name, price FROM services")
        rows = cur.fetchall()

        if not rows:
            print("❌ Таблица services пуста или не существует.")
            print("   Возможно, бот ещё не создал базу данных.")
            print("   Запустите бота хотя бы раз, чтобы создать БД.")
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

        for name, price in updates:
            cur.execute("UPDATE services SET price = ? WHERE name = ?", (price, name))
            if cur.rowcount > 0:
                print(f"  ✅ {name} → {price} ₽")
            else:
                print(f"  ⚠️ {name} не найдена")

        conn.commit()

        print("\n📊 Новые цены:")
        cur.execute("SELECT id, name, price FROM services")
        for row in cur.fetchall():
            print(f"  {row[0]}. {row[1]} - {row[2]} ₽")

        conn.close()
        print("\n✅ Готово!")

    except sqlite3.OperationalError as e:
        print(f"❌ Ошибка: {e}")
        print("   Проверьте, что база данных существует и путь правильный.")
        print(f"   Ищем БД по пути: {DB_NAME}")


if __name__ == "__main__":
    update_prices()