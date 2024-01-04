import os

from flask import Flask, render_template, request, redirect, session, url_for, make_response
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'driving_success_db'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)
UPLOAD_FOLDER = 'static/uploads/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create users table in the database if not exists
with app.app_context():
    cursor = mysql.connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            first_name VARCHAR(255) NOT NULL,
            last_name VARCHAR(255) NOT NULL,
            username VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            role VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL
        )
    ''')
    mysql.connection.commit()
    cursor.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get user input from the registration form
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        hashed_password = sha256_crypt.encrypt(password)

        # Store user in the MySQL database
        cursor = mysql.connection.cursor()
        cursor.execute('''
            INSERT INTO users (first_name, last_name, username, email, role, password)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (first_name, last_name, username, email, role, hashed_password))
        mysql.connection.commit()
        cursor.execute('SELECT id FROM users WHERE username = %s', (username,))
        user_id = cursor.fetchone()['id']
        cursor.close()

        # Start a session and store user_id
        session['user_id'] = user_id

        # Redirect to the login page
        return redirect(url_for('capture_traits'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'jpg', 'jpeg', 'png', 'gif'}

@app.route('/capture_traits', methods=['GET', 'POST'])
def capture_traits():
    if request.method == 'POST':
        age = request.form.get('age')
        gender = request.form.get('gender')
        language = request.form.get('language')

        user_id = session.get('user_id')

        if user_id:
            # Update the users table with the submitted values
            cursor = mysql.connection.cursor()
            cursor.execute('''
                UPDATE users
                SET age = %s, gender = %s, language = %s
                WHERE id = %s
            ''', (age, gender, language, user_id))
            mysql.connection.commit()

            # Handle file upload
            if 'pic' in request.files:
                file = request.files['pic']
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(file_path)

                    # Update the users table with the file name
                    cursor.execute('''
                        UPDATE users
                        SET profile_pic_url = %s
                        WHERE id = %s
                    ''', (filename, user_id))
                    mysql.connection.commit()

            cursor.close()


            # Capture introversion/extroversion trait
            introversion_extroversion = request.form.get('introversion_extroversion')
            cursor = mysql.connection.cursor()
            cursor.execute('''
                            INSERT INTO user_traits (user_id, trait_id)
                            VALUES (%s, %s)
                        ''', (user_id, introversion_extroversion))
            mysql.connection.commit()
            cursor.close()


            # insert traits into user_traits table
            selected_traits = request.form.getlist('traits[]')
            cursor = mysql.connection.cursor()
            for trait_id in selected_traits:
                cursor.execute('''
                                INSERT INTO user_traits (user_id, trait_id)
                                VALUES (%s, %s)
                            ''', (user_id, trait_id))
            mysql.connection.commit()
            cursor.close()


            return redirect(url_for('success_page'))

    # If it's a GET request, retrieve traits from the database
    user_id = session.get('user_id')  # Assuming you store user_id in the session after login
    if user_id:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT id, trait_name FROM in_built_traits ORDER BY id LIMIT 18446744073709551615 OFFSET 2')
        traits = [{'trait_id': row['id'], 'trait_name': row['trait_name']} for row in cursor.fetchall()]
        cursor.close()

        return render_template('capture_traits.html', traits=traits)

    # If user_id is not available in the session
    return redirect(url_for('register'))

@app.route('/success_page', methods=['GET', 'POST'])
def success_page():
    return render_template('capture_success.html')


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.run(debug=True)