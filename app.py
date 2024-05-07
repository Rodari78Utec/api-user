from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_mysqldb import MySQL

# Create an instance of Flask
app = Flask(__name__)
api = Api(app)

# Create an instance of MySQL
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'utec'
app.config['MYSQL_DB'] = 'bd_api'
app.config['MYSQL_HOST'] = '54.175.88.136'
app.config['MYSQL_PORT'] = 8005

mysql = MySQL(app)

# Get All Users, or Create a new user
class UserList(Resource):
    def get(self):
        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM otg_demo_users")
            rows = cur.fetchall()
            cur.close()
            return jsonify(rows)
        except Exception as e:
            print(e)

    def post(self):
        try:
            cur = mysql.connection.cursor()
            _name = request.form['name']
            _age = request.form['age']
            _city = request.form['city']
            insert_user_cmd = """INSERT INTO otg_demo_users(name, age, city) 
                                VALUES(%s, %s, %s)"""
            cur.execute(insert_user_cmd, (_name, _age, _city))
            mysql.connection.commit()
            user_id = cur.lastrowid
            cur.close()
            response = jsonify(message='User added successfully.', id=user_id)
            response.status_code = 200
            return response
        except Exception as e:
            print(e)
            response = jsonify('Failed to add user.')
            response.status_code = 400
            return response

# Get a user by id, update or delete user
class User(Resource):
    def get(self, user_id):
        try:
            cur = mysql.connection.cursor()
            cur.execute('SELECT * FROM otg_demo_users WHERE id = %s', (user_id,))
            row = cur.fetchone()
            cur.close()
            return jsonify(row)
        except Exception as e:
            print(e)

    def put(self, user_id):
        try:
            cur = mysql.connection.cursor()
            _name = request.form['name']
            _age = request.form['age']
            _city = request.form['city']
            update_user_cmd = """UPDATE otg_demo_users 
                                 SET name=%s, age=%s, city=%s
                                 WHERE id=%s"""
            cur.execute(update_user_cmd, (_name, _age, _city, user_id))
            mysql.connection.commit()
            cur.close()
            response = jsonify('User updated successfully.')
            response.status_code = 200
            return response
        except Exception as e:
            print(e)
            response = jsonify('Failed to update user.')
            response.status_code = 400
            return response

    def delete(self, user_id):
        try:
            cur = mysql.connection.cursor()
            cur.execute('DELETE FROM otg_demo_users WHERE id = %s', (user_id,))
            mysql.connection.commit()
            cur.close()
            response = jsonify('User deleted successfully.')
            response.status_code = 200
            return response
        except Exception as e:
            print(e)
            response = jsonify('Failed to delete user.')
            response.status_code = 400
            return response

# API resource routes
api.add_resource(UserList, '/users', endpoint='users')
api.add_resource(User, '/user/<int:user_id>', endpoint='user')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=False)
