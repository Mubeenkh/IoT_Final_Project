#!/usr/bin/env python3
#############################################################################
# Filename    : IoT_SQLite.py
# Description :	Manipulating the 'iotdashboard' Database 
# Author      : Mubeen Khan
# modification: 2023/11/11
########################################################################
import sqlite3 as sql

class IoTModel:
    
    conn = sql.connect('user_data.db')
    cur = conn.cursor()
    path = ""
    def __init__(self, path):
        self.path = path
        # self.conn = sql.connect(f'{path}')
        # self.cur = self.conn.cursor()
        self.open_connection()
        # self.create_user_table()

    def create_user_table(self):
        
        # Drop the table if it already exists
        self.conn.execute('''DROP TABLE IF EXISTS user''') 

        # Create user Table
        self.conn.execute('''CREATE TABLE IF NOT EXISTS user 
                            (user_id integer PRIMARY KEY, 
                            user_name text, 
                            user_email text,
                            temp_threshold integer,
                            hum_threshold integer,
                            light_intensity_threshold integer)
                        ''') 
        self.conn.commit()

    def insert_user(self,user_id, user_name,user_email, temp_threshold, hum_threshold, light_intensity_threshold):
        self.cur.execute('''INSERT INTO user (user_id, user_name, user_email, temp_threshold, hum_threshold, light_intensity_threshold) 
                            VALUES (?, ?, ?, ?, ?)''',
                            user_id, user_name,user_email, temp_threshold, hum_threshold, light_intensity_threshold)
        self.conn.commit()

    def insertData(self):
        self.cur.execute("INSERT INTO user (user_id, user_name, user_email, temp_threshold, hum_threshold, light_intensity_threshold) VALUES (117222150172, 'Mubeenkh', 'extramuffin0922@gmail.com', 24, 60, 400)")
        self.cur.execute("INSERT INTO user (user_id, user_name, user_email, temp_threshold, hum_threshold, light_intensity_threshold) VALUES (615925249, 'RachelleBadua', 'mubkhan01@gmail.com', 22, 70, 300)")
        self.cur.execute("INSERT INTO user (user_id, user_name, user_email, temp_threshold, hum_threshold, light_intensity_threshold) VALUES (16510311173, 'DamiVisa', 'damianovisa@gmail.com', 23, 75, 280)")
        self.cur.execute("INSERT INTO user (user_id, user_name, user_email, temp_threshold, hum_threshold, light_intensity_threshold) VALUES (13106149, 'JohnSmith', 'jsmith@hotmail.com', 24.4, 70, 350)")
        self.cur.execute("INSERT INTO user (user_id, user_name, user_email, temp_threshold, hum_threshold, light_intensity_threshold) VALUES (239601823, 'TheRock', 'dwane@gmail.com', 24, 80, 200)")
        self.conn.commit()
    
    def select_all(self):
        
        self.open_connection()
        self.cur.execute('''SELECT * FROM user''')
        self.conn.commit()
        return self.cur.fetchall()
    
    def select_user(self, user_id):
        
        self.open_connection()
        self.cur.execute("SELECT * FROM user WHERE user_id = ?", (user_id,))
        self.conn.commit()
        return self.cur.fetchone()
    
    def update(self,user_id, temp_threshold, hum_threshold, light_intensity_threshold):
        self.cur.execute('''UPDATE user 
                         SET temp_threshold = ?, hum_threshold = ?, light_intensity_threshold = ? WHERE user_id = ?''',
                         temp_threshold, hum_threshold, light_intensity_threshold, user_id)
        self.conn.commit()
        
    def delete(self, user_id):
        self.cur.execute("DELETE FROM user WHERE user_id = ?", user_id)
        self.conn.commit()

    def open_connection(self):
        # Open to DB object
        self.conn = sql.connect(f'{self.path}')
        self.cur = self.conn.cursor()
        
    def close_connection(self):
        # Close DB object
        self.cur.close()
        self.conn.close()
        

if __name__ == '__main__':
    path = 'user_data.db'
    user_table = IoTModel(path)
    # user_table.create_user_table()
    # user_table.insertData()

    # selectAll = user_table.select_all()
    # print(selectAll)

    
    selectUser = user_table.select_user(117222150172)
    # print(selectUser)
    selectUser = user_table.select_user(615925249)

    selectUser3 = user_table.select_user(16510311173)
    print(selectUser3)
    # user_table.close_connection()