import sqlite3 as sql

# Connect to a database
conn = sql.connect('sample.db')

# Create a cursor
cur = conn.cursor()


# conn.execute('''DROP TABLE IF EXISTS user''') 

# # Create user Table
# conn.execute('''CREATE TABLE IF NOT EXISTS user 
#                 (user_id integer, 
#                 user_name text, 
#                 temp_threshold integer,
#                 hum_threshold integer,
#                 light_intensity_threshold integer)
#             ''') 

# cur.execute("INSERT INTO user (user_id, user_name, temp_threshold, hum_threshold, light_intensity_threshold) VALUES (NULL, 'Mubeenkh', 24, 60, 400)")
# cur.execute("INSERT INTO user (user_id, user_name, temp_threshold, hum_threshold, light_intensity_threshold) VALUES (NULL, 'RachelleBadua', 26, 70, 300)")
# cur.execute("INSERT INTO user (user_id, user_name, temp_threshold, hum_threshold, light_intensity_threshold) VALUES (NULL, NULL, NULL, NULL, NULL)")


# SELECT:
cur.execute("SELECT * FROM user")
conn.commit()
print(cur.fetchall())

# UPDATE:
# cur.execute("UPDATE user SET temp_threshold = 28, hum_threshold = 65 WHERE user_name = 'Mubeenkh'")
# cur.execute("SELECT * FROM user")
# conn.commit()
# print(cur.fetchall())

# DELETE:
# cur.execute("DELETE FROM user")
# cur.execute("SELECT * FROM user")
# conn.commit()
# print(cur.fetchall())




# Close DB object
cur.close()
conn.close()
