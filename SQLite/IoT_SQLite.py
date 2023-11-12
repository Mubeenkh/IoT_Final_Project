#!/usr/bin/env python3
#############################################################################
# Filename    : IoT_SQLite.py
# Description :	Manipulating the 'iotdashboard' Database 
# Author      : Mubeen Khan
# modification: 2023/11/11
########################################################################
import sqlite3 as sql

class UserDatabase:
    
    def __init__(self):
        pass
        # Connect to a database
        self.conn = sql.connect('iotdashboard.db')
        # Create a cursor
        self.cur = self.conn.cursor()
        self.create_user_table()

    def create_user_table(self):
        
        # Drop the table if it already exists
        self.conn.execute('''DROP TABLE IF EXISTS user''') 

        # Create user Table
        self.conn.execute('''CREATE TABLE IF NOT EXISTS user 
                            (user_id integer, 
                            user_name text, 
                            temp_threshold integer,
                            hum_threshold integer,
                            light_intensity_threshold integer)
                        ''') 

        # Insert some default values when creating the table
        self.cur.execute("INSERT INTO user (user_id, user_name, temp_threshold, hum_threshold, light_intensity_threshold) VALUES (1962558, 'Mubeenkh', 24, 60, 400)")
        self.cur.execute("INSERT INTO user (user_id, user_name, temp_threshold, hum_threshold, light_intensity_threshold) VALUES (2131305, 'RachelleBadua', 26, 70, 300)")
        # self.cur.execute("INSERT INTO user (user_id, user_name, temp_threshold, hum_threshold, light_intensity_threshold) VALUES (NULL, NULL, NULL, NULL, NULL)")

    def insert_user(self,user_id, user_name, temp_threshold, hum_threshold, light_intensity_threshold):
        self.cur.execute('''INSERT INTO user (user_id, user_name, temp_threshold, hum_threshold, light_intensity_threshold) 
                            VALUES (?, ?, ?, ?, ?)''',
                            user_id, user_name, temp_threshold, hum_threshold, light_intensity_threshold)

    def select_all(self):
        # SELECT:
        self.cur.execute('''SELECT * FROM user''')
        # self.conn.commit()
        # print(self.cur.fetchall())
        return self.cur.fetchall()
    
    def select_user(self, user_id):
        # SELECT:
        self.cur.execute("SELECT * FROM user WHERE user_id = ?", (user_id,))
        # self.conn.commit()
        # print(self.cur.fetchall())
        return self.cur.fetchone()
    
    def update(self,user_id, temp_threshold, hum_threshold, light_intensity_threshold):
        # UPDATE:
        self.cur.execute('''UPDATE user 
                         SET temp_threshold = ?, hum_threshold = ?, light_intensity_threshold = ? WHERE user_id = ?''',
                         temp_threshold, hum_threshold, light_intensity_threshold, user_id)
        # self.cur.execute("SELECT * FROM user")
        self.conn.commit()
        # print(self.cur.fetchall())
        
    def delete(self, user_id):
        # DELETE:
        self.cur.execute("DELETE FROM user WHERE user_id = ?", user_id)
        # cur.execute("SELECT * FROM user")
        self.conn.commit()
        # print(cur.fetchall())

    def close_connection(self):
        # Close DB object
        self.cur.close()
        self.conn.close()


if __name__ == '__main__':
    
    user_table = UserDatabase();
        
    selectAll = user_table.select_all()
    print(selectAll)
    
    selectUser = user_table.select_user(1962558)
    print(selectUser)
    selectUser = user_table.select_user(2131305)
    print(selectUser)
    selectUser = user_table.select_user(123)
    print(selectUser)