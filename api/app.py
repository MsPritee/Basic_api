from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
import hashlib

app = Flask(__name__)
CORS(app)

def create_db():
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="pritee0000"
        )
        mycursor = mydb.cursor()
        mycursor.execute("CREATE DATABASE IF NOT EXISTS my_database")
        mycursor.execute("USE my_database")
        mycursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            username VARCHAR(255) UNIQUE,
                            password VARCHAR(255)
                        )''')
        mydb.commit()
    except Error as e:
        print(f"Error creating database or table: {e}")
    finally:
        if mydb.is_connected():
            mycursor.close()
            mydb.close()

create_db()

@app.route('/register', methods=['POST'])
def register():
    mydb = None  
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'message': 'Username and password are required'}), 400


        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="pritee0000",
            database="my_database"
        )
        mycursor = mydb.cursor()

        try:
            mycursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
            mydb.commit()
            return jsonify({'message': 'User registered successfully'}), 201
        except mysql.connector.errors.IntegrityError:
            return jsonify({'message': 'Username already exists'}), 400

    except Error as e:
        return jsonify({'message': f'Error: {e}'}), 500
    finally:
        if mydb and mydb.is_connected():
            mycursor.close()
            mydb.close()

if __name__ == '__main__':
    app.run(debug=True)
