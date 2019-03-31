import sqlite3
user = 289257662
conn = sqlite3.connect('robo_users')
cursor = conn.cursor()
cursor.execute(f"UPDATE users SET ACCOUNT = 'owner' WHERE ID = {user}")
conn.commit()
cursor.execute(f'SELECT ACCOUNT FROM users WHERE ID = {user}')
res = cursor.fetchall()

conn.close()

if res != []:
    print(res)
else:
    print('kek')