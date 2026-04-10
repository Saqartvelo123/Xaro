from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# მონაცემთა ბაზის შექმნა
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # ვქმნით ცხრილს: მომხმარებლის სახელი და პაროლი
    cursor.execute('CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # !!! უსაფრთხოების ხვრელი N1: SQL Injection !!!
        # მონაცემები გადაეცემა პირდაპირ სტრინგში f-string-ით
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        query = f"INSERT INTO users (username, password) VALUES ('{username}', '{password}')"
        cursor.execute(query)
        
        conn.commit()
        conn.close()
        return "რეგისტრაცია წარმატებულია! ახლა შენი მონაცემები 'ღიად' დევს ბაზაში."
    
    return render_template('register.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
