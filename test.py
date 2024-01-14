@app.route('/find_instructors',  methods=['GET', 'POST'])
def find_instructors():
    user_id = session.get('user_id')
    user_info = None

    if user_id:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
        user_info = cursor.fetchone()
        cursor.close()
        if request.method == 'POST':
            vehicle_transmission_type = request.form.get('vehicle_transmission_type')
            vehicle_category = request.form.get('vehicle_category')
            experience = request.form.get('experience')
            charges_max = request.form.get('charges_max')
            min_experience = 0
            max_experience = 100
            if experience == 'zero':
                min_experience = 0
                max_experience = 1
            if experience == 'one-to-five':
                min_experience = 1
                max_experience = 5
            elif experience == 'six-to-nine':
                min_experience = 6
                max_experience = 9
            elif experience == 'ten-plus':
                min_experience = 10

            cursor = mysql.connection.cursor()
            query = (
                'SELECT * FROM instructor_details '
                'WHERE instructor_charges <= %s AND instructor_vehicle_transmission_type = %s '
                'AND instructor_vehicle_category = %s AND instructor_experience BETWEEN %s AND %s'
            )
            cursor.execute(query,
                           (charges_max, vehicle_transmission_type, vehicle_category, min_experience, max_experience))
            instructor_details = cursor.fetchall()
            cursor.close()
            for instructor_detail in instructor_details:
                cursor = mysql.connection.cursor()
                cursor.execute('SELECT * FROM users WHERE id = %s', (instructor_detail['user_id'],))
                filtered_instructors = cursor.fetchall()
                cursor.close()

            return render_template('view_instructors.html', instructor_details=instructor_details, filtered_instructors=filtered_instructors)

        return render_template('find_instructors.html', user_info=user_info)
    return render_template('view_all_instructors.html')