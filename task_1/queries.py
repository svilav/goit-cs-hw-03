import psycopg2

conn = psycopg2.connect(
    dbname="task_management",
    user="postgres",
    password="postgres",  # замініть на ваш пароль
    host="localhost",
    port="5432"
)

cur = conn.cursor()

def get_all_tasks_for_user(user_id):
    cur.execute("SELECT * FROM tasks WHERE user_id = %s", (user_id,))
    return cur.fetchall()

def get_tasks_by_status(status_name):
    cur.execute("""
    SELECT * FROM tasks WHERE status_id = (
        SELECT id FROM status WHERE name = %s
    )
    """, (status_name,))
    return cur.fetchall()

def update_task_status(task_id, new_status_name):
    cur.execute("""
    UPDATE tasks 
    SET status_id = (SELECT id FROM status WHERE name = %s)
    WHERE id = %s
    """, (new_status_name, task_id))
    conn.commit()

def get_users_with_no_tasks():
    cur.execute("""
    SELECT * FROM users WHERE id NOT IN (SELECT user_id FROM tasks)
    """)
    return cur.fetchall()

def add_new_task(title, description, status_name, user_id):
    cur.execute("""
    INSERT INTO tasks (title, description, status_id, user_id)
    VALUES (%s, %s, (SELECT id FROM status WHERE name = %s), %s)
    """, (title, description, status_name, user_id))
    conn.commit()

def get_uncompleted_tasks():
    cur.execute("""
    SELECT * FROM tasks WHERE status_id != (
        SELECT id FROM status WHERE name = 'completed'
    )
    """)
    return cur.fetchall()

def delete_task(task_id):
    cur.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    conn.commit()

def find_users_by_email(email_pattern):
    cur.execute("SELECT * FROM users WHERE email LIKE %s", (email_pattern,))
    return cur.fetchall()

def update_user_name(user_id, new_name):
    cur.execute("UPDATE users SET fullName = %s WHERE id = %s", (new_name, user_id))
    conn.commit()

def get_task_count_by_status():
    cur.execute("""
    SELECT s.name, COUNT(t.id) FROM tasks t
    JOIN status s ON t.status_id = s.id
    GROUP BY s.name
    """)
    return cur.fetchall()

def get_tasks_by_email_domain(domain_pattern):
    cur.execute("""
    SELECT t.* FROM tasks t
    JOIN users u ON t.user_id = u.id
    WHERE u.email LIKE %s
    """, (domain_pattern,))
    return cur.fetchall()

def get_tasks_without_description():
    cur.execute("SELECT * FROM tasks WHERE description IS NULL OR description = ''")
    return cur.fetchall()

def get_inprogress_tasks_with_users():
    cur.execute("""
    SELECT u.*, t.* FROM tasks t
    JOIN users u ON t.user_id = u.id
    WHERE t.status_id = (
        SELECT id FROM status WHERE name = 'in progress'
    )
    """)
    return cur.fetchall()

def get_users_with_tasks_count():
    cur.execute("""
    SELECT u.id, u.fullname, u.email, COUNT(t.id) as task_count 
    FROM users u
    LEFT JOIN tasks t ON u.id = t.user_id
    GROUP BY u.id
    """)
    return cur.fetchall()

if __name__ == "__main__":
    user_id = 1
    print(get_all_tasks_for_user(user_id))

    status_name = 'new'
    print(get_tasks_by_status(status_name))

    task_id = 1
    new_status_name = 'in progress'
    update_task_status(task_id, new_status_name)

    print(get_users_with_no_tasks())

    title = 'New Task'
    description = 'New Task Description'
    status_name = 'new'
    user_id = 1
    add_new_task(title, description, status_name, user_id)

    print(get_uncompleted_tasks())

    task_id = 2
    delete_task(task_id)

    email_pattern = '%@example.com'
    print(find_users_by_email(email_pattern))

    user_id = 1
    new_name = 'Updated Name'
    update_user_name(user_id, new_name)

    print(get_task_count_by_status())

    domain_pattern = '%@example.com'
    print(get_tasks_by_email_domain(domain_pattern))

    print(get_tasks_without_description())

    print(get_inprogress_tasks_with_users())

    print(get_users_with_tasks_count())

cur.close()
conn.close()
