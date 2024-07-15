import psycopg2
from faker import Faker
import random

fake = Faker()

conn = psycopg2.connect(
    dbname="task_management",
    user="postgres",
    password="postgres",  # замініть на ваш пароль
    host="localhost",
    port="5432"
)

cur = conn.cursor()

# Додаємо статуси завдань
statuses = ['new', 'in progress', 'completed']
for status in statuses:
    cur.execute("INSERT INTO status (name) VALUES (%s) ON CONFLICT (name) DO NOTHING", (status,))

# Додаємо користувачів
for _ in range(10):
    fullname = fake.name()
    email = fake.unique.email()
    cur.execute("INSERT INTO users (fullname, email) VALUES (%s, %s)", (fullname, email))

# Додаємо завдання
cur.execute("SELECT id FROM users")
user_ids = cur.fetchall()

cur.execute("SELECT id FROM status")
status_ids = [row[0] for row in cur.fetchall()]

for _ in range(50):
    title = fake.sentence(nb_words=6)
    description = fake.text()
    status_id = random.choice(status_ids)
    user_id = random.choice(user_ids)[0]
    cur.execute("INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s)", (title, description, status_id, user_id))

conn.commit()

cur.close()
conn.close()
