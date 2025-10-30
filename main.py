from tkinter import *
from tkinter import ttk, messagebox
import sqlite3 as sq  # Исправлен импорт

# Инициализация БД
def init_db():
    try:
        with sq.connect("hospital.db") as con:
            cur = con.cursor()
            # Создание таблиц
            cur.executescript("""
                CREATE TABLE IF NOT EXISTS patient (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fio TEXT NOT NULL,
                    policy INTEGER UNIQUE NOT NULL,
                    age INTEGER,
                    doctor_is_office INTEGER
                );
                
                CREATE TABLE IF NOT EXISTS appointment (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    reception_time TEXT,
                    policy INTEGER,
                    FOREIGN KEY (policy) REFERENCES patient (policy)
                );
                
                CREATE TABLE IF NOT EXISTS doctor (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fio TEXT NOT NULL,
                    post TEXT,
                    age INTEGER,
                    doctor_is_office INTEGER
                );
            """)
    except sq.Error as e:
        messagebox.showerror("Ошибка БД", f"Не удалось создать таблицы:\n{e}")
        return False
    return True

# Заполнение тестовыми данными
def seed_data():
    try:
        with sq.connect("hospital.db") as con:
            cur = con.cursor()

            # Проверка и вставка пациента
            cur.execute("SELECT 1 FROM patient WHERE policy = 12312322")
            if not cur.fetchone():
                cur.execute(
                    "INSERT INTO patient (fio, policy, age, doctor_is_office) VALUES (?, ?, ?, ?)",
                    ("Екатерина Сергеевна Морозова", 12312322, 24, 360)
                )

            # Проверка и вставка приёма
            cur.execute("SELECT 1 FROM appointment WHERE policy = 12312322")
            if not cur.fetchone():
                cur.execute(
                    "INSERT INTO appointment (reception_time, policy) VALUES (?, ?)",
                    ("10:00", 12312322)
                )

            # Проверка и вставка врача
            cur.execute("SELECT 1 FROM doctor WHERE fio = 'Михаил Андреевич Лебедев'")
            if not cur.fetchone():
                cur.execute(
                    "INSERT INTO doctor (fio, post, age, doctor_is_office) VALUES (?, ?, ?, ?)",
                    ("Михаил Андреевич Лебедев", "Physician", 40, 360)
                )
    except sq.Error as e:
        messagebox.showerror("Ошибка БД", f"Не удалось заполнить тестовые данные:\n{e}")

# GUI
root = Tk()
root.title("Hospital Management System")
root.geometry("1000x650")
root.resizable(False, False)
root.configure(bg="#f0f0f0")

# Форма ввода
input_frame = ttk.LabelFrame(root, text="Управление записью", padding=(15, 10))
input_frame.pack(fill=X, padx=15, pady=(10, 5))


# Строка 0
ttk.Label(input_frame, text="ФИО пациента:", font=("Segoe UI", 9)).grid(row=0, column=0, sticky=W, pady=5, padx=(0, 10))
entry_fio = ttk.Entry(input_frame, width=28, font=("Segoe UI", 9))
entry_fio.grid(row=0, column=1, pady=5, sticky=EW)

ttk.Label(input_frame, text="Возраст:", font=("Segoe UI", 9)).grid(row=0, column=2, sticky=W, pady=5, padx=(20, 10))
entry_age = ttk.Entry(input_frame, width=8, font=("Segoe UI", 9))
entry_age.grid(row=0, column=3, pady=5)

# Строка 1
ttk.Label(input_frame, text="Полис:", font=("Segoe UI", 9)).grid(row=1, column=0, sticky=W, pady=5, padx=(0, 10))
entry_policy = ttk.Entry(input_frame, width=18, font=("Segoe UI", 9))
entry_policy.grid(row=1, column=1, pady=5, sticky=W)

ttk.Label(input_frame, text="Кабинет:", font=("Segoe UI", 9)).grid(row=1, column=2, sticky=W, pady=5, padx=(20, 10))
entry_office = ttk.Entry(input_frame, width=8, font=("Segoe UI", 9))
entry_office.grid(row=1, column=3, pady=5)

