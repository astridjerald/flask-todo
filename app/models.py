import sqlite3
from flask import Flask, jsonify

from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_jwt_extended import (create_access_token)
from datetime import datetime

bcrypt = Bcrypt()
jwt = JWTManager()


class Schema:
    def __init__(self):
        self.conn = sqlite3.connect('todo.db')
        self.create_user_table()
        self.create_to_do_table()

    def __del__(self):
        # body of destructor
        self.conn.commit()
        self.conn.close()

    def create_to_do_table(self):

        query = """
        CREATE TABLE IF NOT EXISTS "Todo" (
          id INTEGER PRIMARY KEY,
          Title TEXT,
          Description TEXT,
          _is_done boolean DEFAULT 0,
          _is_deleted boolean DEFAULT 0,
          CreatedOn Date DEFAULT CURRENT_DATE,
          DueDate Date,
          UserId INTEGER FOREIGNKEY REFERENCES User(_id)
        );
        """

        self.conn.execute(query)

    def create_user_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS "User" (
        _id INTEGER PRIMARY KEY AUTOINCREMENT, 
        first_name TEXT NOT NULL, 
        last_name TEXT,
        email TEXT NOT NULL,
        password TEXT NOT NULL, 
        created TEXT
        );
        """
        self.conn.execute(query)


class ToDoModel:
    TABLENAME = "Todo"

    def __init__(self):
        self.conn = sqlite3.connect('todo.db')
        self.conn.row_factory = sqlite3.Row

    def __del__(self):
        # body of destructor
        self.conn.commit()
        self.conn.close()

    def get_by_id(self, _id):
        where_clause = f"AND id={_id}"
        return self.list_items(where_clause)

    def create(self, params):
        print(params)
        query = f'insert into {self.TABLENAME} ' \
                f'(Title, Description, DueDate, UserId) ' \
                f'values ("{params.get("Title")}","{params.get("Description")}",' \
                f'"{params.get("DueDate")}","{params.get("UserId")}")'
        result = self.conn.execute(query)
        return self.get_by_id(result.lastrowid)

    def delete(self, item_id):
        query = f"UPDATE {self.TABLENAME} " \
                f"SET _is_deleted =  {1} " \
                f"WHERE id = {item_id}"
        print(query)
        self.conn.execute(query)
        query_new = f'SELECT * FROM {self.TABLENAME} ' \
            f'WHERE id = {item_id}'
        print(query_new)
        result = self.conn.execute(query_new).fetchone()
        UserId = result['UserId']
        where_clause = f" AND UserId={UserId}"
        return self.list_items(where_clause)

    def update(self, item_id, update_dict):
        """
        column: value
        Title: new title
        """

        set_query = ", ".join([f"{column} = '{value}'"
                               for column, value in update_dict.items()])

        query = f"UPDATE {self.TABLENAME} " \
                f"SET {set_query} " \
                f"WHERE id = {item_id}"
        print("The update query", query)
        self.conn.execute(query)
        return self.get_by_id(item_id)

    def list_items(self, where_clause=""):
        query = f"SELECT id, Title, Description, DueDate, _is_done " \
                f"from {self.TABLENAME} WHERE _is_deleted != {1} {where_clause}" \

        print(query)
        result_set = self.conn.execute(query).fetchall()
        result = [{column: row[i]
                   for i, column in enumerate(result_set[0].keys())}
                  for row in result_set]
        return result


class UserModel:
    TABLENAME = "User"

    def __init__(self):
        self.conn = sqlite3.connect('todo.db')
        self.conn.row_factory = sqlite3.Row

    def __del__(self):
        # body of destructor
        self.conn.commit()
        self.conn.close()

    def create(self, params):
        print("User params", params)
        first_name = params.get("first_name")
        last_name = params.get("last_name")
        email = params.get("email")
        created = datetime.utcnow()
        password = bcrypt.generate_password_hash(params.get('password')).decode('utf-8')
        print("params got",first_name,last_name,email,created,password)
        query = f'insert into {self.TABLENAME} ' \
                f'(first_name, last_name, email, password, created) ' \
                f'values ("{first_name}","{last_name}","{email}","{password}","{created}")'
        self.conn.execute(query)
        print("Query",query)
        return ({'result': {
            'first_name': first_name,
            'last_name': last_name,
            'created': created,
            'email': email,
            'password': password

        }})

    def login(self, params):
        email = params.get("email")
        password = params.get("password")
        query = f'SELECT * FROM User where email="{email}"'
        result = self.conn.execute(query).fetchone()

        if result != None and bcrypt.check_password_hash(result['password'], password):
            access_token = create_access_token(identity={
                'UserId': result['_id'],
                'first_name': result['first_name'], 'last_name': result['last_name'], 'email': result['email']})
            print("Flask userid", result['_id'])
            result = access_token
        else:
            result = {"error": "Invalid username/password"}
        return result
