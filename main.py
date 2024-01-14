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
    user_id = session.get('user_id')
    user_info = None

    if user_id:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
        user_info = cursor.fetchone()
        cursor.close()

        # Fetch instructors
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE role = %s  LIMIT 6', ('instructor',))
        instructors = cursor.fetchall()

        # Fetch captured traits for the user
        cursor.execute('SELECT * FROM captured_learner_traits WHERE user_id = %s', (user_id,))
        learner_traits = cursor.fetchall()

        # Prepare a list to store the results
        results = []

        # Calculate and store the similarity count for each instructor
        for instructor in instructors:
            # Fetch captured traits for each instructor
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT * FROM captured_traits WHERE user_id = %s', (instructor['id'],))
            instructor_traits = cursor.fetchall()
            cursor.close()

            # Perform similarity check
            similarity_count = sum(1 for user_trait in learner_traits for instructor_trait in instructor_traits
                                   if user_trait['trait_category_id'] == instructor_trait['trait_category_id']
                                   and user_trait['captured_trait'] == instructor_trait['captured_trait'])
            similarity_percentage = round(similarity_count / 13 * 100)

            # Append results for this instructor
            results.append({
                'instructor_id': f"{instructor['id']} ",
                'instructor_name': f"{instructor['first_name']} {instructor['last_name']}",
                'profile_pic_url': f"{instructor['profile_pic_url']} ",
                'similarity_percentage': similarity_percentage
            })
            results = sorted(results, key=lambda x: x['similarity_percentage'], reverse=True)

        # Move the return statement outside of the loop
        return render_template('index.html', user_info=user_info, results=results)

    return render_template('index.html', user_info=user_info)

