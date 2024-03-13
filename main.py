import os

from flask import Flask, render_template, request, redirect, session, url_for, make_response, flash
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import secrets
import MySQLdb
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
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM users WHERE role = %s  LIMIT 6', ('instructor',))
    instructors = cursor.fetchall()
    cursor.close()
    user_id = session.get('user_id')
    user_info = None

    if user_id:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
        user_info = cursor.fetchone()
        cursor.close()
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE role = %s  LIMIT 6', ('instructor',))
        instructors = cursor.fetchall()
        cursor.execute('SELECT * FROM captured_learner_traits WHERE user_id = %s', (user_id,))
        learner_traits = cursor.fetchall()
        results = []
        for instructor in instructors:
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT * FROM captured_traits WHERE user_id = %s', (instructor['id'],))
            instructor_traits = cursor.fetchall()
            cursor.close()
            # Perform similarity check
            similarity_count = sum(1 for user_trait in learner_traits for instructor_trait in instructor_traits
                                   if user_trait['trait_category_id'] == instructor_trait['trait_category_id']
                                   and user_trait['captured_trait'] == instructor_trait['captured_trait'])
            similarity_percentage = round(similarity_count / 13 * 100)
            results.append({
                'instructor_id': f"{instructor['id']} ",
                'instructor_name': f"{instructor['first_name']} {instructor['last_name']}",
                'profile_pic_url': f"{instructor['profile_pic_url']} ",
                'similarity_percentage': similarity_percentage
            })
            results = sorted(results, key=lambda x: x['similarity_percentage'], reverse=True)

        return render_template('index.html', user_info=user_info, results=results)

    return render_template('index.html', user_info=user_info,instructors=instructors)

@app.route('/view_instructors', methods=['GET', 'POST'])
def view_instructors():
    user_id = session.get('user_id')
    user_info = None
    cursor = mysql.connection.cursor()
    query = '''
        SELECT users.*, instructor_details.*
        FROM users
        INNER JOIN instructor_details ON users.id = instructor_details.user_id
        WHERE users.role = %s
    '''
    cursor.execute(query, ('instructor',))
    instructors = cursor.fetchall()
    cursor.close()

    if user_id:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
        user_info = cursor.fetchone()
        cursor.close()

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM captured_learner_traits WHERE user_id = %s', (user_id,))
        learner_traits = cursor.fetchall()

        results = []
        for instructor in instructors:

            cursor = mysql.connection.cursor()
            cursor.execute('SELECT * FROM captured_traits WHERE user_id = %s', (instructor['id'],))
            instructor_traits = cursor.fetchall()
            cursor.close()

            # Perform similarity check
            similarity_count = sum(1 for user_trait in learner_traits for instructor_trait in instructor_traits
                                   if user_trait['trait_category_id'] == instructor_trait['trait_category_id']
                                   and user_trait['captured_trait'] == instructor_trait['captured_trait'])
            similarity_percentage = round(similarity_count / 13 * 100)

            results.append({
                'instructor_id': f"{instructor['id']} ",
                'instructor_name': f"{instructor['first_name']} {instructor['last_name']}",
                'profile_pic_url': f"{instructor['profile_pic_url']} ",
                'similarity_percentage': similarity_percentage
            })
            results = sorted(results, key=lambda x: x['similarity_percentage'], reverse=True)

        return render_template('view_instructors.html', user_info=user_info, results=results)

    return render_template('view_instructors.html', user_info=user_info, instructors=instructors)

