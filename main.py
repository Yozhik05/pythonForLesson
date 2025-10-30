from tkinter import *
from tkinter import ttk
import sqlite3 as sq

# Создание БД и таблиц
with sq.connect("hospital.db") as con:
    cur = con.cursor()

    # Создание таблиц
    cur.executescript("""
        CREATE TABLE IF NOT EXISTS patient (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fio TEXT,
            policy INTEGER,
            age INTEGER,
            doctor_is_office INTEGER
        );
        
        CREATE TABLE IF NOT EXISTS appointment (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reception_time TEXT,
            policy INTEGER
        );
        
        CREATE TABLE IF NOT EXISTS doctor (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fio TEXT,
            post TEXT,
            age INTEGER,
            doctor_is_office INTEGER
        );
    """)

    # Добавление тестовых данных (только если их ещё нет)
    cur.execute("SELECT COUNT(*) FROM appointment WHERE policy=12312322")
    if cur.fetchone()[0] == 0:
        cur.execute("INSERT INTO appointment (reception_time, policy) VALUES (?, ?)", ("10:00", 12312322))

    cur.execute("SELECT COUNT(*) FROM patient WHERE policy=12312322")
    if cur.fetchone()[0] == 0:
        cur.execute(
            "INSERT INTO patient (fio, policy, age, doctor_is_office) VALUES (?, ?, ?, ?)",
            ("Екатерина Сергеевна Морозова", 12312322, 24, 360)
        )

    cur.execute("SELECT COUNT(*) FROM doctor WHERE fio='Михаил Андреевич Лебедев'")
    if cur.fetchone()[0] == 0:
        cur.execute(
            "INSERT INTO doctor (fio, post, age, doctor_is_office) VALUES (?, ?, ?, ?)",
            ("Михаил Андреевич Лебедев", "Physician", 40, 360)
        )

# Создание GUI
root = Tk()
root.title("Hospital Management System")
root.geometry("800x400")

# Определение колонок для Treeview
columns = ("fio", "age", "policy", "doctor_is_office", "reception_time", "fio_doctor", "post")

# Создание Treeview
tree = ttk.Treeview(columns=columns, show="headings", height=15)
tree.pack(fill=BOTH, expand=1, padx=10, pady=10)

# Настройка заголовков
tree.heading("fio", text="ФИО пациента")
tree.heading("age", text="Возраст")
tree.heading("policy", text="Полис")
tree.heading("doctor_is_office", text="Кабинет врача")
tree.heading("reception_time", text="Время приёма")
tree.heading("fio_doctor", text="ФИО врача")
tree.heading("post", text="Должность")

# Настройка ширины колонок
tree.column("fio", width=150)
tree.column("age", width=60)
tree.column("policy", width=100)
tree.column("doctor_is_office", width=80)
tree.column("reception_time", width=100)
tree.column("fio_doctor", width=180)
tree.column("post", width=120)

# Функция для загрузки данных из БД в таблицу
def load_data():
    # Очищаем текущую таблицу
    for item in tree.get_children():
        tree.delete(item)

    # Выполняем JOIN-запрос для получения объединённых данных
    with sq.connect("hospital.db") as con:
        cur = con.cursor()
        cur.execute("""
            SELECT 
                p.fio,
                p.age,
                p.policy,
                p.doctor_is_office,
                a.reception_time,
                d.fio,
                d.post
            FROM patient p
            LEFT JOIN appointment a ON p.policy = a.policy
            LEFT JOIN doctor d ON p.doctor_is_office = d.doctor_is_office
        """)
        rows = cur.fetchall()

    # Добавляем данные в таблицу
    for row in rows:
        tree.insert("", END, values=row)

# Загружаем данные при запуске
load_data()

root.mainloop()
