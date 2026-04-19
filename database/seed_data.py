from database.db import get_db_connection

def insert_menu():
    conn = get_db_connection()
    cursor = conn.cursor()

    items = [
        ("Onion Paratha", 50),
        ("Aloo Paratha", 40),
        ("Paneer Paratha", 50)
    ]

    cursor.executemany(
        "INSERT INTO menu_items (name, price) VALUES (?, ?)", items
    )

    conn.commit()
    conn.close()
    print("Menu inserted!")

insert_menu()