@app.route('/filter_instructors', methods=['GET', 'POST'])
def filter_instructors():
    user_info = None
    if request.method == 'POST':
        vehicle_transmission_type = request.form.get('vehicle_transmission_type')
        vehicle_category = request.form.get('vehicle_category')
        experience = request.form.get('experience')
        charges_max = request.form.get('charges_max')

        min_experience = 0
        max_experience = 100

        if experience == 'zero':
            max_experience = 1
        elif experience == 'one-to-five':
            min_experience, max_experience = 1, 5
        elif experience == 'six-to-nine':
            min_experience, max_experience = 6, 9
        elif experience == 'ten-plus':
            min_experience = 10

        user_id = session.get('user_id')
        if user_id:
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
            user_info = cursor.fetchone()
            cursor.close()

            cursor = mysql.connection.cursor()
            query = '''
                    SELECT users.*, instructor_details.*
                    FROM users
                    INNER JOIN instructor_details ON users.id = instructor_details.user_id
                    WHERE users.role = %s
                        AND instructor_details.instructor_charges <= %s
                        AND instructor_details.instructor_vehicle_transmission_type = %s
                        AND instructor_details.instructor_vehicle_category = %s
                        AND instructor_details.instructor_experience BETWEEN %s AND %s
                '''
            cursor.execute(query, (
            'instructor', charges_max, vehicle_transmission_type, vehicle_category, min_experience, max_experience))
            instructors = cursor.fetchall()

            cursor.execute('SELECT * FROM captured_learner_traits WHERE user_id = %s', (user_id,))
            learner_traits = cursor.fetchall()

            results = []

            for instructor in instructors:
                cursor = mysql.connection.cursor()
                cursor.execute('SELECT * FROM captured_traits WHERE user_id = %s', (instructor['id'],))
                instructor_traits = cursor.fetchall()
                cursor.close()

                # Perform similarity check
                similarity_count = sum(1 for user_trait in learner_traits for instructor_trait in instructor_traits
                                       if user_trait['trait_category_id'] == instructor_trait['trait_category_id']
                                       and user_trait['captured_trait'] == instructor_trait['captured_trait'])
                similarity_percentage = round(similarity_count / 13 * 100)

                results.append({
                    'instructor_id': f"{instructor['id']} ",
                    'instructor_name': f"{instructor['first_name']} {instructor['last_name']}",
                    'profile_pic_url': f"{instructor['profile_pic_url']} ",
                    'similarity_percentage': similarity_percentage
                })


            results = sorted(results, key=lambda x: x['similarity_percentage'], reverse=True)


            return render_template('view_instructors.html', user_info=user_info, results=results)

    return render_template('view_instructors.html', user_info=user_info)





