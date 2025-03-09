from flask import Flask, request, render_template, redirect, url_for
import mysql.connector
from werkzeug.security import generate_password_hash

app = Flask(__name__)

# Configure database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Aizen!!123",
    database="bookmyshow",
    auth_plugin='mysql_native_password'
)

@app.route('/index', methods=['POST'])
def index():
    name = request.form['name']
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']

    # Hash the password for security
    hashed_password = generate_password_hash(password)

    cursor = db.cursor()

    try:
        # Insert the form data into the users table
        cursor.execute(
            "INSERT INTO users (name, username, password, email) VALUES (%s, %s, %s, %s)",
            (name, username, hashed_password, email)
        )
        db.commit()
        return redirect(url_for('success'))
    except mysql.connector.Error as err:
        db.rollback()
        return f"Error: {err}"
    finally:
        cursor.close()

@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