# Строка 2
ttk.Label(input_frame, text="Время приёма:", font=("Segoe UI", 9)).grid(row=2, column=0, sticky=W, pady=5, padx=(0, 10))
entry_time = ttk.Entry(input_frame, width=18, font=("Segoe UI", 9))
entry_time.grid(row=2, column=1, pady=5, sticky=W)

ttk.Label(input_frame, text="ФИО врача:", font=("Segoe UI", 9)).grid(row=2, column=2, sticky=W, pady=5, padx=(20, 10))
entry_doctor = ttk.Entry(input_frame, width=28, font=("Segoe UI", 9))
entry_doctor.grid(row=2, column=3, pady=5, sticky=EW, padx=(0, 5))

# Строка 3
ttk.Label(input_frame, text="Должность:", font=("Segoe UI", 9)).grid(row=3, column=0, sticky=W, pady=5, padx=(0, 10))
entry_post = ttk.Entry(input_frame, width=28, font=("Segoe UI", 9))
entry_post.grid(row=3, column=1, pady=5, sticky=EW, columnspan=3)


input_frame.columnconfigure(1, weight=1)
input_frame.columnconfigure(3, weight=1)


# Таблица (Treeview)
tree_frame = ttk.Frame(root)
tree_frame.pack(fill=BOTH, expand=True, padx=15, pady=5)

columns = ("fio", "age", "policy", "office", "time", "doctor", "post")
tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=16)

tree.heading("fio", text="ФИО пациента", anchor=W)
tree.heading("age", text="Возраст", anchor=CENTER)
tree.heading("policy", text="Полис", anchor=CENTER)
tree.heading("office", text="Кабинет", anchor=CENTER)
tree.heading("time", text="Время приёма", anchor=CENTER)
tree.heading("doctor", text="Врач", anchor=W)
tree.heading("post", text="Должность", anchor=W)

tree.column("fio", width=200, anchor=W)
tree.column("age", width=60, anchor=CENTER)
tree.column("policy", width=100, anchor=CENTER)
tree.column("policy", width=100, anchor=CENTER)
tree.column("office", width=80, anchor=CENTER)
tree.column("time", width=100, anchor=CENTER)
tree.column("doctor", width=200, anchor=W)
tree.column("post", width=140, anchor=W)

tree.pack(fill=BOTH, expand=True)

# Полосы прокрутки
vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
vsb.pack(side=RIGHT, fill=Y)
tree.configure(yscrollcommand=vsb.set)


hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
hsb.pack(side=BOTTOM, fill=X)
tree.configure(xscrollcommand=hsb.set)


# Функции управления данными
def load_data():
    """Загрузка данных в Treeview из БД"""
    try:
        with sq.connect("hospital.db") as con:
            cur = con.cursor()
            cur.execute("""
                SELECT
                    p.fio, p.age, p.policy, p.doctor_is_office,
                    a.reception_time, d.fio, d.post
                FROM patient p
                LEFT JOIN appointment a ON p.policy = a.policy
                LEFT JOIN doctor d ON p.doctor_is_office = d.doctor_is_office
            """)
            rows = cur.fetchall()

        # Очищаем таблицу
        for item in tree.get_children():
            tree.delete(item)
        
        # Заполняем данными
        for row in rows:
            tree.insert("", END, values=row)
            
    except sq.Error as e:
        messagebox.showerror("Ошибка БД", f"Не удалось загрузить данные:\n{e}")

