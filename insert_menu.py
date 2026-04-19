import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# CLEAR OLD MENU (THIS REMOVES DUPLICATES)
cursor.execute("DELETE FROM menu")

menu_items = [
    ("Onion Paratha",50),
    ("Aloo Paratha",40),
    ("Paneer Paratha",50),
    ("Aloo Butter Paratha",50),
    ("Aloo Cheese Paratha",60),
    ("Paneer Butter Paratha",60),
    ("Paneer Cheese Paratha",70),
    ("Onion Cheese Paratha",60),
    ("Methi Paratha",40),
    ("Aloo Methi Mix Paratha",60)
]

cursor.executemany(
    "INSERT INTO menu (name, price) VALUES (?, ?)",
    menu_items
)

conn.commit()
conn.close()

print("Menu reset and inserted successfully!")