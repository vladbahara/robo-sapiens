import sqlite3
user = 289257662
conn = sqlite3.connect('robo_users')
cursor = conn.cursor()
cursor.execute(f'SELECT ACCOUNT FROM users WHERE ID = {user}')
res = cursor.fetchall()

if res != []:
    print(res[0][0])
else:
    print('kek')