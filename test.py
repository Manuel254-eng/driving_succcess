@app.route('/book_appointment', methods=['POST'])
def book_appointment():
    if request.method == 'POST':
        try:
            learner_id = request.form.get('learner_id')
            instructor_id = request.form.get('instructor_id')
            appointment_date_time = request.form.get('appointment_date_time')

            # Calculate the end time of the proposed appointment
            proposed_end_time = (datetime.datetime.strptime(appointment_date_time, '%Y-%m-%d %H:%M') + timedelta(
                hours=2)).strftime('%Y-%m-%d %H:%M')

            # Check if the appointment_date_time overlaps with existing appointments for the instructor
            cursor = mysql.connection.cursor()
            cursor.execute('''
                SELECT * FROM appointments 
                WHERE instructor_id = %s 
                AND (appointment_date_time < %s AND %s < (appointment_date_time + INTERVAL 2 HOUR))
            ''', (instructor_id, proposed_end_time, appointment_date_time))

            existing_appointment = cursor.fetchone()
            cursor.close()

            if existing_appointment:
                flash("The instructor already has another appointment during that time. Please select another time.",
                      "error")
                return redirect(url_for('view_single_instructor_details'))

            # If no existing appointment, proceed with inserting the new appointment
            cursor = mysql.connection.cursor()
            cursor.execute('''
                INSERT INTO appointments (learner_id, instructor_id, appointment_date_time)
                VALUES (%s, %s, %s)
            ''', (learner_id, instructor_id, appointment_date_time))

            mysql.connection.commit()
            cursor.close()

            flash("Appointment booked successfully", "success")
            return redirect(url_for('learner_dashboard'))
        except Exception as e:
            flash(f"An error occurred: {str(e)}", "error")

    return redirect(url_for('home'))