import sqlite3

# Укажите путь к скачанной БД
DB_PATH = "shop_bot.db"  # или путь к скачанному файлу


def update_prices():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    print("📊 Текущие цены:")
    cur.execute("SELECT id, name, price FROM services")
    rows = cur.fetchall()
    for row in rows:
        print(f"  {row[0]}. {row[1]} - {row[2]} ₽")

    print("\n🔄 Обновляем цены...")

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
    print("\n✅ Готово! Загрузите файл обратно на BotHost.")


if __name__ == "__main__":
    update_prices()