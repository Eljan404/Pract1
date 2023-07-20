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
        print("Registration successful!")
        conn.commit()
        return True
    except psycopg2.IntegrityError:
        print("Registration failed because username already exists. Try again, please:")
        conn.rollback()  # Rollback the transaction
        return False
    except psycopg2.Error as e:
        print("Registration failed:", e)
        conn.rollback()  # Rollback the transaction
        return False

def login(username, password):
    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    user = cursor.fetchone()
    while user is None or not verify_password(password, user[2]):
        print("Login failed. Invalid username or password. Please, try again:")
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        user = cursor.fetchone()
    print("Login successful!")

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def verify_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

registration_success = False
while not registration_success:
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    registration_success = register(username, password)

login_username = input("Enter your username: ")
login_password = input("Enter your password: ")

login(login_username, login_password)

conn.close()