def add_record():
    """Добавление новой записи"""
    fio = entry_fio.get().strip()
    age = entry_age.get().strip()
    policy = entry_policy.get().strip()
    office = entry_office.get().strip()
    time = entry_time.get().strip()
    doctor = entry_doctor.get().strip()
    post = entry_post.get().strip()

    # Валидация
    if not fio:
        messagebox.showwarning("Ошибка ввода", "Поле 'ФИО пациента' не может быть пустым!")
        return
    if not age.isdigit() or int(age) <= 0:
        messagebox.showwarning("Ошибка ввода", "Возраст должен быть положительным числом!")
        return
    if not policy.isdigit() or len(policy) < 5:
        messagebox.showwarning("Ошибка ввода", "Полис должен содержать минимум 5 цифр!")
        return
    if not office.isdigit() or int(office) <= 0:
        messagebox.showwarning("Ошибка ввода", "Номер кабинета должен быть положительным числом!")
        return

    try:
        with sq.connect("hospital.db") as con:
            cur = con.cursor()
            
            # Добавляем пациента
            cur.execute(
                "INSERT INTO patient (fio, policy, age, doctor_is_office) VALUES (?, ?, ?, ?)",
                (fio, int(policy), int(age), int(office))
            )
            
            # Добавляем приём
            cur.execute(
                "INSERT INTO appointment (reception_time, policy) VALUES (?, ?)",
                (time, int(policy))
            )
            
            # Добавляем врача (если его ещё нет)
            cur.execute(
                "SELECT 1 FROM doctor WHERE fio = ? AND doctor_is_office = ?",
                (doctor, int(office))
            )
            if not cur.fetchone():
                cur.execute(
                    "INSERT INTO doctor (fio, post, age, doctor_is_office) VALUES (?, ?, ?, ?)",
                    (doctor, post, 35, int(office))
                )
                
        load_data()
        messagebox.showinfo("Успех", "Запись успешно добавлена!")
        
    except sq.IntegrityError:
        messagebox.showerror("Ошибка", "Полис уже существует в базе!")
    except sq.Error as e:
        messagebox.showerror("Ошибка БД", f"Не удалось добавить запись:\n{e}")

def delete_record():
    """Удаление выделенной записи"""
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Внимание", "Выберите запись для удаления!")
        return

    values = tree.item(selected[0], "values")
    if len(values) < 3:
        messagebox.showerror("Ошибка", "Не удалось получить данные записи.")
        return

    policy = values[2]  # policy — третий столбец

    try:
        with sq.connect("hospital.db") as con:
            cur = con.cursor()
            cur.execute("DELETE FROM patient WHERE policy = ?", (policy,))
            cur.execute("DELETE FROM appointment WHERE policy = ?", (policy,))
        load_data()
        messagebox.showinfo("Успех", "Запись удалена!")
    except sq.Error as e:
        messagebox.showerror("Ошибка БД", f"Не удалось удалить запись:\n{e}")


def copy_record():
    """Копирование данных из выделенной строки в форму"""
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Внимание", "Выберите запись для копирования!")
        return

    values = tree.item(selected[0], "values")
    if len(values) < 7:
        messagebox.showerror("Ошибка", "Недостаточно данных для копирования.")
        return

    entry_fio.delete(0, END)
    entry_fio.insert(0, values[0])
    entry_age.delete(0, END)
    entry_age.insert(0, values[1])
    entry_policy.delete(0, END)
    entry_policy.insert(0, values[2])
    entry_office.delete(0, END)
    entry_office.insert(0, values[3])
    entry_time.delete(0, END)
    entry_time.insert(0, values[4])
    entry_doctor.delete(0, END)
    entry_doctor.insert(0, values[5])
    entry_post.delete(0, END)
    entry_post.insert(0, values[6])

# Кнопки управления
btn_frame = ttk.Frame(root)
btn_frame.pack(fill=X, padx=15, pady=(0, 10))

btn_add = ttk.Button(
    btn_frame,
    text="Добавить",
    command=add_record
)
btn_add.pack(side=LEFT, padx=(0, 8))

btn_delete = ttk.Button(
    btn_frame,
    text="Удалить",
    command=delete_record
)
btn_delete.pack(side=LEFT, padx=(0, 8))

btn_copy = ttk.Button(
    btn_frame,
    text="Копировать",
    command=copy_record
)
btn_copy.pack(side=LEFT)

# Инициализация приложения
if not init_db():
    root.destroy()
    exit()

seed_data()
load_data()

# Запуск приложения
root.mainloop()