@app.route('/view_instructors', methods=['GET', 'POST'])
def view_instructors():
    user_id = session.get('user_id')
    user_info = None

    if user_id:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
        user_info = cursor.fetchone()
        cursor.close()

        # Fetch instructors with additional information from instructor_details
        cursor = mysql.connection.cursor()
        query = '''
            SELECT users.*, instructor_details.*
            FROM users
            INNER JOIN instructor_details ON users.id = instructor_details.user_id
            WHERE users.role = %s
        '''
        cursor.execute(query, ('instructor',))
        instructors = cursor.fetchall()

        # Fetch captured traits for the user
        cursor.execute('SELECT * FROM captured_learner_traits WHERE user_id = %s', (user_id,))
        learner_traits = cursor.fetchall()

        # Prepare a list to store the results
        results = []

        # Calculate and store the similarity count for each instructor
        for instructor in instructors:
            # Fetch captured traits for each instructor
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT * FROM captured_traits WHERE user_id = %s', (instructor['id'],))
            instructor_traits = cursor.fetchall()
            cursor.close()

            # Perform similarity check
            similarity_count = sum(1 for user_trait in learner_traits for instructor_trait in instructor_traits
                                   if user_trait['trait_category_id'] == instructor_trait['trait_category_id']
                                   and user_trait['captured_trait'] == instructor_trait['captured_trait'])
            similarity_percentage = round(similarity_count / 13 * 100)

            # Append results for this instructor
            results.append({
                'instructor_id': f"{instructor['id']} ",
                'instructor_name': f"{instructor['first_name']} {instructor['last_name']}",
                'profile_pic_url': f"{instructor['profile_pic_url']} ",
                'similarity_percentage': similarity_percentage
            })
            results = sorted(results, key=lambda x: x['similarity_percentage'], reverse=True)

        # Move the return statement outside of the loop
        return render_template('view_instructors.html', user_info=user_info, results=results)

    return render_template('view_instructors.html', user_info=user_info)

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
            # perform filtering from the search From
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

            # Fetch captured traits for the user
            cursor.execute('SELECT * FROM captured_learner_traits WHERE user_id = %s', (user_id,))
            learner_traits = cursor.fetchall()

            # Prepare a list to store the results
            results = []

            # Calculate and store the similarity count for each instructor
            for instructor in instructors:
                # Fetch captured traits for each instructor
                cursor = mysql.connection.cursor()
                cursor.execute('SELECT * FROM captured_traits WHERE user_id = %s', (instructor['id'],))
                instructor_traits = cursor.fetchall()
                cursor.close()

                # Perform similarity check
                similarity_count = sum(1 for user_trait in learner_traits for instructor_trait in instructor_traits
                                       if user_trait['trait_category_id'] == instructor_trait['trait_category_id']
                                       and user_trait['captured_trait'] == instructor_trait['captured_trait'])
                similarity_percentage = round(similarity_count / 13 * 100)

                # Append results for this instructor
                results.append({
                    'instructor_id': f"{instructor['id']} ",
                    'instructor_name': f"{instructor['first_name']} {instructor['last_name']}",
                    'profile_pic_url': f"{instructor['profile_pic_url']} ",
                    'similarity_percentage': similarity_percentage
                })

            # Move the sorting outside the loop
            results = sorted(results, key=lambda x: x['similarity_percentage'], reverse=True)

            # Move the return statement outside of the loop
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
        cursor.execute('SELECT id, password FROM users WHERE email = %s', (email,))
        user = cursor.fetchone()
        cursor.close()

        if user and sha256_crypt.verify(password_candidate, user['password']):
            # Password is correct, log in the user
            session['user_id'] = user['id']
            return redirect(url_for('home'))
        else:
            # Invalid credentials, show an error message or redirect to the login page
            return render_template('login.html', error='Invalid email or password')

    return render_template('login.html')


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

                    # Update the users table with the file name
                    cursor.execute('''
                        UPDATE users
                        SET profile_pic_url = %s
                        WHERE id = %s
                    ''', (filename, user_id))
                    mysql.connection.commit()

            cursor.close()

            # insert traits into captured traits
            captured_traits = []
            # Iterate over form data to get selected traits
            for key, value in request.form.items():
                if key.startswith('trait_category_') and value.isdigit():
                    trait_category_id = int(key.split('_')[-1])
                    captured_trait_id = int(value)
                    captured_traits.append((user_id, trait_category_id, captured_trait_id))

                # Insert selected traits into captured_traits table
            cursor = mysql.connection.cursor()
            cursor.executemany('''
                            INSERT INTO captured_learner_traits (user_id, trait_category_id, captured_trait)
                            VALUES (%s, %s, %s)
                        ''', captured_traits)
            mysql.connection.commit()
            cursor.close()


            return redirect(url_for('success_page'))

    # If it's a GET request, retrieve traits from the database
    user_id = session.get('user_id')  # Assuming you store user_id in the session after login
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


# capture instructor traits

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

            # insert more instructor details
            cursor = mysql.connection.cursor()
            cursor.execute('''
                INSERT INTO instructor_details (user_id, instructor_experience, instructor_charges, instructor_vehicle_transmission_type, instructor_vehicle_category, instructor_vehicle_model, instructor_description, instructor_mins_per_session)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ''', (user_id, instructor_experience, instructor_charges_per_session, vehicle_transmission_type, vehicle_category, vehicle_model, instructor_description, instructor_minutes_per_session ))
            mysql.connection.commit()
            cursor.close()



            # insert traits into captured traits
            captured_traits = []
            # Iterate over form data to get selected traits
            for key, value in request.form.items():
                if key.startswith('trait_category_') and value.isdigit():
                    trait_category_id = int(key.split('_')[-1])
                    captured_trait_id = int(value)
                    captured_traits.append((user_id, trait_category_id, captured_trait_id))

                # Insert selected traits into captured_traits table
            cursor = mysql.connection.cursor()
            cursor.executemany('''
                            INSERT INTO captured_traits (user_id, trait_category_id, captured_trait)
                            VALUES (%s, %s, %s)
                        ''', captured_traits)
            mysql.connection.commit()
            cursor.close()


            return redirect(url_for('instructor_success_page'))

    # If user_id is not available in the session
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
            return render_template('instructor_dashboard.html')
    return render_template('login.html')

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
    return render_template('view_all_instructors.html')




if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.run(debug=True)