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

if __name__ == '__main__':
    # make debug true to see the log details while app is running
    app.run(debug=True)
