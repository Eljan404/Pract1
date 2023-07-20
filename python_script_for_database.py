import psycopg2
import bcrypt 

conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="12bpform$4",
    port=5432

)
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(255) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL
    )
''')
conn.commit()

def register(username, password):
    hashed_password = hash_password(password)
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
        conn.commit()
        print("Registration successful!")
    except psycopg2.Error as e:
        print("Registration failed:", e)


def login(username, password):
    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    user = cursor.fetchone()
    if verify_password(password,user[2]):
        print("Login successful!")
    else:
        print("Login failed. Invalid username or password.")

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def verify_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

register("cemil32","rinq")  
login("cemil32","rinq") 



