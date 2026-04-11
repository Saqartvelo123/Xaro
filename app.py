from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from werkzeug.security import generate_password_hash

app = Flask(__name__)

# მონაცემთა ბაზის ინიციალიზაცია
def init_db():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        # ვქმნით ცხრილს, თუ ის უკვე არ არსებობს
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')
        conn.commit()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            return "გთხოვთ შეავსოთ ყველა ველი!"

        # 1. პაროლის დაჰეშვა (უსაფრთხოებისთვის)
        hashed_password = generate_password_hash(password)

        try:
            # 2. უსაფრთხო ჩაწერა ბაზაში (SQL Injection-ის პრევენცია)
            with sqlite3.connect('database.db') as conn:
                cursor = conn.cursor()
                # ვიყენებთ ? სიმბოლოებს f-string-ის ნაცვლად
                cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                               (username, hashed_password))
                conn.commit()
            return "რეგისტრაცია წარმატებით დასრულდა!"
        
        except sqlite3.IntegrityError:
            return "ეს მომხმარებლის სახელი უკვე დაკავებულია."
        except Exception as e:
            return f"მოხდა გაუთვალისწინებელი შეცდომა: {e}"
    
    return render_template('register.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
