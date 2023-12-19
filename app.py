from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database setup
DB_NAME = 'tasks.db'

def create_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            priority TEXT,
            due_date TEXT,
            completed BOOLEAN
        )
    ''')

    conn.commit()
    conn.close()

create_table()

# Routes
@app.route('/')
def index():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()

    conn.close()

    return render_template('index.html', tasks=tasks)

@app.route('/add_task', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        name = request.form['name']
        priority = request.form['priority']
        due_date = request.form['due_date']

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO tasks (name, priority, due_date, completed)
            VALUES (?, ?, ?, ?)
        ''', (name, priority, due_date, False))

        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    return render_template('add_task.html')

@app.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        priority = request.form['priority']
        due_date = request.form['due_date']
        completed = 'completed' in request.form

        cursor.execute('''
            UPDATE tasks
            SET name=?, priority=?, due_date=?, completed=?
            WHERE id=?
        ''', (name, priority, due_date, completed, task_id))

        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    cursor.execute('SELECT * FROM tasks WHERE id=?', (task_id,))
    task = cursor.fetchone()

    conn.close()

    return render_template('edit_task.html', task=task)

@app.route('/delete_task/<int:task_id>')
def delete_task(task_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('DELETE FROM tasks WHERE id=?', (task_id,))

    conn.commit()
    conn.close()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
