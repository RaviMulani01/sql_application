from flask import Flask, jsonify, request
from connection import *

app = Flask(__name__)

# Create get endpoint for retrive all student Info
#URI : GET: http://127.0.0.1:5000/students
@app.route('/students', methods=['GET'])
def get_students():
    try:
        # Establish a database connection
        connection = Connection.getConn()

        # Create a cursor to interact with the database
        cursor = connection.cursor()

        # Execute an SQL query to retrieve student information
        query = "SELECT * FROM student_info"
        cursor.execute(query)

        # Fetch all the results
        results = cursor.fetchall()

        # Convert the results to a list of dictionaries
        student_list = []
        for row in results:
            student = {
                "studentid": row[0],
                "name": row[1],
                "phonenumber": row[2],
                "city": row[3]
            }
            student_list.append(student)

        # Close cursor and connection
        cursor.close()
        Connection.closeConn(connection)

        # Return the data as JSON
        return jsonify(student_list)

    except Exception as e:
        return jsonify({"error": str(e)})
    
# Create post endpoint for add student 
#URI : POST: http://127.0.0.1:5000/addstudents    
@app.route('/addstudents', methods=['POST'])
def add_student():
    try:
        # Establish a database connection
        connection = Connection.getConn()

        # Create a cursor to interact with the database
        cursor = connection.cursor()

        # Get data from the request
        data = request.json
        student_id = data['studentid']
        name = data['name']
        phone_number = data['phonenumber']
        city = data['city']

        # Execute an SQL query to insert a new student
        insert_query = "INSERT INTO student_info (studentid, name, phonenumber, city) VALUES (%s, %s, %s, %s)"
        cursor.execute(insert_query, (student_id, name, phone_number, city))

        # Commit the transaction
        connection.commit()

        # Close cursor and connection
        cursor.close()
        Connection.closeConn(connection)

        return 'Data added successfully'

    except Exception as e:
        return jsonify({"error": str(e)})

# Create PATCH endpoint for add student 
#URI : PATCH: http://127.0.0.1:5000//api/update/studentidNumber(1,2,3,etc..)       
@app.route('/api/update/<int:id>', methods=['PATCH'])
def update_data(id):
    try:
           # Establish a database connection
        connection = Connection.getConn()

        # Create a cursor to interact with the database
        cursor = connection.cursor()
        data = request.json  # Assuming the JSON data contains keys 'studentid', 'name', 'phonenumber', 'city'.

        # Get data from the request
        student_id = data['studentid']
        name = data['name']
        phone_number = data['phonenumber']
        city = data['city']

        # Execute an SQL query to update the student's information
        update_query = "UPDATE student_info SET studentid=%s, name=%s, phonenumber=%s, city=%s WHERE studentid=%s"
        cursor.execute(update_query, (student_id, name, phone_number, city, id))

        # Check how many rows were affected by the update
        rows_affected = cursor.rowcount

        connection.commit()

        # Close cursor and connection
        cursor.close()
        Connection.closeConn(connection)

        if rows_affected == 0:
            return 'No matching student found for the specified studentid', 404
        else:
            return 'Data updated successfully'
    
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    # make debug true to see the log details while app is running
    app.run(debug=True)