@app.route('/view_learner_traits')
def view_learner_traits():
    user_id = session.get('user_id')
    user_info = None

    if user_id:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
        user_info = cursor.fetchone()
        cursor.close()


    return render_template('index.html', user_info=user_info)



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get user input from the registration form
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        username = request.form['username']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        role = request.form['role']
        hashed_password = sha256_crypt.encrypt(password)

        # Store user in the  database
        cursor = mysql.connection.cursor()
        cursor.execute('''
            INSERT INTO users (first_name, last_name, username, email, phone, role, password)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (first_name, last_name, username, email, phone, role, hashed_password))
        mysql.connection.commit()
        cursor.execute('SELECT id FROM users WHERE username = %s', (username,))
        user_id = cursor.fetchone()['id']
        cursor.close()
        # Start session and store user_id
        session['user_id'] = user_id
        if role == 'learner':
            return redirect(url_for('capture_traits'))
        elif role == 'instructor':
            return redirect(url_for('instructor_on_boarding'))


    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password_candidate = request.form.get('password')

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT id, password, role FROM users WHERE email = %s', (email,))
        user = cursor.fetchone()
        cursor.close()

        if user and sha256_crypt.verify(password_candidate, user['password']):
            # Password is correct, log in the user
            session['user_id'] = user['id']
            role = user['role']
            if role == "instructor":
                return redirect(url_for('instructor_dashboard'))
            else:
                return redirect(url_for('home'))
        else:
            # Invalid credentials
            return render_template('login.html', error='Invalid email or password')

    return render_template('login.html')

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        user = cursor.fetchone()
        cursor.close()

        if user:
            token = secrets.token_urlsafe(20)
            cursor = mysql.connection.cursor()
            cursor.execute('''
                                INSERT INTO password_reset (email, token)
                                VALUES (%s, %s)
                            ''', (email, token))
            mysql.connection.commit()
            cursor.close()
            return redirect(url_for('confirm_password', email=email, token=token))
        else:
            return render_template('forgot_password.html', error="Email not found.")

    return render_template('forgot_password.html')


@app.route('/confirm_password', methods=['GET', 'POST'])
def confirm_password():
    email = request.args.get('email', '')
    token = request.args.get('token', '')
    if request.method == 'POST':
            return render_template('forgot_password.html', error="Email not found.")

    return render_template('confirm_password.html', email=email, token=token)


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'GET':
        # Handle GET request
        email = request.args.get('email', '')
        token = request.args.get('token', '')
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM password_reset WHERE email = %s AND token = %s', (email, token))
        password_reset_row = cursor.fetchone()
        cursor.close()

        if password_reset_row:
            return render_template('reset_password.html', email=email)
        else:
            return render_template('forgot_password.html', error='Invalid email or token')

    elif request.method == 'POST':
        # Handle POST request
        email = request.form.get('email', '')
        new_password = request.form.get('new_password', '')

        try:
            hashed_password = sha256_crypt.encrypt(new_password)

            # Update the user's password in the users table
            cursor = mysql.connection.cursor()
            cursor.execute('UPDATE users SET password = %s WHERE email = %s', (hashed_password, email))
            mysql.connection.commit()
            cursor.close()

            # Delete the password_reset_row from the password_reset table
            cursor = mysql.connection.cursor()
            cursor.execute('DELETE FROM password_reset WHERE email = %s', (email,))
            mysql.connection.commit()
            cursor.close()

            return redirect(url_for('login'))

        except Exception as e:
            # Handle the exception (e.g., display an error message or log the error)
            return render_template('error.html', error=str(e))



@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))



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
                    cursor.execute('''
                        UPDATE users
                        SET profile_pic_url = %s
                        WHERE id = %s
                    ''', (filename, user_id))
                    mysql.connection.commit()

            cursor.close()
            captured_traits = []
            for key, value in request.form.items():
                if key.startswith('trait_category_') and value.isdigit():
                    trait_category_id = int(key.split('_')[-1])
                    captured_trait_id = int(value)
                    captured_traits.append((user_id, trait_category_id, captured_trait_id))
            cursor = mysql.connection.cursor()
            cursor.executemany('''
                            INSERT INTO captured_learner_traits (user_id, trait_category_id, captured_trait)
                            VALUES (%s, %s, %s)
                        ''', captured_traits)
            mysql.connection.commit()
            cursor.close()


            return redirect(url_for('success_page'))


    user_id = session.get('user_id')
    if user_id:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM trait_categories')
        trait_categories = [
            {'trait_id': row['id'], 'trait_category_name': row['trait_category_name'], 'question': row['learner_q']}
            for row in cursor.fetchall()]
        for trait_category in trait_categories:
            cursor.execute('SELECT * FROM in_built_learner_traits WHERE trait_category = %s',
                           (trait_category['trait_id'],))
            traits = [{'trait_id': row['id'], 'trait_name': row['trait_name']} for row in cursor.fetchall()]
            trait_category['traits'] = traits
        cursor.close()
        return render_template('capture_traits.html', trait_categories=trait_categories)
    # If user_id is not available in the session
    return redirect(url_for('register'))

@app.route('/success_page', methods=['GET', 'POST'])
def success_page():
    return render_template('capture_success.html')
@app.route('/instructor_success_page', methods=['GET', 'POST'])
def instructor_success_page():
    return render_template('capture_instructor_success.html')

# Instructor onboarding
@app.route('/instructor_on_boarding', methods=['GET', 'POST'])
def instructor_on_boarding():
    user_id = session.get('user_id')
    if user_id:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM trait_categories')
        trait_categories = [
            {'trait_id': row['id'], 'trait_category_name': row['trait_category_name'], 'question': row['instructor_q']}
            for row in cursor.fetchall()]

        for trait_category in trait_categories:
            cursor.execute('SELECT * FROM in_built_instructor_traits WHERE trait_category = %s',
                           (trait_category['trait_id'],))
            traits = [{'trait_id': row['id'], 'trait_name': row['trait_name']} for row in cursor.fetchall()]
            trait_category['traits'] = traits

        cursor.close()
        return render_template('instructor_on_boarding.html', trait_categories=trait_categories)

    return redirect(url_for('register'))

@app.route('/capture_instructor_traits', methods=['GET', 'POST'])
def capture_instructor_traits():
    if request.method == 'POST':
        age = request.form.get('age')
        gender = request.form.get('gender')
        language = request.form.get('language')
        instructor_description = request.form.get('instructor_description')
        instructor_experience  = request.form.get('instructor_experience')
        vehicle_transmission_type = request.form.get('vehicle_transmission_type')
        vehicle_category = request.form.get('vehicle_category')
        vehicle_model =  request.form.get('vehicle_model')
        instructor_charges_per_session = request.form.get('instructor_charges_per_session')
        instructor_minutes_per_session = request.form.get('instructor_minutes_per_session')
        user_id = session.get('user_id')

        if user_id:

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
                    cursor.execute('''
                        UPDATE users
                        SET profile_pic_url = %s
                        WHERE id = %s
                    ''', (filename, user_id))
                    mysql.connection.commit()

            cursor.close()


            cursor = mysql.connection.cursor()
            cursor.execute('''
                INSERT INTO instructor_details (user_id, instructor_experience, instructor_charges, instructor_vehicle_transmission_type, instructor_vehicle_category, instructor_vehicle_model, instructor_description, instructor_mins_per_session)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ''', (user_id, instructor_experience, instructor_charges_per_session, vehicle_transmission_type, vehicle_category, vehicle_model, instructor_description, instructor_minutes_per_session ))
            mysql.connection.commit()
            cursor.close()
            captured_traits = []
            for key, value in request.form.items():
                if key.startswith('trait_category_') and value.isdigit():
                    trait_category_id = int(key.split('_')[-1])
                    captured_trait_id = int(value)
                    captured_traits.append((user_id, trait_category_id, captured_trait_id))


            cursor = mysql.connection.cursor()
            cursor.executemany('''
                            INSERT INTO captured_traits (user_id, trait_category_id, captured_trait)
                            VALUES (%s, %s, %s)
                        ''', captured_traits)
            mysql.connection.commit()
            cursor.close()


            return redirect(url_for('instructor_success_page'))
    return redirect(url_for('register'))

@app.route('/view_single_instructor_details/<int:instructor_id>')
def view_single_instructor_details(instructor_id):
    user_id = session.get('user_id')
    user_info = None
    if user_id:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE id = %s', (instructor_id,))
        instructor = cursor.fetchone()
        cursor.close()
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM instructor_details WHERE user_id = %s', (instructor_id,))
        instructor_details = cursor.fetchone()
        cursor.close()
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
        user_info = cursor.fetchone()
        role = user_info['role']
        cursor.close()
        if role == 'learner':
            return render_template('single_instructor_details.html', instructor=instructor, user_info=user_info, instructor_details=instructor_details)
        else:
            return render_template('error_2.html', error='This action is only available to learner accounts')
    return render_template('login.html', error='Please log in to view instructor details')

@app.route('/view_single_learner_details/<int:learner_id>')
def view_single_learner_details(learner_id):
    user_id = session.get('user_id')
    user_info = None
    if user_id:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE id = %s', (learner_id,))
        learner = cursor.fetchone()
        cursor.close()
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
        user_info = cursor.fetchone()
        role = user_info['role']
        cursor.close()
        if role == 'instructor':
            return render_template('single_learner_details.html', learner=learner, user_info=user_info)
        else:
            return render_template('error_2.html', error='This action is only available to instructor accounts')
    return render_template('login.html', error='Please log in to view instructor details')



@app.route('/find_instructors',  methods=['GET', 'POST'])
def find_instructors():
    user_id = session.get('user_id')
    user_info = None

    if user_id:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
        user_info = cursor.fetchone()
        cursor.close()

        return render_template('find_instructors.html', user_info=user_info)
    return redirect(url_for('view_instructors'))

@app.route('/instructor_dashboard', methods=['GET', 'POST'])
def instructor_dashboard():
    user_id = session.get('user_id')
    user_info = None

    if user_id:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
        user_info = cursor.fetchone()
        cursor.close()
        cursor = mysql.connection.cursor()
        cursor.execute('''
                SELECT appointments.*, users.*
                FROM appointments
                JOIN users ON appointments.learner_id = users.id
                WHERE instructor_id = %s
            ''', (user_id,))
        instructor_appointments = cursor.fetchall()
        cursor.close()
        return render_template('instructor_dashboard.html', user_info=user_info, instructor_appointments=instructor_appointments)

    return redirect(url_for('login'))


@app.route('/book_appointment', methods=['POST'])
def book_appointment():
    if request.method == 'POST':
        learner_id = request.form.get('learner_id')
        instructor_id = request.form.get('instructor_id')
        appointment_date_time_str = request.form.get('appointment_date_time')
        appointment_date_time = datetime.strptime(appointment_date_time_str, '%Y-%m-%dT%H:%M')

        # Calculate the end time of the appointment (assuming each appointment takes 2 hours)
        appointment_end_time = appointment_date_time + timedelta(hours=2)

        # Check  time slot is available
        cursor = mysql.connection.cursor()
        cursor.execute('''
                        SELECT * FROM appointments
                        WHERE instructor_id = %s
                        AND ((%s >= appointment_date_time AND %s < DATE_ADD(appointment_date_time, INTERVAL 2 HOUR))
                             OR (%s > appointment_date_time AND %s <= appointment_date_time))
                    ''', (instructor_id, appointment_date_time, appointment_date_time,
                          appointment_date_time, appointment_date_time))

        existing_appointment = cursor.fetchone()

        if existing_appointment:
            flash("Appointment time slot is already booked for the selected date and time", "danger")
            cursor.close()
            return redirect(url_for('view_single_instructor_details', instructor_id=instructor_id))
        else:
            cursor = mysql.connection.cursor()
            # If time slot is available, insert  new appointment
            cursor.execute('''
                            INSERT INTO appointments (learner_id, instructor_id, appointment_date_time)
                            VALUES (%s, %s, %s)
                        ''', (learner_id, instructor_id, appointment_date_time))

            mysql.connection.commit()
            flash("Appointment booked successfully", "success")
            cursor.close()
            return redirect(url_for('learner_dashboard'))
    return redirect(url_for('home'))


@app.route('/update_appointment_status_instructor', methods=['POST'])
def update_appointment_status():
    if request.method == 'POST':
        learner_id = request.form.get('learner_id')
        instructor_id = int(request.form.get('instructor_id'))
        appointment_date_time_str = request.form.get('appointment_date_time')
        submitted_action = request.form.get('submit')
        print(instructor_id)

        new_state = 1 if submitted_action == "Approve" else 2

        user_id = int(session.get('user_id'))
        print(user_id)
        if user_id == instructor_id:
            try:

                appointment_date_time = datetime.strptime(appointment_date_time_str, '%Y-%m-%dT%H:%M')
                cursor = mysql.connection.cursor()
                cursor.execute('''
                                UPDATE appointments
                                SET status = %s
                                WHERE learner_id = %s
                                  AND instructor_id = %s
                                  AND appointment_date_time = %s
                            ''', (new_state, learner_id, instructor_id, appointment_date_time))

                mysql.connection.commit()
                cursor.close()

                if new_state == 1:
                    flash("Appointment approved successfully", "success")
                else:
                    flash("Appointment cancelled successfully", "success")

                return redirect(url_for('instructor_dashboard'))
            except Exception as e:
                flash(f"Error updating appointment status: {str(e)}", "error")
                return redirect(url_for('instructor_dashboard'))

        flash("You do not have the rights to perform this action", "error")
        return redirect(url_for('instructor_dashboard'))

    flash("Something went wrong", "error")
    return redirect(url_for('instructor_dashboard'))



@app.route('/learner_dashboard', methods=['GET', 'POST'])
def learner_dashboard():
    user_id = session.get('user_id')
    user_info = None

    if user_id:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
        user_info = cursor.fetchone()
        cursor.close()
        cursor = mysql.connection.cursor()
        cursor.execute('''
                   SELECT appointments.*, users.*, instructor_details.instructor_charges
                   FROM appointments
                   JOIN users ON appointments.instructor_id = users.id
                   JOIN instructor_details ON appointments.instructor_id = instructor_details.user_id
                   WHERE learner_id = %s
               ''', (user_id,))
        learner_appointments = cursor.fetchall()
        cursor.close()
        return render_template('learner_dashboard.html', user_info=user_info, learner_appointments=learner_appointments)

    return redirect(url_for('login'))

@app.route('/update_appointment_status_learner', methods=['POST'])
def update_appointment_status_leaner():
    if request.method == 'POST':
        learner_id = int(request.form.get('learner_id'))
        instructor_id = int(request.form.get('instructor_id'))
        appointment_date_time_str = request.form.get('appointment_date_time')
        submitted_action = request.form.get('submit')
        print(learner_id)

        new_state = 1 if submitted_action == "Approve" else 2

        user_id = int(session.get('user_id'))
        print(user_id)
        if user_id == learner_id:
            try:
                appointment_date_time = datetime.strptime(appointment_date_time_str, '%Y-%m-%dT%H:%M')
                cursor = mysql.connection.cursor()
                cursor.execute('''
                                UPDATE appointments
                                SET status = %s
                                WHERE learner_id = %s
                                  AND instructor_id = %s
                                  AND appointment_date_time = %s
                            ''', (new_state, learner_id, instructor_id, appointment_date_time))

                mysql.connection.commit()
                cursor.close()
                if new_state == 1:
                    flash("Appointment approved successfully", "success")
                else:
                    flash("Appointment cancelled successfully", "success")

                return redirect(url_for('learner_dashboard'))
            except Exception as e:
                flash(f"Error updating appointment status: {str(e)}", "error")
                return redirect(url_for('learner_dashboard'))

        flash("You do not have the rights to perform this action", "error")
        return redirect(url_for('learner_dashboard'))

    flash("Something went wrong", "error")
    return redirect(url_for('learner_dashboard'))


@app.route('/profile')
def view_profile():
    user_id = session.get('user_id')
    user_info = None

    if user_id:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
        user_info = cursor.fetchone()
        cursor.close()


    return render_template('profile.html', user_info=user_info)

@app.route('/edit-profile', methods=['GET', 'POST'])
def edit_profile():
    user_id = session.get('user_id')
    user_info = None

    if user_id:
        cursor = mysql.connection.cursor()
        if request.method == 'POST':
            # Retrieve form data for updating user profile
            username = request.form['username']
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            email = request.form['email']
            age = request.form['age']

            # Update user info in the database
            cursor.execute('UPDATE users SET username = %s, first_name = %s, last_name = %s, email = %s, age = %s WHERE id = %s', (username, first_name, last_name, email, age, user_id))
            mysql.connection.commit()

            # Redirect to profile page after updating
            return redirect(url_for('view_profile'))
        else:
            # Fetch user info for rendering edit profile page
            cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
            user_info = cursor.fetchone()

        cursor.close()

    return render_template('edit_profile.html', user_info=user_info)



if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.run(debug=True)